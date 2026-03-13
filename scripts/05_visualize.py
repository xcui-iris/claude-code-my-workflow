"""
05_visualize.py — VUCA AEB Extension
========================================
Generate publication-ready figures.

Inputs:
    output/vuca_monthly.parquet
    output/quant_measures.parquet

Outputs (PDF + PNG, 300 DPI):
    output/figures/fig1_aeb_vs_time.{pdf,png}
    output/figures/fig2_vuca_panel.{pdf,png}
    output/figures/fig3_subcomponents.{pdf,png}
    output/figures/fig4_correlation_heatmap.{pdf,png}
    output/figures/fig5_robustness.{pdf,png}

Standards:
    - White background, minimal grid
    - Colorblind-safe palette (Wong 2011): see config.VUCA_COLORS
    - 300 DPI
    - Event lines annotated

Usage:
    python scripts/05_visualize.py
"""

import sys
import pathlib
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import config

warnings.filterwarnings("ignore")

# ── Global style ──────────────────────────────────────────────────────────────

def apply_style():
    """Apply publication-ready matplotlib style."""
    plt.rcParams.update({
        "figure.dpi": 150,          # screen preview; save at 300
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": "#333333",
        "axes.grid": True,
        "grid.color": "#eeeeee",
        "grid.linewidth": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.family": "serif",
        "font.size": 10,
        "axes.labelsize": 10,
        "axes.titlesize": 11,
        "legend.fontsize": 9,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "lines.linewidth": 1.5,
    })


def add_event_lines(ax, alpha=0.35, label=True):
    """Add vertical event annotation lines to an axes."""
    colors = ["#888888"] * len(config.EVENT_DATES)
    for (date, lbl), color in zip(config.EVENT_DATES, colors):
        ax.axvline(date, color=color, linewidth=0.8, linestyle="--", alpha=alpha)
        if label:
            y_top = ax.get_ylim()[1]
            ax.text(
                date, y_top * 0.97, lbl,
                rotation=90, fontsize=7, color="#666666",
                ha="right", va="top"
            )


def save_figure(fig, name: str):
    """Save figure to PDF and PNG."""
    config.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    for fmt in config.FIGURE_FORMAT:
        path = config.FIGURES_DIR / f"{name}.{fmt}"
        fig.savefig(path, dpi=config.FIGURE_DPI, bbox_inches="tight")
        print(f"[SAVED] {path}")
    plt.close(fig)


# ── Figure 1: AEB time series ─────────────────────────────────────────────────

def fig1_aeb_time_series(vuca: pd.DataFrame):
    """Monthly AEB index over time with event annotations."""
    if "AEB_mean" not in vuca.columns:
        print("[FIG1] AEB_mean not in dataset — skipping")
        return

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(vuca.index, vuca["AEB_mean"], color="#2166ac", linewidth=1.5, label="Monthly AEB")
    ax.set_title("Purdue/CME Group Ag Economy Barometer — Monthly Mean", fontsize=11)
    ax.set_ylabel("AEB Index")
    ax.set_xlabel("")
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%Y"))
    add_event_lines(ax)
    ax.legend(loc="lower left")
    plt.tight_layout()
    save_figure(fig, "fig1_aeb_vs_time")


# ── Figure 2: VUCA panel ──────────────────────────────────────────────────────

def fig2_vuca_panel(vuca: pd.DataFrame):
    """2×2 panel of V, U, C, A scores over time."""
    dims = [
        ("V_score", "V — Volatility"),
        ("U_score", "U — Uncertainty"),
        ("C_score", "C — Complexity"),
        ("A_score", "A — Ambiguity"),
    ]
    available = [(col, lbl) for col, lbl in dims if col in vuca.columns]
    if not available:
        print("[FIG2] No VUCA scores found — skipping")
        return

    fig, axes = plt.subplots(2, 2, figsize=(11, 7), sharey=False)
    axes = axes.flatten()

    for i, (col, lbl) in enumerate(available):
        ax = axes[i]
        dim_key = col[0]  # 'V', 'U', 'C', 'A'
        color = config.VUCA_COLORS.get(dim_key, "#333333")
        series = vuca[col].dropna()
        ax.plot(series.index, series.values, color=color, linewidth=1.5)
        ax.axhline(0, color="#999999", linewidth=0.7, linestyle="-")
        ax.set_title(lbl)
        ax.set_ylabel("Z-score")
        add_event_lines(ax, alpha=0.3, label=(i == 0))

    for j in range(len(available), len(axes)):
        axes[j].set_visible(False)

    fig.suptitle("VUCA Dimensions — Ag Economy Barometer (2015–2024)", fontsize=12, y=1.01)
    plt.tight_layout()
    save_figure(fig, "fig2_vuca_panel")


