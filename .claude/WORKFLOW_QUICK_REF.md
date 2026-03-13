# Workflow Quick Reference — VUCA AEB Extension

**Model:** Contractor (you direct, Claude orchestrates)

---

## The Loop

```
Your instruction
    ↓
[PLAN] (if multi-file or unclear) → Show plan → Your approval
    ↓
[EXECUTE] Implement, verify, done
    ↓
[REPORT] Summary + what's ready
    ↓
Repeat
```

---

## I Ask You When

- **Design forks:** "Option A (12-mo rolling) vs. Option B (6-mo). Which?"
- **Data ambiguity:** "Word Cloud column unclear. Inspect manually?"
- **Scope question:** "Also add robustness check while here, or focus on X?"
- **External data:** "Granger tests need USDA loan series — proceed without or flag for Phase 2?"

---

## I Just Execute When

- Bug fix is obvious (wrong column index, off-by-one in rolling window)
- Verification (script runs, output shape correct, peaks at known events)
- Documentation (logs, commits)
- Plotting (per established figure standards)
- Standardization (z-score formula is fully specified)

---

## VUCA-Specific Checkpoints

Before any commit on analysis scripts, confirm:

- [ ] **Baseline period:** Z-scores use 2016–2019 mean/SD (not full-sample)
- [ ] **Column indices:** AEB = col 19, ICC = col 20, IFE = col 21 (0-indexed, header=None)
- [ ] **Monthly groupby:** groups by Year AND Month (not just Month)
- [ ] **Event lines annotated** in figures: 2016-11, 2018-03, 2019-05, 2020-03, 2022-03
- [ ] **LDA seed set:** `random_state=config.RANDOM_SEED` in all stochastic steps
- [ ] **Paths via config:** no hardcoded absolute paths in scripts
- [ ] **Output saved:** parquets to `output/`, figures to `output/figures/`

---

## Quality Gates (No Exceptions)

| Score | Action |
|-------|--------|
| >= 80 | Ready to commit |
| < 80  | Fix blocking issues |

---

## Non-Negotiables

- `scripts/config.py` for DATA_ROOT — collaborators change one line
- `RANDOM_SEED = 42` — set in all stochastic code
- Z-score baseline: **2016–2019 only**
- Figures: white background, 300 DPI, PDF + PNG, colorblind-safe 4-color palette
- Tolerance: correlation checks pass if |r| within ±0.05 of expectation

---

## Pipeline Run Order

```bash
python scripts/00_load_data.py           # ALWAYS first — creates parquets
python scripts/01_quant_vuca.py          # Needs 00 output
python scripts/02_text_vuca.py           # Needs 00 output (slow — LDA)
python scripts/03_combine_standardize.py # Needs 01 + 02 output
python scripts/04_validation.py          # Needs 03 output
python scripts/05_visualize.py           # Needs 03 output
```

---

## Exploration Mode

For experimental work, use the **Fast-Track** workflow:
- Work in `explorations/` folder
- 60/100 quality threshold (vs. 80/100 for production)
- No plan needed — just a research value check (2 min)
- See `.claude/rules/exploration-fast-track.md`

---

## Data Source Reminders

| Data | Location |
|------|----------|
| AEB individual responses | `config.AEB_FILE` → `historical aeb data - malone.xlsx` |
| Word Cloud monthly files | `config.WORD_CLOUD_DIR` → `Word Cloud Data/YYYY/word cloud - YY-MM.xlsx` |
| Cleaned monthly AEB | `output/aeb_monthly.parquet` |
| Cleaned text monthly | `output/text_monthly.parquet` |
| Final VUCA scores | `output/vuca_monthly.parquet` |

---

## Next Step

You provide task → I plan (if needed) → Your approval → Execute → Done.
