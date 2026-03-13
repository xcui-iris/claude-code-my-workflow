"""
04_validation.py — VUCA AEB Extension
=========================================
Validate VUCA scores: face validity, convergent validity,
discriminant validity, and robustness checks.

Inputs:
    output/vuca_monthly.parquet     (from 03_combine_standardize.py)
    output/quant_measures.parquet   (for robustness: 6-month V re-estimate)

Outputs:
    output/tables/validation_correlations.csv
    output/tables/validation_summary.txt

Predictive validity (Granger causality against external series) is Phase 2.
This script covers internal validation only.

Usage:
    python scripts/04_validation.py
"""

import sys
import pathlib
import warnings
import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import config

warnings.filterwarnings("ignore")


# ── Face Validity ─────────────────────────────────────────────────────────────

def face_validity_check(vuca: pd.DataFrame) -> dict:
    """
    Check that VUCA scores are elevated around known shock events.
    Returns a dict of {event: {dim: value_at_event, mean_baseline, ratio}}
    """
    baseline_mask = (vuca.index.year >= config.BASELINE_YEARS[0]) & (
        vuca.index.year <= config.BASELINE_YEARS[1]
    )
    dims = ["V_score", "U_score", "C_score", "A_score"]
    baseline_means = vuca.loc[baseline_mask, dims].mean()

    results = {}
    print("\n[FACE VALIDITY] Score values at key shock events (vs. baseline mean):")
    print(f"  {'Event':<35} {'V':>7} {'U':>7} {'C':>7} {'A':>7}")
    print("  " + "-" * 63)

    for date, label in config.EVENT_DATES:
        # Use ±2 month window around event to capture delayed response
        window = vuca.loc[
            (vuca.index >= date - pd.DateOffset(months=1)) &
            (vuca.index <= date + pd.DateOffset(months=2)),
            dims
        ]
        if window.empty:
            event_vals = pd.Series(np.nan, index=dims)
        else:
            event_vals = window.mean()

        row = {}
        for d in dims:
            row[d] = {"value": event_vals[d], "baseline_mean": baseline_means[d]}
        results[label] = row

        vals_str = "  ".join(f"{event_vals[d]:>7.2f}" for d in dims)
        print(f"  {label:<35} {vals_str}")

    bl_str = "  ".join(f"{baseline_means[d]:>7.2f}" for d in dims)
    print(f"\n  {'Baseline mean (2016–2019)':<35} {bl_str}")

    return results


# ── Convergent Validity ───────────────────────────────────────────────────────

def convergent_validity(vuca: pd.DataFrame) -> pd.DataFrame:
    """
    Correlate V, U, C, A with AEB_mean and IFE-based measures.
    Expected: U negatively correlated with AEB (high uncertainty → low barometer).
    """
    dims = ["V_score", "U_score", "C_score", "A_score"]
    targets = ["AEB_mean"]

    # Add IFE if present from AEB monthly
    if "IFE_mean" in vuca.columns:
        targets.append("IFE_mean")

    pairs = []
    print("\n[CONVERGENT VALIDITY] Pearson and Spearman correlations with AEB indicators:")
    print(f"\n  {'Pair':<35} {'Pearson r':>10} {'p-value':>10} {'Spearman r':>10} {'p-value':>10}")
    print("  " + "-" * 75)

    for dim in dims:
        for target in targets:
            joint = vuca[[dim, target]].dropna()
            if len(joint) < 10:
                continue
            pearson_r, pearson_p = stats.pearsonr(joint[dim], joint[target])
            spearman_r, spearman_p = stats.spearmanr(joint[dim], joint[target])
            pairs.append({
                "dimension": dim,
                "target": target,
                "pearson_r": round(pearson_r, 3),
                "pearson_p": round(pearson_p, 3),
                "spearman_r": round(spearman_r, 3),
                "spearman_p": round(spearman_p, 3),
                "n": len(joint),
            })
            label = f"{dim} vs {target}"
            print(f"  {label:<35} {pearson_r:>10.3f} {pearson_p:>10.3f} "
                  f"{spearman_r:>10.3f} {spearman_p:>10.3f}")

    # Check expected sign for U vs AEB
    u_aeb = [p for p in pairs if p["dimension"] == "U_score" and p["target"] == "AEB_mean"]
    if u_aeb:
        r = u_aeb[0]["pearson_r"]
        if r > 0:
            print(f"\n  [WARNING] U_score vs AEB_mean: r={r:.3f} is POSITIVE (expected negative).")
            print("            Verify U_quant and U_text are capturing disagreement, not confidence.")
        else:
            print(f"\n  [OK] U_score vs AEB_mean: r={r:.3f} (expected negative — check)")

    return pd.DataFrame(pairs)


# ── Discriminant Validity ─────────────────────────────────────────────────────

