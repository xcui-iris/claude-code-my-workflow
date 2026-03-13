"""
04b_granger_validation.py — VUCA AEB Extension
================================================
Phase 2 predictive validity: Granger causality tests between VUCA scores
and external agricultural economic indicators.

External data: Creighton University Main Street Economy survey
  - Loan Volume index (monthly diffusion index)
  - Farm Equipment Sales index (monthly diffusion index)
  - Farmland Prices index (monthly diffusion index)
Source file: farmloan_equipmentsale_indices.xlsx
  Structure: one sheet per year (e.g. "2016", "2017"...)
  Each sheet: rows = Index / Loan volume / Farmland prices / Farm equipment sales
              cols = Index name + Jan..Dec

Inputs:
    output/vuca_monthly.parquet
    farmloan_equipmentsale_indices.xlsx  (at DATA_ROOT)

Outputs:
    output/tables/granger_results.csv
    output/tables/granger_summary.txt

Usage:
    python scripts/04b_granger_validation.py
"""

import sys
import pathlib
import warnings
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller, grangercausalitytests

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import config

warnings.filterwarnings("ignore")

EXTERNAL_FILE = config.DATA_ROOT / "farmloan_equipmentsale_indices.xlsx"
MAX_LAGS = 4  # test up to 4 monthly lags


# ── Load external data ────────────────────────────────────────────────────────

def load_external_data(path: pathlib.Path) -> pd.DataFrame:
    """
    Load all year sheets from the Creighton xlsx and combine into
    a single monthly time series DataFrame.

    Sheet structure (per the 2025 sample):
      Row 0: month labels (Jan, Feb, ..., Dec)
      Row 1: Loan volume
      Row 2: Farmland prices
      Row 3: Farm equipment sales
      Col 0: index/variable name
      Cols 1-12: monthly values
    """
    xl = pd.ExcelFile(path)
    year_sheets = []
    for sheet in xl.sheet_names:
        try:
            year = int(sheet)
        except ValueError:
            continue  # skip non-year sheets

        df = xl.parse(sheet, header=None)

        # Row 0 should be month labels; rows 1+ are variables
        # Find the row that contains 'Jan' or 'jan'
        header_row = None
        for i, row in df.iterrows():
            if any(str(v).strip().lower() == "jan" for v in row.values):
                header_row = i
                break

        if header_row is None:
            print(f"  [WARN] Sheet {year}: could not find month header row — skipping")
            continue

        months_row = df.iloc[header_row]
        data_rows = df.iloc[header_row + 1:].reset_index(drop=True)

        # Build month→column mapping
        month_map = {
            "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
            "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
        }
        col_to_month = {}
        for col_idx, val in months_row.items():
            key = str(val).strip().lower()[:3]
            if key in month_map:
                col_to_month[col_idx] = month_map[key]

        if not col_to_month:
            print(f"  [WARN] Sheet {year}: no month columns found — skipping")
            continue

        # Parse each variable row
        records = []
        for _, row in data_rows.iterrows():
            var_name = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
            if not var_name or var_name.lower() in ("nan", "index", ""):
                continue
            for col_idx, month in col_to_month.items():
                val = pd.to_numeric(row[col_idx], errors="coerce")
                records.append({
                    "Year": year,
                    "Month": month,
                    "Variable": var_name,
                    "Value": val,
                })

        year_sheets.append(pd.DataFrame(records))

    if not year_sheets:
        raise ValueError(f"No valid year sheets found in {path}")

    long = pd.concat(year_sheets, ignore_index=True)

    # Pivot to wide format: one column per variable
    wide = (
        long.pivot_table(index=["Year", "Month"], columns="Variable", values="Value", aggfunc="mean")
        .reset_index()
        .sort_values(["Year", "Month"])
        .reset_index(drop=True)
    )
    wide.columns.name = None

    # Build DatetimeIndex
    wide["Date"] = pd.to_datetime(
        wide["Year"].astype(str) + "-" + wide["Month"].astype(str).str.zfill(2)
    )
    wide = wide.set_index("Date").drop(columns=["Year", "Month"])

    print(f"[EXTERNAL] Loaded {len(wide)} months from {len(year_sheets)} year sheets")
    print(f"[EXTERNAL] Date range: {wide.index[0].strftime('%Y-%m')} → {wide.index[-1].strftime('%Y-%m')}")
    print(f"[EXTERNAL] Variables: {list(wide.columns)}")
    print(f"[EXTERNAL] Sample:\n{wide.head(3).to_string()}")

    return wide


