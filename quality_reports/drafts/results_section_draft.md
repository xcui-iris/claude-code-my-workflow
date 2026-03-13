# Results Section — DRAFT
**Target:** American Journal of Agricultural Economics (AJAE)
**Status:** Draft v2 — 2026-03-13 (citations filled; confirmed checks resolved)
**Note:** [CHECK] = verify against figures/tables before submission.

---

## 4. Results

### 4.1 Descriptive Patterns in VUCA Dimensions

Figure 1 presents the monthly AEB index over the full sample period (October 2015 through December 2024). The series exhibits clear cyclical variation, with sustained elevated sentiment during the 2017–2018 commodity price recovery, a sharp decline coinciding with the onset of the COVID-19 pandemic in March 2020, and a subsequent rebound driven by strong commodity prices in 2021–2022. These patterns provide a benchmark against which the VUCA dimension scores can be assessed.

Figure 2 presents the four VUCA dimension scores over the same period. Several features are noteworthy. First, the Volatility dimension (V) exhibits its two largest spikes during the May 2019 U.S.–China trade war escalation (+1.11 SD above baseline) and the March 2020 COVID-19 onset (+1.68 SD), consistent with the interpretation of these events as periods of rapid and large-scale change in the agricultural operating environment. Second, the Complexity dimension (C) rises sharply during the 2021–2022 period, reaching its clearest expression at the March 2022 Federal Reserve rate hiking cycle (+2.29 SD), reflecting the simultaneous pressures of commodity price surges, input cost inflation, and supply chain disruption that characterized the post-pandemic agricultural economy — a period in which farmers faced an unusually large number of distinct and interacting forces. Third, the Uncertainty dimension (U) tracks inversely with the AEB throughout the sample, consistent with the theoretical expectation that aggregate pessimism and forward-looking uncertainty move together. Fourth, the Ambiguity dimension (A) exhibits more muted variation, with the clearest signal appearing around the November 2016 presidential election (+0.51 SD) — a period in which farm policy expectations were genuinely unclear.

Table 1 reports descriptive statistics for all four VUCA dimension scores over the full sample and the 2016–2019 baseline period. By construction, baseline means are approximately zero and baseline standard deviations are approximately one for each dimension. Full-sample means depart from zero to the extent that the post-2019 period is systematically more or less turbulent than the baseline. Notably, the full-sample mean of C_score (+0.794 SD) indicates that complexity has been persistently above baseline since 2020, while U_score (−0.396 SD) reflects the fact that the trade war years included in the 2016–2019 baseline represent a period of elevated uncertainty relative to the broader sample average.

---

### 4.2 Validation Results

#### 4.2.1 Face Validity

Table 2 reports mean VUCA dimension scores in ±2 month windows around five major structural events. The Volatility dimension performs best on face validity grounds, registering above-baseline values at two of its strongest events: the 2019 trade war escalation (+1.11 SD) and the 2020 COVID-19 onset (+1.68 SD). The Complexity dimension shows its strongest face-valid response during the March 2022 Federal Reserve rate hiking cycle (+2.29 SD), consistent with the interpretation that rapidly rising input costs, land value uncertainty, and credit market tightening jointly increased the dimensionality of farm decision-making environments. Notably, the 2018 tariff announcement window shows Volatility below baseline (−1.66 SD), reflecting the lag between tariff policy announcements and realized sentiment disruption — the larger V response appears in 2019 when trade war escalation intensified.

The Uncertainty and Ambiguity dimensions show more modest event-window responses. For Uncertainty, this reflects in part the composition of the 2016–2019 baseline: because the trade war years (2018–2019) are included in the reference period, the baseline U level already embeds elevated uncertainty, and subsequent shocks must be unusually severe to register as positive deviations. The relatively muted Ambiguity signal likely reflects the difficulty of detecting mixed-signal environments from short-horizon text responses, a limitation we discuss in Section 5.

#### 4.2.2 Convergent Validity

Table 3 presents Pearson and Spearman correlations between each VUCA dimension score and the monthly mean AEB index. The Uncertainty dimension is strongly and negatively correlated with the AEB (Pearson $r = -0.758$, $p < 0.001$; Spearman $\rho = -0.720$, $p < 0.001$), indicating that months in which farmers express elevated uncertainty about the future are systematically months of lower overall agricultural sentiment. This result is robust to rank-based correlation and is consistent with the interpretation of inverted IFE as an aggregate uncertainty proxy.

The Ambiguity dimension also correlates negatively with the AEB ($r = -0.240$, $p = 0.007$), consistent with the theoretical expectation that ambiguous, mixed-signal environments are associated with reduced farm confidence. The Complexity dimension is approximately orthogonal to the AEB ($r = -0.069$, $p = 0.456$), which we interpret as reflecting the conceptual independence of complexity from aggregate sentiment: a complex environment is not necessarily a pessimistic one, as was evident during the commodity price boom of 2021 when AEB was elevated alongside high complexity.