# ── Figure 3: Quant vs text sub-measures ─────────────────────────────────────

def fig3_subcomponents(vuca: pd.DataFrame):
    """Overlay quant vs text sub-measures for each VUCA dimension.

    For C: falls back to C_fallback_z if LDA columns are all NaN.
    """
    # Determine C quant column: prefer LDA, fall back to C_fallback
    c_quant_col = "C_quant_lda_z"
    c_quant_label = "Quantitative (LDA)"
    if c_quant_col not in vuca.columns or vuca[c_quant_col].isna().all():
        c_quant_col = "C_fallback_z"
        c_quant_label = "Quantitative (fallback)"

    c_text_col = "C_text_z"
    c_text_label = "Text-based"
    if c_text_col not in vuca.columns or vuca[c_text_col].isna().all():
        c_text_col = None

    pairs = [
        ("V_quant_z", "V_text_z", "V — Volatility", "V", "Quantitative", "Text-based"),
        ("U_quant_z", "U_text_z", "U — Uncertainty", "U", "Quantitative", "Text-based"),
        (c_quant_col, c_text_col, "C — Complexity", "C", c_quant_label, c_text_label),
        ("A_quant_z", "A_text_z", "A — Ambiguity", "A", "Quantitative", "Text-based"),
    ]

    # Keep panel if at least one column has data
    available = [
        (q, t, lbl, k, ql, tl) for q, t, lbl, k, ql, tl in pairs
        if (q and q in vuca.columns and vuca[q].notna().any()) or
           (t and t in vuca.columns and vuca[t].notna().any())
    ]
    if not available:
        print("[FIG3] Sub-component columns not found — skipping")
        return

    fig, axes = plt.subplots(2, 2, figsize=(11, 7))
    axes = axes.flatten()

    for i, (q_col, t_col, lbl, dim_key, q_label, t_label) in enumerate(available):
        ax = axes[i]
        color = config.VUCA_COLORS.get(dim_key, "#333333")

        if q_col and q_col in vuca.columns and vuca[q_col].notna().any():
            ax.plot(vuca.index, vuca[q_col], color=color, linewidth=1.5,
                    label=q_label, alpha=0.9)
        if t_col and t_col in vuca.columns and vuca[t_col].notna().any():
            ax.plot(vuca.index, vuca[t_col], color=color, linewidth=1.5,
                    label=t_label, linestyle="--", alpha=0.7)

        ax.axhline(0, color="#999999", linewidth=0.7)
        ax.set_title(lbl)
        ax.set_ylabel("Z-score")
        add_event_lines(ax, alpha=0.25, label=False)
        if i == 0:
            ax.legend(loc="lower left", fontsize=8)

    for j in range(len(available), len(axes)):
        axes[j].set_visible(False)

    fig.suptitle("VUCA Sub-Measures: Quantitative vs Text-Based (Z-scored)", fontsize=12, y=1.01)
    plt.tight_layout()
    save_figure(fig, "fig3_subcomponents")


# ── Figure 4: Correlation heatmap ─────────────────────────────────────────────

