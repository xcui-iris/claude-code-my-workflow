"""
06_var_irf.py — VUCA AEB Extension
====================================
VAR impulse-response functions for the significant Granger causality pairs.

Focus pairs (from 04b_granger_validation.py results):
  - V_score -> farmland_prices  (significant at all 4 lags, strongest result)
  - A_score -> loan_volume      (significant at lags 2 and 4)
  - U_score -> farmland_prices  (marginal at lag 1)

Method:
  1. Fit bivariate VAR for each pair with lag order selected by AIC (max 6).
  2. Compute orthogonalized IRFs over a 12-month horizon.
  3. Compute bootstrap confidence intervals (n=500 draws).
  4. Plot IRFs with 90% CI bands.

Inputs:
    output/vuca_monthly.parquet
    farmloan_equipmentsale_indices.xlsx  (at DATA_ROOT, via 04b loader)

Outputs:
    output/figures/fig6_irf_v_farmland.pdf/.png
    output/figures/fig6_irf_v_farmland.pdf/.png
    output/figures/fig7_irf_a_loans.pdf/.png
    output/tables/var_lag_selection.csv
    output/tables/irf_summary.txt

Usage:
    python scripts/06_var_irf.py
"""

import sys
import pathlib
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import config
# Re-use the Creighton data loader from 04b
from importlib import import_module
granger_mod = import_module("04b_granger_validation")
load_external_data = granger_mod.load_external_data
standardize_col_names = granger_mod.standardize_col_names

warnings.filterwarnings("ignore")

EXTERNAL_FILE = config.DATA_ROOT / "farmloan_equipmentsale_indices.xlsx"
IRF_HORIZON = 12      # months ahead
N_BOOTSTRAP = 500     # bootstrap draws for CI
CI_LEVEL = 0.90       # confidence interval width
MAX_LAG_SELECT = 6    # AIC search range
RANDOM_SEED = config.RANDOM_SEED

# Pairs to analyse: (vuca_col, external_col, figure_label, fig_suffix)
PAIRS = [
    ("V_score", "farmland_prices", "Volatility -> Farmland Prices", "v_farmland"),
    ("A_score", "loan_volume",     "Ambiguity -> Farm Loan Volume", "a_loans"),
    ("U_score", "farmland_prices", "Uncertainty -> Farmland Prices", "u_farmland"),
]


# ── Stationarity ──────────────────────────────────────────────────────────────

def make_stationary(series: pd.Series, name: str) -> pd.Series:
    """First-difference if ADF rejects stationarity; return transformed series."""
    s = series.dropna()
    p = adfuller(s, autolag="AIC")[1]
    if p >= 0.05:
        print(f"  {name}: non-stationary (ADF p={p:.3f}) — differencing")
        return series.diff()
    print(f"  {name}: stationary (ADF p={p:.3f})")
    return series


# ── VAR fitting ───────────────────────────────────────────────────────────────

def fit_var(y: pd.DataFrame, label: str) -> tuple:
    """
    Fit bivariate VAR with lag order selected by AIC.

    Parameters
    ----------
    y : DataFrame with two columns — [external_var, vuca_dim]
        (external first so the shock-of-interest is col 1)

    Returns
    -------
    results : VARResults
    selected_lag : int
    ic_table : DataFrame
    """
    model = VAR(y.dropna())
    ic_rows = []
    for p in range(1, MAX_LAG_SELECT + 1):
        try:
            r = model.fit(p, trend="c")
            ic_rows.append({"lag": p, "aic": r.aic, "bic": r.bic, "hqic": r.hqic})
        except Exception as e:
            print(f"    [lag {p}] fit failed: {e}")
            continue

    if not ic_rows:
        print(f"  [WARN] All lag fits failed for {label}; defaulting to lag=1")
        selected_lag = 1
        results = model.fit(1, trend="c")
        return results, selected_lag, pd.DataFrame()

    ic_table = pd.DataFrame(ic_rows)
    selected_lag = int(ic_table.loc[ic_table["aic"].idxmin(), "lag"])
    print(f"  {label}: VAR lag selected = {selected_lag} (AIC)")

    results = model.fit(selected_lag, trend="c")
    return results, selected_lag, ic_table


# ── IRF computation ───────────────────────────────────────────────────────────

