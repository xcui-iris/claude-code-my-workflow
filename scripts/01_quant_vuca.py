"""
01_quant_vuca.py — VUCA AEB Extension
========================================
Compute quantitative VUCA sub-measures from AEB panel data.

Inputs:
    output/aeb_monthly.parquet   (from 00_load_data.py)

Outputs:
    output/quant_measures.parquet

Measures:
    V_quant  — rolling 12-mo SD of monthly AEB first-differences
    U_quant  — cross-sectional variance of individual future expectations
    A_kurtosis  — monthly excess kurtosis of individual AEB distribution
    A_bimodality — Hartigan dip test p-value (bimodal if p < 0.05)
    A_signflip   — rolling 6-mo count of skewness sign changes
    C_fallback   — rolling SD of ICC–IFE spread (proxy if LDA unavailable)

Usage:
    python scripts/01_quant_vuca.py
"""

import sys
import pathlib
import warnings
import pandas as pd
import numpy as np
from scipy import stats

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import config

warnings.filterwarnings("ignore")

# Optional: diptest package for Hartigan dip test
try:
    import diptest
    HAS_DIPTEST = True
except ImportError:
    HAS_DIPTEST = False
    print("[WARNING] 'diptest' package not found. A_bimodality will use kurtosis proxy.")
    print("          Install with: pip install diptest")


# ── helpers ──────────────────────────────────────────────────────────────────

def load_aeb_individual(path: pathlib.Path) -> pd.DataFrame:
    """Reload raw AEB for individual-level measures."""
    import openpyxl  # noqa: F401
    df = pd.read_excel(
        config.AEB_FILE, sheet_name=config.AEB_SHEET, header=None
    )
    df = df.rename(columns={k: v for k, v in config.AEB_COLUMN_NAMES.items() if k < df.shape[1]})
    for col in ["Month", "Year", "AEB", "Q2_idx", "Q3_idx", "Q4_idx"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["Year", "Month", "AEB"])
    df["Year"] = df["Year"].astype(int)
    df["Month"] = df["Month"].astype(int)
    df["Year"] = df["Year"].apply(lambda y: y + 2000 if y < 100 else y)
    df["FutExp_indiv"] = df[["Q2_idx", "Q3_idx", "Q4_idx"]].mean(axis=1)
    return df


# ── V — Volatility ───────────────────────────────────────────────────────────

def compute_v_quant(monthly: pd.DataFrame) -> pd.Series:
    """
    V_quant = rolling 12-month SD of monthly AEB first-differences.

    First-difference: delta_AEB[t] = AEB_mean[t] - AEB_mean[t-1]
    Rolling SD applied to delta_AEB over window of ROLLING_WINDOW_V months.
    """
    delta = monthly["AEB_mean"].diff()
    v = delta.rolling(config.ROLLING_WINDOW_V, min_periods=6).std()
    v.name = "V_quant"
    print(f"[V_quant] Non-null: {v.notna().sum()} months")
    print(f"[V_quant] Mean: {v.mean():.3f}, SD: {v.std():.3f}")
    return v


# ── U — Uncertainty ──────────────────────────────────────────────────────────

def compute_u_quant(monthly: pd.DataFrame) -> pd.Series:
    """
    U_quant = inverted IFE (Index of Future Expectations).

    U_quant = -IFE_mean_t

    When farmers are uncertain/pessimistic about the future, IFE falls and
    U_quant rises. This captures aggregate uncertainty, not cross-sectional
    disagreement. See quality_reports/specs/2026-03-13_u-quant-decision.md.
    """
    u = -monthly["IFE_mean"]
    u.name = "U_quant"
    print(f"[U_quant] Non-null: {u.notna().sum()} months")
    print(f"[U_quant] Mean: {u.mean():.3f}, SD: {u.std():.3f}")
    return u


# ── A — Ambiguity ─────────────────────────────────────────────────────────────

def compute_a_kurtosis(individual: pd.DataFrame) -> pd.Series:
    """Excess kurtosis of individual AEB distribution per month (Fisher definition)."""
    def month_kurtosis(grp):
        if len(grp) < 4:
            return np.nan
        return stats.kurtosis(grp["AEB"].dropna(), fisher=True)

    kurt = (
        individual.groupby(["Year", "Month"])
        .apply(month_kurtosis)
        .reset_index(name="A_kurtosis")
    )
    kurt["Date"] = pd.to_datetime(
        kurt["Year"].astype(str) + "-" + kurt["Month"].astype(str).str.zfill(2)
    )
    series = kurt.set_index("Date")["A_kurtosis"]
    series.name = "A_kurtosis"
    print(f"[A_kurtosis] Non-null: {series.notna().sum()} months")
    return series


def compute_a_bimodality(individual: pd.DataFrame) -> pd.Series:
    """
    Hartigan dip test p-value per month.
    Bimodal = p < 0.05 → A_bimodality = 1 - p (higher = more bimodal).
    Falls back to kurtosis proxy if diptest not installed.
    """
    results = {}
    for (year, month), grp in individual.groupby(["Year", "Month"]):
        aeb_vals = grp["AEB"].dropna().values
        date = pd.Timestamp(f"{year}-{month:02d}-01")

        if len(aeb_vals) < config.MIN_RESPONSES_DIP:
            results[date] = np.nan
            continue

        if HAS_DIPTEST:
            _, p_val = diptest.diptest(aeb_vals)
            results[date] = 1 - p_val  # high = more bimodal
        else:
            # Proxy: bimodality coefficient (DeCarlo 1997)
            n = len(aeb_vals)
            k = stats.kurtosis(aeb_vals, fisher=True)
            g = stats.skew(aeb_vals)
            bc = (g**2 + 1) / (k + 3 * ((n - 1)**2 / ((n - 2) * (n - 3))))
            results[date] = bc  # threshold ~0.555 for bimodality

    series = pd.Series(results, name="A_bimodality")
    series.index = pd.DatetimeIndex(series.index)
    series = series.sort_index()
    n_sparse = (individual.groupby(["Year", "Month"])["AEB"].count() < config.MIN_RESPONSES_DIP).sum()
    if n_sparse:
        print(f"[A_bimodality] WARNING: {n_sparse} months skipped (N < {config.MIN_RESPONSES_DIP})")
    print(f"[A_bimodality] Non-null: {series.notna().sum()} months")
    return series


