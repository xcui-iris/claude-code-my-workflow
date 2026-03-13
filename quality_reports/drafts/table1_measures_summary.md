# Table 1 — VUCA Sub-Measure Summary
**For paper:** Insert as Table 1 in Methods section (after standardization equation)

---

## Table 1. VUCA Sub-Measures: Construction and Data Sources

| Dimension | Sub-measure | Symbol | Formula / Method | Data source | Expected direction |
|-----------|-------------|--------|-----------------|-------------|-------------------|
| **V — Volatility** | Quantitative | $V_{\text{quant}}$ | Rolling 12-mo SD of $\Delta\overline{\text{AEB}}_t$ | AEB individual responses (col 19) | ↑ at shock events |
| | Text-based | $V_{\text{text}}$ | Jaccard distance of top-20 tokens, month $t$ vs $t-1$ | Word Cloud open-ended responses | ↑ at shock events |
| **U — Uncertainty** | Quantitative | $U_{\text{quant}}$ | $-\overline{\text{IFE}}_t$ (inverted future expectations) | AEB col 21 (IFE index) | ↑ when farmers pessimistic |
| | Text-based | $U_{\text{text}}$ | % responses with ≥1 EPU/ag uncertainty word | Word Cloud + EPU dictionary | ↑ at policy shocks |
| **C — Complexity** | Quantitative | $C_{\text{quant}}$ | $1 - \lambda_1^{(t)}$: inverse PC1 share, rolling LDA topic PCA | LDA topic shares (pooled corpus) | ↑ when topic space multidimensional |
| | Text-based | $C_{\text{text}}$ | Mean Shannon entropy of per-response topic distributions | LDA ($K=10$) on Word Cloud corpus | ↑ when responses draw on diverse topics |
| **A — Ambiguity** | Quantitative | $A_{\text{quant}}$ | Mean of: excess kurtosis + Hartigan dip p-value + skewness sign-flip count | AEB individual responses (col 19) | ↑ when AEB distribution bimodal/unstable |
| | Text-based | $A_{\text{text}}$ | Mean of: polarity conflict rate + ambiguity phrase rate | Word Cloud + polarity/phrase dictionaries | ↑ when responses contain mixed signals |

**Notes:**
- All sub-measures are z-scored over a 2016–2019 baseline: $z_{it} = (x_{it} - \bar{x}_{i,\text{base}}) / \sigma_{i,\text{base}}$
- Final dimension score: $\text{VUCA}_{d,t} = \frac{1}{2}(z_{d,\text{quant},t} + z_{d,\text{text},t})$
- AEB column indices are 0-based; col 19 = AEB composite, col 20 = ICC, col 21 = IFE
- LDA fitted on pooled corpus of all monthly responses; topic shares extracted per-month with fixed random seed (42)
- Hartigan dip test excluded for months with $N < 50$ respondents
- EPU dictionary and agricultural uncertainty word list provided in supplementary materials

---

## Table 2. Descriptive Statistics — VUCA Dimension Scores

*(Values to be filled from output/vuca_monthly.parquet — run after pipeline)*

| | V_score | U_score | C_score | A_score |
|---|---------|---------|---------|---------|
| Full sample mean | 0.022 | −0.396 | 0.794 | −0.160 |
| Full sample SD | 0.812 | 0.850 | 0.968 | 0.449 |
| Baseline mean (2016–2019) | −0.007 | 0.000 | −0.000 | −0.000 |
| Baseline SD (2016–2019) | 0.787 | 0.772 | 0.687 | 0.517 |
| Min | −1.781 | −2.394 | −1.368 | −0.987 |
| Max | 2.055 | 1.764 | 2.513 | 1.525 |
| Observations | 122 | 123 | 120 | 123 |

---

## Table 3. Convergent Validity — Correlations with AEB

| VUCA Dimension | Pearson $r$ | $p$-value | Spearman $\rho$ | $p$-value |
|----------------|------------|-----------|----------------|-----------|
| V — Volatility | 0.346 | <0.001 | 0.338 | <0.001 |
| U — Uncertainty | −0.758 | <0.001 | −0.720 | <0.001 |
| C — Complexity | −0.069 | 0.456 | −0.097 | 0.290 |
| A — Ambiguity | −0.240 | 0.007 | −0.173 | 0.056 |

---

## Table 4. Discriminant Validity — Cross-Correlation Matrix

| | V | U | C | A |
|---|---|---|---|---|
| V — Volatility | 1.000 | | | |
| U — Uncertainty | −0.352 | 1.000 | | |
| C — Complexity | −0.122 | −0.418 | 1.000 | |
| A — Ambiguity | 0.139 | 0.365 | −0.277 | 1.000 |

---

## Table 5. Predictive Validity — Granger Causality Results

| VUCA → Outcome | Lag | F-stat | $p$-value | Sig. |
|----------------|-----|--------|-----------|------|
| V → Farmland prices | 1 | 5.227 | 0.024 | ** |
| V → Farmland prices | 2 | 3.448 | 0.035 | ** |
| V → Farmland prices | 3 | 3.458 | 0.019 | ** |
| V → Farmland prices | 4 | 2.761 | 0.032 | ** |
| U → Farmland prices | 1 | 3.250 | 0.074 | * |
| A → Loan volume | 2 | 3.549 | 0.032 | ** |
| A → Loan volume | 3 | 2.361 | 0.076 | * |
| A → Loan volume | 4 | 2.827 | 0.028 | ** |
| V → Equipment sales | 2 | 2.505 | 0.086 | * |

*Note: Only significant results shown (p < 0.10). All series transformed to stationarity prior to testing (ADF confirmed). External series: Creighton University Main Street Economy Survey. *** p<0.01, ** p<0.05, * p<0.10.*