def discriminant_validity(vuca: pd.DataFrame) -> pd.DataFrame:
    """
    Cross-correlation matrix of V, U, C, A.
    Expect low-to-moderate inter-correlations (each captures distinct dimension).
    """
    dims = ["V_score", "U_score", "C_score", "A_score"]
    joint = vuca[dims].dropna()

    pearson_mat = joint.corr(method="pearson").round(3)
    print("\n[DISCRIMINANT VALIDITY] VUCA dimension cross-correlation (Pearson):")
    print(pearson_mat.to_string())

    # Flag high correlations (>0.8)
    for i, d1 in enumerate(dims):
        for d2 in dims[i + 1:]:
            r = pearson_mat.loc[d1, d2]
            if abs(r) > 0.8:
                print(f"\n  [WARNING] High correlation: {d1} vs {d2} = {r:.3f}")
                print("            These dimensions may not be sufficiently distinct.")

    return pearson_mat


# ── Robustness ────────────────────────────────────────────────────────────────

def robustness_check(vuca: pd.DataFrame, quant: pd.DataFrame) -> pd.Series:
    """
    Re-estimate V_quant with 6-month rolling window (vs baseline 12-month).
    Report correlation between baseline and robust V series.
    """
    aeb_mean = vuca["AEB_mean"]
    delta = aeb_mean.diff()
    v_robust = delta.rolling(config.ROLLING_WINDOW_ROBUST, min_periods=3).std()
    v_baseline = quant["V_quant"]

    # Align
    joint = pd.concat([v_baseline, v_robust], axis=1).dropna()
    joint.columns = ["V_12mo", "V_6mo"]

    pearson_r, _ = stats.pearsonr(joint["V_12mo"], joint["V_6mo"])
    spearman_r, _ = stats.spearmanr(joint["V_12mo"], joint["V_6mo"])

    print(f"\n[ROBUSTNESS] V_quant: 12-month vs 6-month rolling window")
    print(f"  Pearson r = {pearson_r:.3f}, Spearman r = {spearman_r:.3f}")
    if pearson_r > 0.9:
        print("  [OK] High correlation — results are robust to window choice.")
    else:
        print("  [CAUTION] Moderate correlation — window choice may matter. Investigate.")

    return v_robust


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("04_validation.py — VUCA Score Validation")
    print("=" * 60)

    for fpath in [config.VUCA_MONTHLY_FILE, config.QUANT_MEASURES_FILE]:
        if not fpath.exists():
            raise FileNotFoundError(
                f"Required input missing: {fpath}\n"
                "Run previous scripts in order first."
            )

    vuca = pd.read_parquet(config.VUCA_MONTHLY_FILE)
    quant = pd.read_parquet(config.QUANT_MEASURES_FILE)

    # Merge AEB monthly context if not already in vuca
    if "AEB_mean" not in vuca.columns:
        aeb = pd.read_parquet(config.AEB_MONTHLY_FILE)
        vuca = vuca.join(aeb[["AEB_mean"]], how="left")

    print(f"\n[INPUT] VUCA monthly: {vuca.shape}")
    print(f"[INPUT] Date range: {vuca.index[0]} → {vuca.index[-1]}")

    # Run validation checks
    face_validity_check(vuca)
    corr_df = convergent_validity(vuca)
    discrim_mat = discriminant_validity(vuca)
    v_robust = robustness_check(vuca, quant)

    # Save outputs
    config.TABLES_DIR.mkdir(parents=True, exist_ok=True)

    corr_path = config.TABLES_DIR / "validation_correlations.csv"
    corr_df.to_csv(corr_path, index=False)
    print(f"\n[SAVED] {corr_path}")

    discrim_path = config.TABLES_DIR / "discriminant_matrix.csv"
    discrim_mat.to_csv(discrim_path)
    print(f"[SAVED] {discrim_path}")

    summary_path = config.TABLES_DIR / "validation_summary.txt"
    with open(summary_path, "w") as f:
        f.write("VUCA Validation Summary\n")
        f.write("=" * 40 + "\n\n")
        f.write("Convergent Validity (Pearson r):\n")
        f.write(corr_df[["dimension", "target", "pearson_r", "pearson_p"]].to_string(index=False))
        f.write("\n\nDiscriminant Validity (Cross-correlation matrix):\n")
        f.write(discrim_mat.to_string())
        f.write("\n\nPhase 2 (not yet implemented): Granger causality against\n")
        f.write("  - USDA farm loan demand series\n")
        f.write("  - USDA/NASS machinery sales\n")
        f.write("  - Corn/soybean futures realized volatility\n")
    print(f"[SAVED] {summary_path}")

    print("\n[DONE] 04_validation.py complete.")
    print("  Next: python scripts/05_visualize.py")


if __name__ == "__main__":
    main()