def compute_irf(var_results, horizon: int) -> np.ndarray:
    """
    Compute orthogonalized IRF: response of col-0 (external) to
    a unit shock in col-1 (VUCA score).

    Returns array of shape (horizon+1,) with the IRF values.
    """
    irf_obj = var_results.irf(horizon)
    # orth_irfs shape: (horizon+1, n_vars, n_vars)
    # [h, response_var, shock_var]  ->  col-0 response to col-1 shock
    return irf_obj.orth_irfs[:, 0, 1]


def bootstrap_irf(y: pd.DataFrame, lag: int, horizon: int,
                  n_boot: int = N_BOOTSTRAP, seed: int = RANDOM_SEED) -> np.ndarray:
    """
    Parametric bootstrap for IRF confidence bands.
    Draws residuals from the fitted VAR and re-estimates n_boot times.

    Returns array of shape (n_boot, horizon+1).
    """
    rng = np.random.default_rng(seed)
    data = y.dropna().values  # (T, 2)
    T, k = data.shape

    # Fit once to get coefficient matrices and residuals
    model = VAR(data)
    res = model.fit(lag, trend="c")
    coefs = res.coefs            # (lag, k, k)
    intercept = res.intercept    # (k,)
    sigma = res.sigma_u          # (k, k) — residual covariance
    L = np.linalg.cholesky(sigma)  # for orthogonalisation

    boot_irfs = np.zeros((n_boot, horizon + 1))

    for b in range(n_boot):
        # Draw new residuals ~ N(0, sigma)
        eps = rng.multivariate_normal(np.zeros(k), sigma, size=T)

        # Simulate new data
        y_new = np.zeros_like(data)
        y_new[:lag] = data[:lag]
        for t in range(lag, T):
            y_hat = intercept.copy()
            for p in range(lag):
                y_hat += coefs[p] @ y_new[t - p - 1]
            y_new[t] = y_hat + eps[t]

        # Fit VAR to simulated data
        try:
            res_b = VAR(y_new).fit(lag, trend="c")
            irf_b = res_b.irf(horizon)
            boot_irfs[b] = irf_b.orth_irfs[:, 0, 1]
        except Exception:
            boot_irfs[b] = np.nan

    return boot_irfs


# ── Plotting ──────────────────────────────────────────────────────────────────

def plot_irf(
    irf_vals: np.ndarray,
    boot_irfs: np.ndarray,
    label: str,
    fig_suffix: str,
    vuca_col: str,
    ext_col: str,
) -> None:
    """
    Plot orthogonalized IRF with bootstrap confidence band.
    Saves PDF + PNG to output/figures/.
    """
    horizon = len(irf_vals) - 1
    periods = np.arange(horizon + 1)

    alpha = 1 - CI_LEVEL
    lo = np.nanpercentile(boot_irfs, 100 * alpha / 2, axis=0)
    hi = np.nanpercentile(boot_irfs, 100 * (1 - alpha / 2), axis=0)

    dim_key = vuca_col[0]  # "V", "U", "A", "C"
    color = config.VUCA_COLORS.get(dim_key, "#333333")

    fig, ax = plt.subplots(figsize=(7, 3.5))

    ax.fill_between(periods, lo, hi, color=color, alpha=0.18, label=f"{int(CI_LEVEL*100)}% CI")
    ax.plot(periods, irf_vals, color=color, lw=2.0, label="IRF (point estimate)")
    ax.axhline(0, color="black", lw=0.8, ls="--")

    # Mark first period where CI excludes zero (if any)
    for h in range(1, horizon + 1):
        if lo[h] > 0 or hi[h] < 0:
            ax.axvline(h, color=color, lw=0.6, ls=":", alpha=0.5)

    ax.set_xlabel("Months after shock", fontsize=10)
    ext_label = ext_col.replace("_", " ").title()
    ax.set_ylabel(f"Response: {ext_label}", fontsize=10)
    ax.set_title(f"IRF: {label}", fontsize=11, fontweight="bold")
    ax.xaxis.set_major_locator(mticker.MultipleLocator(2))
    ax.legend(fontsize=9, framealpha=0.9)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()

    config.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    for fmt in config.FIGURE_FORMAT:
        path = config.FIGURES_DIR / f"fig6_{fig_suffix}.{fmt}"
        fig.savefig(path, dpi=config.FIGURE_DPI, bbox_inches="tight")
        print(f"  [SAVED] {path}")
    plt.close(fig)


# ── Summary table ─────────────────────────────────────────────────────────────