def standardize_col_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names to snake_case for easier referencing."""
    rename = {}
    for col in df.columns:
        key = col.lower().strip()
        if "loan" in key:
            rename[col] = "loan_volume"
        elif "equipment" in key or "farm equip" in key:
            rename[col] = "equipment_sales"
        elif "farmland" in key or "land price" in key:
            rename[col] = "farmland_prices"
        else:
            rename[col] = col.lower().replace(" ", "_")
    return df.rename(columns=rename)


# ── Stationarity ──────────────────────────────────────────────────────────────

def check_stationarity(series: pd.Series, name: str) -> tuple[bool, pd.Series]:
    """
    ADF test for stationarity. If non-stationary, first-difference and retest.
    Returns (is_stationary_after_transform, transformed_series).
    """
    s = series.dropna()
    result = adfuller(s, autolag="AIC")
    p = result[1]
    if p < 0.05:
        print(f"  {name}: stationary (ADF p={p:.3f})")
        return True, series
    else:
        print(f"  {name}: non-stationary (ADF p={p:.3f}) — first-differencing")
        s_diff = series.diff()
        result2 = adfuller(s_diff.dropna(), autolag="AIC")
        p2 = result2[1]
        status = "stationary" if p2 < 0.05 else "STILL non-stationary"
        print(f"  {name} (differenced): {status} (ADF p={p2:.3f})")
        return p2 < 0.05, s_diff


# ── Granger tests ─────────────────────────────────────────────────────────────

def run_granger_tests(
    vuca: pd.DataFrame,
    external: pd.DataFrame,
    max_lags: int = MAX_LAGS,
) -> pd.DataFrame:
    """
    Test: does each VUCA score Granger-cause each external series?

    For each (VUCA_dim, external_var) pair, we test:
      H0: VUCA_dim does NOT Granger-cause external_var
    A low p-value rejects H0 → VUCA_dim has predictive content for external_var.
    """
    vuca_dims = ["V_score", "U_score", "C_score", "A_score"]
    ext_vars = [c for c in external.columns if c in ["loan_volume", "equipment_sales", "farmland_prices"]]

    if not ext_vars:
        raise ValueError(
            "Could not find expected columns in external data. "
            f"Found: {list(external.columns)}"
        )

    # Align on common date range
    combined = vuca[vuca_dims].join(external[ext_vars], how="inner")
    print(f"\n[GRANGER] Aligned sample: {len(combined)} months "
          f"({combined.index[0].strftime('%Y-%m')} → {combined.index[-1].strftime('%Y-%m')})")

    print("\n[STATIONARITY] ADF tests:")
    stationary_cols = {}
    transformed = pd.DataFrame(index=combined.index)
    for col in vuca_dims + ext_vars:
        is_stat, series = check_stationarity(combined[col], col)
        stationary_cols[col] = is_stat
        transformed[col] = series

    transformed = transformed.dropna()

    results = []
    print(f"\n[GRANGER] Testing causality (max lags = {max_lags}):")
    print(f"  {'VUCA → External':<35} {'Lag':>4} {'F-stat':>8} {'p-value':>8} {'Sig':>5}")
    print("  " + "-" * 62)

    for dim in vuca_dims:
        for ext_var in ext_vars:
            pair = transformed[[ext_var, dim]].dropna()
            if len(pair) < max_lags * 3 + 10:
                print(f"  {dim} → {ext_var}: insufficient observations ({len(pair)})")
                continue
            try:
                gc_res = grangercausalitytests(pair, maxlag=max_lags, verbose=False)
                for lag in range(1, max_lags + 1):
                    f_stat = gc_res[lag][0]["ssr_ftest"][0]
                    p_val = gc_res[lag][0]["ssr_ftest"][1]
                    sig = "***" if p_val < 0.01 else "**" if p_val < 0.05 else "*" if p_val < 0.10 else ""
                    label = f"{dim} → {ext_var}"
                    print(f"  {label:<35} {lag:>4} {f_stat:>8.3f} {p_val:>8.3f} {sig:>5}")
                    results.append({
                        "vuca_dim": dim,
                        "external_var": ext_var,
                        "lag": lag,
                        "f_stat": round(f_stat, 3),
                        "p_value": round(p_val, 3),
                        "significant_10": p_val < 0.10,
                        "significant_5": p_val < 0.05,
                        "significant_1": p_val < 0.01,
                    })
            except Exception as e:
                print(f"  {dim} → {ext_var}: ERROR — {e}")

    return pd.DataFrame(results)


# ── Summary ───────────────────────────────────────────────────────────────────

def write_summary(results: pd.DataFrame, path: pathlib.Path) -> None:
    """Write human-readable Granger results summary."""
    lines = [
        "VUCA → Agricultural Indicators: Granger Causality Results",
        "=" * 60,
        f"Source: Creighton University Main Street Economy Survey",
        f"Max lags tested: {MAX_LAGS} months",
        "",
        "Significance: *** p<0.01  ** p<0.05  * p<0.10",
        "",
    ]

    for ext_var in results["external_var"].unique():
        lines.append(f"\n{ext_var.replace('_', ' ').title()}")
        lines.append("-" * 40)
        sub = results[results["external_var"] == ext_var]
        for dim in sub["vuca_dim"].unique():
            best = sub[sub["vuca_dim"] == dim].sort_values("p_value").iloc[0]
            sig = "***" if best["significant_1"] else "**" if best["significant_5"] else "*" if best["significant_10"] else "n.s."
            lines.append(
                f"  {dim}: best lag={best['lag']}, "
                f"F={best['f_stat']:.3f}, p={best['p_value']:.3f} {sig}"
            )

    lines += [
        "",
        "Note: Granger causality tests whether lagged VUCA scores contain",
        "predictive information for the external series beyond the series'",
        "own lags. It does not imply structural causation.",
        "",
        "Phase 2 extension: consider VAR impulse-response functions",
        "for the significant pairs.",
    ]

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[SAVED] {path}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("04b_granger_validation.py — Predictive Validity (Phase 2)")
    print("=" * 60)

    if not EXTERNAL_FILE.exists():
        raise FileNotFoundError(
            f"External data file not found: {EXTERNAL_FILE}\n"
            f"Expected at: {EXTERNAL_FILE}"
        )
    if not config.VUCA_MONTHLY_FILE.exists():
        raise FileNotFoundError(
            f"VUCA scores not found: {config.VUCA_MONTHLY_FILE}\n"
            "Run 03_combine_standardize.py first."
        )

    # Load
    external_raw = load_external_data(EXTERNAL_FILE)
    external = standardize_col_names(external_raw)

    vuca = pd.read_parquet(config.VUCA_MONTHLY_FILE)
    print(f"\n[VUCA] Loaded: {vuca.shape}, "
          f"{vuca.index[0].strftime('%Y-%m')} → {vuca.index[-1].strftime('%Y-%m')}")

    # Run Granger tests
    results = run_granger_tests(vuca, external)

    if results.empty:
        print("\n[WARN] No Granger results produced — check data alignment and column names")
        return

    # Save
    config.TABLES_DIR.mkdir(parents=True, exist_ok=True)
    results_path = config.TABLES_DIR / "granger_results.csv"
    results.to_csv(results_path, index=False)
    print(f"\n[SAVED] {results_path}")

    write_summary(results, config.TABLES_DIR / "granger_summary.txt")

    print("\n[DONE] 04b_granger_validation.py complete.")


if __name__ == "__main__":
    main()
