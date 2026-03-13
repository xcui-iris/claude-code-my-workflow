# CLAUDE.MD — VUCA Agricultural Sentiment (AEB Extension)

**Project:** VUCA Agricultural Sentiment — AEB Extension
**Institution:** Purdue University
**Branch:** main

---

## Core Principles

- **Plan first** — enter plan mode before non-trivial tasks; save plans to `quality_reports/plans/`
- **Verify after** — run the relevant script and confirm output at the end of every task
- **Single source of truth** — `scripts/` is authoritative; `output/` derives from it
- **Quality gates** — nothing ships below 80/100
- **Baseline period** — all z-scores use 2016–2019 as baseline (documented in VUCA_method.docx)
- **[LEARN] tags** — when corrected, save `[LEARN:category] wrong → right` to MEMORY.md

---

## Domain Context

### AEB Survey Structure
The Ag Economy Barometer (AEB) is a monthly survey of ~400 U.S. farmers.

**Individual-level data** (`historical aeb data - malone.xlsx`, sheet "Data", header=None):
| Col | Name | Description |
|-----|------|-------------|
| 0 | Month | 1–12 |
| 1 | Year | 2015–2024 |
| 2–8 | Q1–Q5_raw | Raw question responses |
| 9–15 | Q1–Q5_idx | Indexed question values |
| 16 | AEB_raw | Raw AEB composite |
| 17 | ICC_raw | Raw Current Conditions index |
| 18 | IFE_raw | Raw Future Expectations index |
| 19 | AEB | AEB index (col T in method docs) |
| 20 | ICC | Current Conditions index |
| 21 | IFE | Index of Future Expectations |

**Text data** (`Word Cloud Data/YYYY/word cloud - YY-MM.xlsx`): monthly open-ended responses, ~108 files 2015–2024. Column structure confirmed on first load.

### VUCA Formula Reference
| Dimension | Quant measure | Text measure |
|-----------|--------------|--------------|
| V — Volatility | Rolling 12-mo SD of monthly AEB changes | Jaccard distance of top-20 tokens month-to-month |
| U — Uncertainty | Cross-sectional variance of individual future expectations | % responses with EPU/ag-specific uncertainty words |
| C — Complexity | Inverse PC1 variance share over rolling LDA topic vectors | Mean response topic entropy + unique concept count |
| A — Ambiguity | Kurtosis + Hartigan dip p-value + skewness sign-flip count | Polarity conflict rate + ambiguity phrase rate |

All sub-measures z-scored over 2016–2019 baseline before combining. Equal-weight average of quant_z and text_z within each dimension.

### Key Event Annotations
| Date | Event |
|------|-------|
| 2016-11 | U.S. Presidential Election |
| 2018-03 | Tariff announcements begin |
| 2019-05 | U.S.–China trade war escalation |
| 2020-03 | COVID-19 pandemic onset |
| 2022-03 | Federal Reserve rate hikes begin |

---

## Folder Structure

```
my-project/
├── CLAUDE.md                        # This file
├── .claude/                         # Rules, skills, agents, hooks
├── Bibliography_base.bib            # Centralized bibliography
├── data/
│   └── README.md                    # Source paths, column maps (no data files)
├── scripts/
│   ├── config.py                    # DATA_ROOT and output paths — edit here for your machine
│   ├── dictionaries.py              # EPU/ag uncertainty word lists, ambiguity phrases
│   ├── 00_load_data.py              # Load AEB + Word Cloud; validate; save parquets
│   ├── 01_quant_vuca.py             # Quantitative V, U, C (fallback), A measures
│   ├── 02_text_vuca.py              # Text V, U, C (LDA), A measures
│   ├── 03_combine_standardize.py    # Z-score + combine → vuca_monthly.parquet
│   ├── 04_validation.py             # Face / convergent / discriminant / predictive validity
│   └── 05_visualize.py              # Publication-ready figures
├── output/
│   ├── tables/                      # CSV summary tables
│   └── figures/                     # PDF + PNG figures (300 DPI)
├── requirements.txt                 # Python dependencies
├── quality_reports/
│   ├── plans/                       # Approved implementation plans
│   ├── specs/                       # Requirements specs
│   └── session_logs/                # Session logs
├── explorations/                    # Research sandbox
│   └── ARCHIVE/
└── master_supporting_docs/          # VUCA_method.docx, background papers
```

---

## Commands

```bash
# Load and validate data (ALWAYS run first)
python scripts/00_load_data.py

# Quantitative VUCA measures
python scripts/01_quant_vuca.py

# Text-based VUCA measures (slow — LDA)
python scripts/02_text_vuca.py

# Standardize and combine
python scripts/03_combine_standardize.py

# Validation checks + correlation table
python scripts/04_validation.py

# Publication figures
python scripts/05_visualize.py

# Install dependencies
pip install -r requirements.txt
```

---

## Quality Thresholds

| Score | Gate | Meaning |
|-------|------|---------|
| 80 | Commit | Good enough to save |
| 90 | PR | Ready for deployment |
| 95 | Excellence | Aspirational |

---

## Non-Negotiables

- **Paths** — all data paths go through `scripts/config.py`; never hardcode absolute paths in analysis scripts
- **Baseline** — z-scores ALWAYS use 2016–2019 baseline period (not full-sample)
- **Figures** — 300 DPI, PDF + PNG, colorblind-safe palette, saved to `output/figures/`
- **Seed** — `RANDOM_SEED = 42` in `config.py`; set in all stochastic scripts (LDA, PCA)
- **No data in repo** — raw xlsx files stay at their original Windows paths; only parquet outputs go in `output/`

---

## Skills Quick Reference

| Command | What It Does |
|---------|-------------|
| `/proofread [file]` | Grammar/typo/academic writing review |
| `/review-paper [file]` | Manuscript review (structure, spec, citations) |
| `/lit-review [topic]` | Literature search + synthesis |
| `/data-analysis [dataset]` | End-to-end analysis workflow |
| `/commit [msg]` | Stage, commit, PR, merge |
| `/deep-audit` | Repository-wide consistency audit |
| `/context-status` | Show session health + context usage |

---

## N/A for This Project

The following template features are **not used** in this Python/applied-econ project:
- `beamer-quarto-sync` — no Beamer slides or Quarto decks
- `tikz-visual-quality` — no TikZ diagrams
- `no-pause-beamer` — no Beamer
- `r-code-conventions` — Python only; follow PEP 8 + numpy docstring style
- `/compile-latex`, `/deploy`, `/extract-tikz`, `/translate-to-quarto`, `/qa-quarto` — not applicable

---

## Current Project State

| Script | Status | Notes |
|--------|--------|-------|
| `00_load_data.py` | Ready | Inspect Word Cloud column on first run |
| `01_quant_vuca.py` | Ready | V, U, A quant measures |
| `02_text_vuca.py` | Ready | LDA-based C, text V/U/A |
| `03_combine_standardize.py` | Ready | Z-score + combine |
| `04_validation.py` | Ready | Internal validation; external Granger = Phase 2 |
| `05_visualize.py` | Ready | 5 publication figures |
