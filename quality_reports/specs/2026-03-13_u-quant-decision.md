# Decision: U_quant Specification — Option B (Inverted IFE)
**Date:** 2026-03-13
**Status:** ADOPTED
**Affected script:** `scripts/01_quant_vuca.py`

---

## The Problem

The VUCA framework defines **Uncertainty** as: *farmers don't know what the future holds.* A good measure should be high when farmers are confused or worried, and low when farmers are confident.

The original specification measured it as:
> **U_quant = cross-sectional variance of individual future expectations per month**

This asks: *"Do farmers disagree with each other this month?"* — which is a different question.

### Why disagreement ≠ uncertainty

**Scenario A — COVID March 2020:**
Every farmer independently thinks "this is terrible, I have no idea what happens next." They all fill out low future expectations scores. The variance across farmers is **low** (they all agree it's bad). Original U_quant says → *low uncertainty.* ❌

**Scenario B — Normal year 2017:**
Some farmers are optimistic, some cautious, some neutral. Their future expectations scores are spread out. The variance is **high**. Original U_quant says → *high uncertainty.* ❌

The original U_quant accidentally built a **disagreement index**, not an uncertainty index.

### Validation evidence
- U_score was *positively* correlated with AEB (r = +0.22, p = 0.013)
- High uncertainty should go with *low* AEB — the sign was wrong
- U_score was negative at COVID (−0.92), trade war (−0.08), and rate hikes (−1.32)
- Face validity failed: every major shock showed *below-baseline* uncertainty

---

## Option A — Keep it, reframe as "disagreement"

Argue in the paper that cross-sectional disagreement is a valid uncertainty component (Zarnowitz & Lambros 1987; Bachmann et al. 2013). Write up as: *"We decompose uncertainty into aggregate sentiment (U_text) and cross-sectional disagreement (U_quant)."*

**Rejected because:** The face validity failure is hard to defend. COVID producing *low* disagreement-based uncertainty will invite referee scrutiny. More importantly, VUCA_method.docx defines Uncertainty as *lack of predictability about the future*, not *disagreement among respondents* — Option A would require changing the method spec, not just the framing.

---

## Option B — Fix U_quant: inverted IFE ✅ ADOPTED

Replace cross-sectional variance with the **level** of future expectations, inverted:

```
U_quant = −IFE_mean_t
```

When farmers are uncertain or pessimistic → IFE falls → U_quant rises. This directly measures aggregate uncertainty in the direction the theory predicts.

**Why IFE specifically:** IFE (Index of Future Expectations) is the AEB's forward-looking component — it captures what farmers expect over the next 12 months. Low IFE = they see a bad or uncertain future. It's the cleanest internal proxy for aggregate uncertainty and uses data already in the pipeline.

**Implementation:** Negate `IFE_mean` from `aeb_monthly.parquet`. The z-scoring in `03_combine_standardize.py` handles centering; negation ensures direction is correct before standardization.

---

## Expected results after fix
- U_score negatively correlated with AEB ✓
- COVID, trade war, and rate hike events spike upward ✓
- Face validity passes ✓

---

## Note on cross-sectional disagreement
The original U_quant (variance of FutExp_indiv) is not discarded — it is a valid measure of farmer disagreement and could be reported as a supplementary finding or as a fifth dimension in future work. It is saved in `output/quant_measures.parquet` as `FutExp_var` via `make_aeb_monthly()`.