def compute_a_signflip(monthly: pd.DataFrame) -> pd.Series:
    """
    Rolling 6-month count of skewness sign changes in monthly AEB distribution.
    Uses monthly skewness of individual AEB per month, then counts sign flips
    in a 6-month rolling window.

    Note: this uses AEB_mean from the monthly panel as a proxy for skewness
    direction; full individual-level skewness is computed in compute_a_kurtosis.
    We compute monthly skewness separately here.
    """
    # We need individual-level for this — reload handled by caller
    # Here we use the A_kurtosis helper approach on skewness
    pass  # Filled in main() after individual is loaded


def compute_a_signflip_from_individual(individual: pd.DataFrame) -> pd.Series:
    """Compute monthly skewness, then rolling 6-mo sign-flip count."""
    def month_skew(grp):
        if len(grp) < 4:
            return np.nan
        return stats.skew(grp["AEB"].dropna())

    monthly_skew = (
        individual.groupby(["Year", "Month"])
        .apply(month_skew)
        .reset_index(name="skew")
    )
    monthly_skew["Date"] = pd.to_datetime(
        monthly_skew["Year"].astype(str) + "-" + monthly_skew["Month"].astype(str).str.zfill(2)
    )
    skew_series = monthly_skew.set_index("Date")["skew"].sort_index()

    # Sign flip: 1 if sign(skew[t]) != sign(skew[t-1])
    sign = np.sign(skew_series)
    flip = (sign != sign.shift(1)).astype(float)
    flip[skew_series.isna()] = np.nan

    # Rolling 6-month sum of flips
    signflip = flip.rolling(6, min_periods=3).sum()
    signflip.name = "A_signflip"
    print(f"[A_signflip] Non-null: {signflip.notna().sum()} months")
    return signflip


# ── C — Complexity fallback ───────────────────────────────────────────────────

def compute_c_fallback(monthly: pd.DataFrame) -> pd.Series:
    """
    C_fallback = rolling SD of ICC–IFE spread.
    Used if LDA topic model is unavailable.
    """
    spread = monthly["ICC_mean"] - monthly["IFE_mean"]
    c = spread.rolling(12, min_periods=6).std()
    c.name = "C_fallback"
    print(f"[C_fallback] Non-null: {c.notna().sum()} months")
    return c


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("01_quant_vuca.py — Quantitative VUCA Measures")
    print("=" * 60)

    if not config.AEB_MONTHLY_FILE.exists():
        raise FileNotFoundError(
            f"Monthly AEB file not found: {config.AEB_MONTHLY_FILE}\n"
            "Run 00_load_data.py first."
        )

    # Load monthly aggregates
    monthly = pd.read_parquet(config.AEB_MONTHLY_FILE)
    print(f"\n[INPUT] Monthly panel: {monthly.shape}")

    # Load individual-level data for A measures (U no longer needs individual data)
    print("\n[INPUT] Loading individual-level AEB for A measures...")
    individual = load_aeb_individual(config.AEB_FILE)
    print(f"[INPUT] Individual rows: {len(individual)}")

    # Compute measures
    v_quant = compute_v_quant(monthly)
    u_quant = compute_u_quant(monthly)
    a_kurtosis = compute_a_kurtosis(individual)
    a_bimodality = compute_a_bimodality(individual)
    a_signflip = compute_a_signflip_from_individual(individual)
    c_fallback = compute_c_fallback(monthly)

    # Combine into one DataFrame aligned on Date index
    out = pd.DataFrame({
        "V_quant": v_quant,
        "U_quant": u_quant,
        "A_kurtosis": a_kurtosis,
        "A_bimodality": a_bimodality,
        "A_signflip": a_signflip,
        "C_fallback": c_fallback,
    })

    print(f"\n[OUTPUT] Quant measures shape: {out.shape}")
    print("\n[OUTPUT] Summary (non-null counts):")
    print(out.notna().sum().to_string())
    print("\n[OUTPUT] Descriptive statistics:")
    print(out.describe().round(3).to_string())

    # Spot check: print values around COVID (2020-03) and trade war (2019-05)
    print("\n[SPOT CHECK] Values at key events:")
    events = ["2019-05", "2020-03", "2022-03"]
    for e in events:
        try:
            row = out.loc[e]
            if isinstance(row, pd.DataFrame):
                row = row.iloc[0]
            print(f"  {e}: V_quant={row['V_quant']:.3f}, U_quant={row['U_quant']:.3f}, "
                  f"A_kurtosis={row['A_kurtosis']:.3f}")
        except KeyError:
            print(f"  {e}: not in index")

    # Save
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out.to_parquet(config.QUANT_MEASURES_FILE)
    print(f"\n[SAVED] {config.QUANT_MEASURES_FILE}")
    print("  Next: python scripts/02_text_vuca.py")


if __name__ == "__main__":
    main()
