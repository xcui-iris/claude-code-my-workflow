# Plan: VUCA Project — Workflow Configuration + Full Analysis Pipeline
**Date:** 2026-03-13
**Status:** IMPLEMENTED
**Project:** Measuring VUCA in U.S. Agriculture (Ag Economy Barometer)

---

## Summary

Built out the complete VUCA analysis workflow from scratch, adapting the academic Beamer/R template for a Python-based applied economics project at Purdue.

---

## Part A: Workflow Configuration — COMPLETED

| File | Action | Notes |
|------|--------|-------|
| `CLAUDE.md` | Updated | Replaced all brackets; added AEB column map, VUCA formula table, event annotations |
| `.claude/agents/domain-reviewer.md` | Updated | Customized for ag econ + VUCA; 5 lenses per method spec |
| `.claude/WORKFLOW_QUICK_REF.md` | Updated | Python commands, VUCA checkpoints, data source table |
| `requirements.txt` | Created | pandas, numpy, scipy, statsmodels, sklearn, gensim, nltk, textblob, matplotlib, seaborn |

---

## Part B: Analysis Pipeline — IMPLEMENTED

| Script | Status | Key outputs |
|--------|--------|-------------|
| `scripts/config.py` | Done | DATA_ROOT, column indices, baseline, event dates, colors |
| `scripts/dictionaries.py` | Done | EPU words, ag uncertainty words, ambiguity phrases, polarity word lists |
| `scripts/00_load_data.py` | Done | `aeb_monthly.parquet`, `text_monthly.parquet` |
| `scripts/01_quant_vuca.py` | Done | V_quant, U_quant, A_kurtosis, A_bimodality, A_signflip, C_fallback |
| `scripts/02_text_vuca.py` | Done | V_text, U_text, C_text, C_quant (LDA-based), A_polarity_conflict, A_phrase_rate |
| `scripts/03_combine_standardize.py` | Done | `vuca_monthly.parquet` with V/U/C/A scores (z-scored, 2016–2019 baseline) |
| `scripts/04_validation.py` | Done | Face, convergent, discriminant validity; robustness |
| `scripts/05_visualize.py` | Done | 5 publication figures (PDF + PNG, 300 DPI) |

---

## Open Issues

1. **Word Cloud text column** — `00_load_data.py` auto-selects by max string length; must be verified on first run
2. **diptest package** — Hartigan dip test requires `pip install diptest`; falls back to bimodality coefficient if missing
3. **Granger causality** — Predictive validity against external series (farm loans, machinery sales) is Phase 2
4. ~~**04_validation.py import bug**~~ — Fixed: dead `from scripts import config as cfg` removed

---

## Verification Steps

Run in order — each depends on the previous:

```bash
python scripts/00_load_data.py           # Verify: shape, date range, text column name
python scripts/01_quant_vuca.py          # Verify: spot-check peaks at COVID, trade war
python scripts/02_text_vuca.py           # Verify: U_text rate ~10–30%, LDA completes
python scripts/03_combine_standardize.py # Verify: baseline mean ≈ 0, SD ≈ 1
python scripts/04_validation.py          # Verify: U_score negatively correlated with AEB
python scripts/05_visualize.py           # Verify: event lines visible, COVID spike in V/U
```
