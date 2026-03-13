"""
00_load_data.py — VUCA AEB Extension
======================================
Load and validate AEB survey data and Word Cloud text data.
Outputs two cleaned parquet files for downstream scripts.

Usage:
    python scripts/00_load_data.py

Outputs:
    output/aeb_monthly.parquet   — monthly AEB aggregates
    output/text_monthly.parquet  — monthly text response lists
"""

import sys
import pathlib
import warnings
import pandas as pd
import numpy as np

# Add scripts/ to path so config is importable from any working directory
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import config

warnings.filterwarnings("ignore", category=UserWarning)


# ── 1. Load AEB individual-response data ────────────────────────────────────

def load_aeb(path: pathlib.Path) -> pd.DataFrame:
    """Load AEB xlsx, assign column names, basic validation."""
    print(f"\n[AEB] Loading: {path}")
    if not path.exists():
        raise FileNotFoundError(f"AEB file not found: {path}")

    df = pd.read_excel(path, sheet_name=config.AEB_SHEET, header=None)
    print(f"[AEB] Raw shape: {df.shape}")

    # Rename known columns; leave extras as integers
    rename = {k: v for k, v in config.AEB_COLUMN_NAMES.items() if k < df.shape[1]}
    df = df.rename(columns=rename)

    # Type coercion
    for col in ["Month", "Year"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in ["AEB", "ICC", "IFE", "Q2_idx", "Q3_idx", "Q4_idx"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows missing Year or Month
    before = len(df)
    df = df.dropna(subset=["Year", "Month"])
    dropped = before - len(df)
    if dropped:
        print(f"[AEB] Dropped {dropped} rows with missing Year/Month")

    df["Year"] = df["Year"].astype(int)
    df["Month"] = df["Month"].astype(int)

    # Convert 2-digit years (e.g. 15 → 2015)
    df["Year"] = df["Year"].apply(lambda y: y + 2000 if y < 100 else y)

    # Date range
    date_min = f"{df['Year'].min()}-{df['Month'].min():02d}"
    date_max = f"{df['Year'].max()}-{df['Month'].max():02d}"
    print(f"[AEB] Date range: {date_min} → {date_max}")
    print(f"[AEB] Unique year-months: {df.groupby(['Year','Month']).ngroups}")
    print(f"[AEB] AEB col — mean: {df['AEB'].mean():.1f}, SD: {df['AEB'].std():.1f}, "
          f"min: {df['AEB'].min():.1f}, max: {df['AEB'].max():.1f}")

    return df


def make_aeb_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate individual responses to monthly panel."""
    # Individual future expectations = mean of Q2, Q3, Q4 indexed per respondent
    df["FutExp_indiv"] = df[["Q2_idx", "Q3_idx", "Q4_idx"]].mean(axis=1)

    monthly = (
        df.groupby(["Year", "Month"])
        .agg(
            AEB_mean=("AEB", "mean"),
            AEB_var=("AEB", "var"),
            AEB_n=("AEB", "count"),
            ICC_mean=("ICC", "mean"),
            IFE_mean=("IFE", "mean"),
            IFE_var=("IFE", "var"),
            FutExp_var=("FutExp_indiv", "var"),   # cross-sectional var for U_quant
        )
        .reset_index()
        .sort_values(["Year", "Month"])
        .reset_index(drop=True)
    )

    # Add a proper date index
    monthly["Date"] = pd.to_datetime(
        monthly["Year"].astype(str) + "-" + monthly["Month"].astype(str).str.zfill(2)
    )
    monthly = monthly.set_index("Date")

    print(f"\n[AEB Monthly] Shape: {monthly.shape}")
    print(f"[AEB Monthly] N respondents/month — mean: {monthly['AEB_n'].mean():.0f}, "
          f"min: {monthly['AEB_n'].min()}, max: {monthly['AEB_n'].max()}")

    # Flag sparse months
    sparse = monthly[monthly["AEB_n"] < config.MIN_RESPONSES_WARNING]
    if len(sparse):
        print(f"[AEB Monthly] WARNING: {len(sparse)} months with N < {config.MIN_RESPONSES_WARNING}:")
        print(sparse[["Year", "Month", "AEB_n"]].to_string())

    return monthly


# ── 2. Load Word Cloud text data ─────────────────────────────────────────────

def discover_word_cloud_files(wc_dir: pathlib.Path) -> list[pathlib.Path]:
    """Recursively find all word cloud xlsx files."""
    files = sorted(wc_dir.rglob("word cloud - *.xlsx"))
    print(f"\n[TEXT] Found {len(files)} word cloud files in {wc_dir}")
    return files


def inspect_word_cloud_file(path: pathlib.Path) -> pd.DataFrame:
    """Load one file and print its structure for column identification."""
    df = pd.read_excel(path, header=None, nrows=6)
    print(f"\n[TEXT] Inspecting: {path.name}")
    print(f"  Columns ({len(df.columns)}): {list(df.columns)}")
    print(df.to_string())
    return df


def parse_year_month_from_filename(path: pathlib.Path) -> tuple[int, int]:
    """Extract year and month from filename: 'word cloud - YY-MM.xlsx'"""
    stem = path.stem  # 'word cloud - YY-MM'
    ym_part = stem.split(" - ")[-1]  # 'YY-MM'
    yy, mm = ym_part.split("-")
    year = 2000 + int(yy)
    month = int(mm)
    return year, month


def load_word_cloud_file(path: pathlib.Path, text_col: int) -> pd.DataFrame:
    """Load one monthly word cloud file, return rows with (Year, Month, text).

    text_col is a 0-based integer column index (files have no header row).
    """
    year, month = parse_year_month_from_filename(path)
    try:
        df = pd.read_excel(path, header=None)
        if text_col >= df.shape[1]:
            actual_col = 0
        else:
            actual_col = text_col
        texts = df[actual_col].dropna().astype(str).tolist()
        return pd.DataFrame({"Year": year, "Month": month, "text": texts})
    except Exception as e:
        print(f"[TEXT] WARNING: Could not load {path.name}: {e}")
        return pd.DataFrame(columns=["Year", "Month", "text"])


def make_text_monthly(wc_dir: pathlib.Path) -> pd.DataFrame:
    """Load all word cloud files and aggregate to monthly text lists."""
    files = discover_word_cloud_files(wc_dir)
    if not files:
        raise FileNotFoundError(f"No word cloud files found in {wc_dir}")

    # Inspect first file to determine text column (header=None → integer columns)
    sample = inspect_word_cloud_file(files[0])
    # Heuristic: pick the column with the longest average string length
    str_cols = [c for c in sample.columns if sample[c].dtype == object]
    if not str_cols:
        text_col = 0
    else:
        avg_len = {c: sample[c].astype(str).str.len().mean() for c in str_cols}
        text_col = max(avg_len, key=avg_len.get)  # integer column index

    print(f"\n[TEXT] Auto-selected text column index: {text_col}")
    print(f"       First few values: {sample[text_col].dropna().astype(str).tolist()[:3]}")
    print("       >>> Verify these look like farmer text responses <<<")

    # Load all files
    dfs = []
    for f in files:
        dfs.append(load_word_cloud_file(f, text_col))
    raw = pd.concat(dfs, ignore_index=True)

    print(f"\n[TEXT] Total individual text responses: {len(raw)}")

    # Aggregate to monthly: keep list of texts + count
    monthly = (
        raw.groupby(["Year", "Month"])["text"]
        .agg(list)
        .reset_index()
        .rename(columns={"text": "responses"})
    )
    monthly["n_responses"] = monthly["responses"].apply(len)
    monthly["Date"] = pd.to_datetime(
        monthly["Year"].astype(str) + "-" + monthly["Month"].astype(str).str.zfill(2)
    )
    monthly = monthly.sort_values("Date").set_index("Date")

    print(f"[TEXT Monthly] Shape: {monthly.shape}")
    print(f"[TEXT Monthly] N responses/month — mean: {monthly['n_responses'].mean():.0f}, "
          f"min: {monthly['n_responses'].min()}, max: {monthly['n_responses'].max()}")

    # Sparse month warning
    sparse = monthly[monthly["n_responses"] < config.MIN_RESPONSES_WARNING]
    if len(sparse):
        print(f"[TEXT Monthly] WARNING: {len(sparse)} months with N < {config.MIN_RESPONSES_WARNING}")

    return monthly


# ── 3. Validate AEB reconstruction ───────────────────────────────────────────

def validate_aeb_reconstruction(aeb_df: pd.DataFrame) -> None:
    """
    Check that the monthly mean of AEB (col 19) is consistent with
    official published AEB values (if available).
    This is a diagnostic only — no hard failure.
    """
    print("\n[VALIDATE] AEB mean by year (sanity check):")
    by_year = aeb_df.groupby("Year")["AEB"].mean().round(1)
    print(by_year.to_string())
    print("  (Expected range ~80–130; COVID drop ~2020; trade war dip ~2018–2019)")


# ── 4. Main ──────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("00_load_data.py — VUCA AEB Extension")
    print("=" * 60)

    # Ensure output directory exists
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # -- AEB --
    aeb_raw = load_aeb(config.AEB_FILE)
    aeb_monthly = make_aeb_monthly(aeb_raw)
    validate_aeb_reconstruction(aeb_raw)

    # Save
    aeb_monthly.to_parquet(config.AEB_MONTHLY_FILE)
    print(f"\n[SAVED] {config.AEB_MONTHLY_FILE}")

    # -- Text --
    text_monthly = make_text_monthly(config.WORD_CLOUD_DIR)

    # Parquet can't store lists natively — serialize to string for storage
    # Downstream scripts will eval() or use the raw strings
    text_save = text_monthly.copy()
    text_save["responses"] = text_save["responses"].apply(lambda x: "\x00".join(x))
    text_save.to_parquet(config.TEXT_MONTHLY_FILE)
    print(f"[SAVED] {config.TEXT_MONTHLY_FILE}")

    print("\n[DONE] 00_load_data.py complete.")
    print("  Next: python scripts/01_quant_vuca.py")


if __name__ == "__main__":
    main()
