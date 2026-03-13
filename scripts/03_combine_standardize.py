"""
03_combine_standardize.py — VUCA AEB Extension
================================================
Z-score all sub-measures over 2016–2019 baseline and combine into
final V, U, C, A scores.

Inputs:
    output/aeb_monthly.parquet
    output/quant_measures.parquet   (from 01_quant_vuca.py)
    output/text_measures.parquet    (from 02_text_vuca.py)

Outputs:
    output/vuca_monthly.parquet     — final VUCA scores + all sub-measures

Standardization protocol (per VUCA_method.docx):
    z = (x - mean_baseline) / sd_baseline
    where baseline = months with Year in [2016, 2019] (inclusive)

Combination:
    V_score = mean(V_quant_z, V_text_z)
    U_score = mean(U_quant_z, U_text_z)
    C_score = mean(C_quant_z, C_text_z)
    A_score = mean(A_quant_z, A_text_z)

    A_quant_z = mean of standardized A_kurtosis_z, A_bimodality_z, A_signflip_z

Usage:
    python scripts/03_combine_standardize.py
"""

import sys
import pathlib
import warnings
import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import config

warnings.filterwarnings("ignore")


# ── Standardization ───────────────────────────────────────────────────────────

def z_score_baseline(series: pd.Series, baseline_years: tuple[int, int]) -> pd.Series:
    """
    Z-score a series using mean and SD from the baseline period only.

    Parameters
    ----------
    series : pd.Series with DatetimeIndex
    baseline_years : (start_year, end_year) inclusive

    Returns
    -------
    pd.Series — full-sample z-scores relative to baseline statistics
    """
    start_yr, end_yr = baseline_years
    baseline_mask = (series.index.year >= start_yr) & (series.index.year <= end_yr)
    baseline_vals = series[baseline_mask].dropna()

    if len(baseline_vals) < 6:
        print(f"  [WARNING] {series.name}: only {len(baseline_vals)} baseline observations — "
              "z-score may be unreliable")

    mu = baseline_vals.mean()
    sd = baseline_vals.std()

    if sd == 0 or np.isnan(sd):
        print(f"  [WARNING] {series.name}: baseline SD = {sd:.4f} — returning NaN series")
        return pd.Series(np.nan, index=series.index, name=series.name + "_z")

    z = (series - mu) / sd
    z.name = series.name + "_z"
    return z


def standardize_all(quant: pd.DataFrame, text: pd.DataFrame) -> pd.DataFrame:
    """Z-score all sub-measures over baseline period."""
    print(f"\n[STANDARDIZE] Baseline period: {config.BASELINE_YEARS[0]}–{config.BASELINE_YEARS[1]}")

    all_measures = {
        # Quant
        "V_quant": quant["V_quant"],
        "U_quant": quant["U_quant"],
        "A_kurtosis": quant["A_kurtosis"],
        "A_bimodality": quant["A_bimodality"],
        "A_signflip": quant["A_signflip"],
        "C_fallback": quant["C_fallback"],
        # Text
        "V_text": text["V_text"],
        "U_text": text["U_text"],
        "C_text": text["C_text"],
        "C_quant_lda": text["C_quant"].rename("C_quant_lda"),
        "A_polarity_conflict": text["A_polarity_conflict"],
        "A_phrase_rate": text["A_phrase_rate"],
    }

    z_scores = {}
    for name, series in all_measures.items():
        print(f"  Standardizing {name}...")
        z = z_score_baseline(series, config.BASELINE_YEARS)
        z_scores[z.name] = z

    return pd.DataFrame(z_scores)


# ── Combination ───────────────────────────────────────────────────────────────