The Volatility dimension is positively correlated with the AEB ($r = 0.346$, $p < 0.001$). This result, while initially counterintuitive, reflects a feature of agricultural commodity markets: periods of high price volatility often coincide with commodity price rallies, which are associated with elevated farm sentiment. The positive V–AEB correlation therefore captures the asymmetric nature of agricultural price volatility — upside volatility is welcomed by producers — rather than indicating a measurement failure.

#### 4.2.3 Discriminant Validity

Table 4 presents the cross-correlation matrix of the four VUCA dimension scores. All pairwise correlations are moderate ($|r| \leq 0.42$), and no pair exceeds the conventional threshold of 0.70 that would suggest construct overlap. The largest correlation is between Uncertainty and Complexity ($r = -0.418$), which is economically interpretable: periods of high uncertainty tend to be characterized by a single dominant narrative (e.g., COVID, trade war), reducing the dimensionality of farmer discourse and therefore reducing measured complexity. Conversely, moderate-uncertainty periods tend to feature a broader range of simultaneous concerns. These results support the conclusion that the four dimensions capture conceptually distinct aspects of agricultural turbulence.

#### 4.2.4 Predictive Validity

Table 5 reports Granger causality test results for each VUCA dimension score against three external agricultural economic indicators from the Creighton University Main Street Economy survey. Stationarity tests indicate that VUCA scores V, U, and A are stationary in levels, while C requires first-differencing; all three external series require first-differencing.

The Volatility dimension exhibits the strongest predictive content, Granger-causing farmland price changes at all four tested lag lengths (all $p < 0.05$). This result suggests that elevated sentiment volatility among farmers leads land market adjustments by one to four months, consistent with the interpretation that forward-looking land buyers and sellers respond to the informational content of volatility in farmer confidence surveys before farmland price indices reflect those adjustments.

The Ambiguity dimension Granger-causes farm loan volume changes at lags 2 and 4 ($p < 0.05$) and marginally at lag 3 ($p = 0.076$). This finding is economically plausible: when farmers face ambiguous signals about future conditions, they defer large capital commitments but may increase operating credit demand as a precautionary buffer, with credit market responses lagging the sentiment signal by approximately two months.

The Uncertainty dimension exhibits marginal Granger causality for farmland prices at lag 1 ($p = 0.074$), consistent with the idea that aggregate pessimism about the future has a near-term dampening effect on land market activity, though the effect dissipates at longer lags. Neither Complexity nor any VUCA dimension Granger-causes farm equipment sales at conventional significance levels, suggesting that equipment investment decisions respond to longer-horizon or different information sets than those captured by our monthly measures.

Taken together, the predictive validity results indicate that VUCA dimension scores contain economically meaningful leading information for agricultural financial markets, particularly land values and credit demand, beyond what is contained in those series' own histories.

---

### 4.3 Robustness

Figure 5 compares the baseline Volatility measure — computed using a 12-month rolling window — against an alternative 6-month window. The two series are positively correlated (Pearson $r = 0.746$, Spearman $\rho = 0.721$) but diverge meaningfully at several points in the sample, indicating that the window choice matters for the timing and amplitude of measured volatility spikes. The 12-month window is preferred in the main specification to filter seasonal variation in AEB responses; shorter windows may be preferred in applications where timeliness is prioritized over smoothing. Results based on the 6-month window are qualitatively similar and available upon request.

---

*[END OF RESULTS DRAFT]*

---

## Notes for revision

- ~~**[CHECK]** Face validity SD values~~ — **RESOLVED** ✓: V(2019)=+1.11SD, V(2020)=+1.68SD, C(2022)=+2.29SD, A(2016)=+0.51SD
- ~~**[CHECK]** Full-sample means~~ — **RESOLVED** ✓: C_score=+0.794, U_score=−0.396, V_score=+0.022, A_score=−0.160
- **[CHECK]** N < 50 months for dip test — `n_respondents` not in quant_measures.parquet; must pull from AEB individual data directly (run diagnostic from `01_quant_vuca.py`)
- **Table 1** — descriptive statistics table: generate from `output/vuca_monthly.parquet`
- **Table 2** — face validity event table: extract from `output/tables/validation_summary.txt`
- **Table 3** — convergent validity correlations: from `output/tables/validation_correlations.csv`
- **Table 4** — discriminant matrix: from `output/tables/discriminant_matrix.csv`
- **Table 5** — Granger results: from `output/tables/granger_results.csv`
- ~~**[CITE]** Granger (1969)~~ — filled ✓ (cited in-text in methods section)
- ~~**[CITE]** Sims (1980)~~ — filled ✓ (cited in-text in methods section)
- ~~**[CITE]** Goss and Natvig~~ — filled ✓ → Goss, E. and Natvig, B. (2023). Creighton University Rural Mainstreet Economy Survey. **[CHECK]** confirm exact year/format.
- **Figure references** — confirm figure numbers match `output/figures/` file names
