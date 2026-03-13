"""
config.py — VUCA AEB Extension
================================
Central configuration for all analysis scripts.

TO ADAPT FOR YOUR MACHINE:
  Change DATA_ROOT to the folder containing the AEB data files.
  Everything else is derived automatically.
"""

import pathlib

# ── 1. Data root ────────────────────────────────────────────────────────────
# All source data lives here. Change this one line for a different machine.
DATA_ROOT = pathlib.Path(r"C:\Users\cui205\Documents\CAB Lab\cluster 1\VUCA")

# ── 2. Source file paths ─────────────────────────────────────────────────────
AEB_FILE = DATA_ROOT / "historical aeb data - malone.xlsx"
AEB_SHEET = "Data"

WORD_CLOUD_DIR = DATA_ROOT / "Word Cloud Data"

# ── 3. Output paths ──────────────────────────────────────────────────────────
# These are relative to this project's my-project/ folder.
PROJECT_ROOT = pathlib.Path(__file__).parent.parent  # my-project/
OUTPUT_DIR = PROJECT_ROOT / "output"
TABLES_DIR = OUTPUT_DIR / "tables"
FIGURES_DIR = OUTPUT_DIR / "figures"

# Cleaned parquet files
AEB_MONTHLY_FILE = OUTPUT_DIR / "aeb_monthly.parquet"
TEXT_MONTHLY_FILE = OUTPUT_DIR / "text_monthly.parquet"
QUANT_MEASURES_FILE = OUTPUT_DIR / "quant_measures.parquet"
TEXT_MEASURES_FILE = OUTPUT_DIR / "text_measures.parquet"
VUCA_MONTHLY_FILE = OUTPUT_DIR / "vuca_monthly.parquet"

# ── 4. AEB column configuration ──────────────────────────────────────────────
# Column indices (0-based, header=None in source xlsx)
AEB_COL_MONTH = 0
AEB_COL_YEAR = 1
AEB_COL_Q2_IDX = 10   # Q2 indexed (future expectations component)
AEB_COL_Q3_IDX = 11   # Q3 indexed
AEB_COL_Q4_IDX = 12   # Q4 indexed
AEB_COL_AEB = 19      # AEB index (col T in method docs)
AEB_COL_ICC = 20      # Index of Current Conditions
AEB_COL_IFE = 21      # Index of Future Expectations

AEB_COLUMN_NAMES = {
    0: "Month", 1: "Year",
    2: "Q1_raw", 3: "Q2_raw", 4: "Q3_raw", 5: "Q4_raw", 6: "Q5_raw",
    7: "Q6_raw", 8: "Q7_raw",
    9: "Q1_idx", 10: "Q2_idx", 11: "Q3_idx", 12: "Q4_idx",
    13: "Q5_idx", 14: "Q6_idx", 15: "Q7_idx",
    16: "AEB_raw", 17: "ICC_raw", 18: "IFE_raw",
    19: "AEB", 20: "ICC", 21: "IFE",
}

# ── 5. Analysis parameters ───────────────────────────────────────────────────
# Baseline period for z-score standardization (per VUCA_method.docx)
BASELINE_YEARS = (2016, 2019)  # inclusive

# Rolling window sizes
ROLLING_WINDOW_V = 12   # months, for V_quant (SD of AEB changes)
ROLLING_WINDOW_ROBUST = 6  # months, for robustness check

# LDA parameters
LDA_N_TOPICS = 10
LDA_MAX_ITER = 50

# Reproducibility
RANDOM_SEED = 42

# Sparse month threshold (flag months with fewer responses)
MIN_RESPONSES_WARNING = 30
MIN_RESPONSES_DIP = 50  # Hartigan dip test unreliable below this

# ── 6. Key event dates for annotations ──────────────────────────────────────
import pandas as pd
EVENT_DATES = [
    (pd.Timestamp("2016-11-01"), "2016 Election"),
    (pd.Timestamp("2018-03-01"), "Tariffs Begin"),
    (pd.Timestamp("2019-05-01"), "Trade War Escalation"),
    (pd.Timestamp("2020-03-01"), "COVID-19"),
    (pd.Timestamp("2022-03-01"), "Fed Rate Hikes"),
]

# ── 7. Figure standards ──────────────────────────────────────────────────────
FIGURE_DPI = 300
FIGURE_FORMAT = ["pdf", "png"]

# Colorblind-safe palette (Wong 2011), one per VUCA dimension
VUCA_COLORS = {
    "V": "#E69F00",   # orange
    "U": "#56B4E9",   # sky blue
    "C": "#009E73",   # green
    "A": "#CC79A7",   # purple
}