def write_irf_summary(all_results: list, path: pathlib.Path) -> None:
    lines = [
        "VAR Impulse-Response Function Summary",
        "=" * 60,
        f"IRF horizon: {IRF_HORIZON} months",
        f"Bootstrap CI: {int(CI_LEVEL*100)}%,  n_boot={N_BOOTSTRAP}",
        "",
        "For each pair: peak IRF, period of peak, and whether the",
        f"{int(CI_LEVEL*100)}% CI excludes zero at any horizon.",
        "",
    ]
    for r in all_results:
        lines.append(f"Pair: {r['label']}")
        lines.append(f"  VAR lag order: {r['lag']}")
        lines.append(f"  Peak IRF: {r['peak_val']:.4f} at month {r['peak_h']}")
        lines.append(f"  CI excludes zero at months: {r['sig_months']}")
        lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[SAVED] {path}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("06_var_irf.py — VAR Impulse-Response Functions")
    print("=" * 60)

    if not EXTERNAL_FILE.exists():
        raise FileNotFoundError(f"External data not found: {EXTERNAL_FILE}")
    if not config.VUCA_MONTHLY_FILE.exists():
        raise FileNotFoundError("Run 03_combine_standardize.py first.")

    # Load data
    external = standardize_col_names(load_external_data(EXTERNAL_FILE))
    vuca = pd.read_parquet(config.VUCA_MONTHLY_FILE)
    vuca.index = pd.to_datetime(vuca.index)
    external.index = pd.to_datetime(external.index)

    # Lag selection table accumulator
    all_ic = []
    all_irf_results = []

    for vuca_col, ext_col, label, fig_suffix in PAIRS:
        print(f"\n{'-'*50}")
        print(f"Pair: {label}")

        if ext_col not in external.columns:
            print(f"  [SKIP] '{ext_col}' not found in external data.")
            continue

        # Align and stationarize
        combined = vuca[[vuca_col]].join(external[[ext_col]], how="inner").dropna()
        print(f"  Aligned sample: {len(combined)} months "
              f"({combined.index[0].strftime('%Y-%m')} -> {combined.index[-1].strftime('%Y-%m')})")

        print("  Stationarity:")
        v_stat = make_stationary(combined[vuca_col], vuca_col)
        e_stat = make_stationary(combined[ext_col], ext_col)

        # Stack with external first (so shock = col-1 = VUCA)
        pair_df = pd.DataFrame({ext_col: e_stat, vuca_col: v_stat}).dropna()

        # Fit VAR
        var_res, lag, ic_table = fit_var(pair_df, label)
        ic_table["pair"] = label
        all_ic.append(ic_table)

        # IRF
        irf_vals = compute_irf(var_res, IRF_HORIZON)

        # Bootstrap CI
        print(f"  Computing bootstrap CI ({N_BOOTSTRAP} draws)...")
        boot_irfs = bootstrap_irf(pair_df, lag, IRF_HORIZON)

        # Identify months where CI excludes zero
        alpha = 1 - CI_LEVEL
        lo = np.nanpercentile(boot_irfs, 100 * alpha / 2, axis=0)
        hi = np.nanpercentile(boot_irfs, 100 * (1 - alpha / 2), axis=0)
        sig_months = [h for h in range(1, IRF_HORIZON + 1) if lo[h] > 0 or hi[h] < 0]
        peak_h = int(np.argmax(np.abs(irf_vals)))
        peak_val = irf_vals[peak_h]

        print(f"  Peak IRF: {peak_val:.4f} at month {peak_h}")
        print(f"  CI excludes zero at: {sig_months if sig_months else 'none'}")

        all_irf_results.append({
            "label": label,
            "lag": lag,
            "peak_val": peak_val,
            "peak_h": peak_h,
            "sig_months": sig_months,
        })

        # Plot
        plot_irf(irf_vals, boot_irfs, label, fig_suffix, vuca_col, ext_col)

    # Save lag selection table
    if all_ic:
        ic_all = pd.concat(all_ic, ignore_index=True)
        ic_path = config.TABLES_DIR / "var_lag_selection.csv"
        ic_all.to_csv(ic_path, index=False)
        print(f"\n[SAVED] {ic_path}")

    # Save IRF summary
    write_irf_summary(all_irf_results, config.TABLES_DIR / "irf_summary.txt")

    print("\n[DONE] 06_var_irf.py complete.")
    print(f"Figures saved to: {config.FIGURES_DIR}")


if __name__ == "__main__":
    main()