def fig4_correlation_heatmap(vuca: pd.DataFrame):
    """Correlation matrix of V, U, C, A + AEB, IFE."""
    cols = ["V_score", "U_score", "C_score", "A_score", "AEB_mean"]
    for opt in ["IFE_mean", "ICC_mean"]:
        if opt in vuca.columns:
            cols.append(opt)

    available_cols = [c for c in cols if c in vuca.columns]
    joint = vuca[available_cols].dropna()

    if len(joint) < 10:
        print("[FIG4] Too few observations for correlation matrix — skipping")
        return

    corr = joint.corr(method="pearson")

    # Prettier labels
    label_map = {
        "V_score": "V (Volatility)", "U_score": "U (Uncertainty)",
        "C_score": "C (Complexity)", "A_score": "A (Ambiguity)",
        "AEB_mean": "AEB", "IFE_mean": "IFE", "ICC_mean": "ICC",
    }
    corr.index = [label_map.get(c, c) for c in corr.index]
    corr.columns = [label_map.get(c, c) for c in corr.columns]

    fig, ax = plt.subplots(figsize=(7, 6))
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    sns.heatmap(
        corr, ax=ax,
        annot=True, fmt=".2f", cmap="RdBu_r",
        vmin=-1, vmax=1, center=0,
        linewidths=0.5, linecolor="#dddddd",
        cbar_kws={"shrink": 0.8},
    )
    ax.set_title("VUCA Dimensions — Pearson Correlation Matrix", fontsize=11)
    plt.tight_layout()
    save_figure(fig, "fig4_correlation_heatmap")


# ── Figure 5: Robustness ──────────────────────────────────────────────────────

def fig5_robustness(vuca: pd.DataFrame, quant: pd.DataFrame):
    """Baseline V_quant (12-mo) vs 6-month rolling window robustness check."""
    aeb_mean = vuca["AEB_mean"] if "AEB_mean" in vuca.columns else None
    if aeb_mean is None:
        print("[FIG5] AEB_mean not found — skipping")
        return

    delta = aeb_mean.diff()
    v_6mo = delta.rolling(config.ROLLING_WINDOW_ROBUST, min_periods=3).std()
    v_12mo = quant["V_quant"] if "V_quant" in quant.columns else None

    fig, ax = plt.subplots(figsize=(9, 4))
    if v_12mo is not None:
        ax.plot(v_12mo.index, v_12mo.values, label="12-month window",
                color=config.VUCA_COLORS["V"], linewidth=1.5)
    ax.plot(v_6mo.index, v_6mo.values, label="6-month window (robustness)",
            color=config.VUCA_COLORS["V"], linewidth=1.2, linestyle="--", alpha=0.7)

    ax.set_title("V — Volatility: Baseline vs 6-Month Window (Robustness)", fontsize=11)
    ax.set_ylabel("Rolling SD of AEB Changes")
    add_event_lines(ax, alpha=0.3, label=True)
    ax.legend()
    plt.tight_layout()
    save_figure(fig, "fig5_robustness")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("05_visualize.py — Publication Figures")
    print("=" * 60)

    for fpath in [config.VUCA_MONTHLY_FILE]:
        if not fpath.exists():
            raise FileNotFoundError(
                f"Required input missing: {fpath}\n"
                "Run 03_combine_standardize.py first."
            )

    apply_style()

    vuca = pd.read_parquet(config.VUCA_MONTHLY_FILE)
    quant = (
        pd.read_parquet(config.QUANT_MEASURES_FILE)
        if config.QUANT_MEASURES_FILE.exists() else pd.DataFrame()
    )

    print(f"\n[INPUT] VUCA monthly: {vuca.shape}")
    print(f"[INPUT] Date range: {vuca.index[0]} → {vuca.index[-1]}")

    print("\n--- Figure 1: AEB time series ---")
    fig1_aeb_time_series(vuca)

    print("\n--- Figure 2: VUCA 2×2 panel ---")
    fig2_vuca_panel(vuca)

    print("\n--- Figure 3: Sub-components ---")
    fig3_subcomponents(vuca)

    print("\n--- Figure 4: Correlation heatmap ---")
    fig4_correlation_heatmap(vuca)

    print("\n--- Figure 5: Robustness ---")
    fig5_robustness(vuca, quant)

    print(f"\n[DONE] All figures saved to {config.FIGURES_DIR}")
    print("  Review figures before committing. Check:")
    print("  - Event lines visible and correctly dated")
    print("  - Axes labeled with units")
    print("  - COVID (2020-03) and trade war (2019-05) spikes visible in V and U")


if __name__ == "__main__":
    main()