def combine_scores(z: pd.DataFrame) -> pd.DataFrame:
    """
    Combine z-scored sub-measures into final VUCA dimension scores.
    Equal-weight average within each dimension.
    """
    scores = pd.DataFrame(index=z.index)

    # V — Volatility
    scores["V_score"] = z[["V_quant_z", "V_text_z"]].mean(axis=1)

    # U — Uncertainty
    scores["U_score"] = z[["U_quant_z", "U_text_z"]].mean(axis=1)

    # C — Complexity
    # Prefer LDA-based scores; fall back to C_fallback if LDA is mostly NaN.
    # pandas .mean(axis=1) already skips NaN columns, so partial availability is fine.
    lda_coverage = z["C_quant_lda_z"].notna().mean()
    c_text_coverage = z["C_text_z"].notna().mean()
    if lda_coverage > 0.5 or c_text_coverage > 0.5:
        scores["C_score"] = z[["C_quant_lda_z", "C_text_z"]].mean(axis=1)
        print(f"[C] Using LDA-based C (LDA coverage: {lda_coverage:.0%}, "
              f"C_text coverage: {c_text_coverage:.0%})")
    else:
        scores["C_score"] = z["C_fallback_z"]
        print(f"[C] LDA unavailable — using C_fallback only "
              f"(LDA coverage: {lda_coverage:.0%}, C_text: {c_text_coverage:.0%})")

    # A — Ambiguity
    # A_quant = mean of A_kurtosis_z, A_bimodality_z, A_signflip_z
    a_quant_z = z[["A_kurtosis_z", "A_bimodality_z", "A_signflip_z"]].mean(axis=1)
    a_quant_z.name = "A_quant_z"
    a_text_z = z[["A_polarity_conflict_z", "A_phrase_rate_z"]].mean(axis=1)
    a_text_z.name = "A_text_z"
    scores["A_score"] = pd.concat([a_quant_z, a_text_z], axis=1).mean(axis=1)

    # Store intermediate A components for transparency
    scores["A_quant_z"] = a_quant_z
    scores["A_text_z"] = a_text_z

    return scores


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("03_combine_standardize.py — Standardize + Combine VUCA Scores")
    print("=" * 60)

    # Check inputs
    for fpath in [config.AEB_MONTHLY_FILE, config.QUANT_MEASURES_FILE, config.TEXT_MEASURES_FILE]:
        if not fpath.exists():
            raise FileNotFoundError(
                f"Required input missing: {fpath}\n"
                "Run 00_load_data.py, 01_quant_vuca.py, and 02_text_vuca.py first."
            )

    # Load
    aeb = pd.read_parquet(config.AEB_MONTHLY_FILE)
    quant = pd.read_parquet(config.QUANT_MEASURES_FILE)
    text = pd.read_parquet(config.TEXT_MEASURES_FILE)

    print(f"\n[INPUT] AEB monthly: {aeb.shape}")
    print(f"[INPUT] Quant measures: {quant.shape}")
    print(f"[INPUT] Text measures: {text.shape}")

    # Standardize
    z = standardize_all(quant, text)

    # Combine
    scores = combine_scores(z)

    # Build final output: VUCA scores + all sub-measures + AEB context
    out = pd.concat([scores, z, aeb[["AEB_mean", "AEB_n"]]], axis=1)

    print(f"\n[OUTPUT] Final VUCA dataset shape: {out.shape}")

    print("\n[OUTPUT] VUCA score descriptive statistics (baseline should be ≈ 0 mean, ≈ 1 SD):")
    baseline_mask = (out.index.year >= config.BASELINE_YEARS[0]) & (
        out.index.year <= config.BASELINE_YEARS[1]
    )
    for col in ["V_score", "U_score", "C_score", "A_score"]:
        bl = out.loc[baseline_mask, col].dropna()
        full = out[col].dropna()
        print(f"  {col}: baseline mean={bl.mean():.3f}, baseline SD={bl.std():.3f}, "
              f"full mean={full.mean():.3f}, full SD={full.std():.3f}")

    print("\n[OUTPUT] Full-sample VUCA scores:")
    print(out[["V_score", "U_score", "C_score", "A_score"]].describe().round(3).to_string())

    # Save
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out.to_parquet(config.VUCA_MONTHLY_FILE)
    print(f"\n[SAVED] {config.VUCA_MONTHLY_FILE}")
    print("  Next: python scripts/04_validation.py")


if __name__ == "__main__":
    main()
