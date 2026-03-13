# Methods Section — DRAFT
**Target:** American Journal of Agricultural Economics (AJAE)
**Status:** Draft v2 — 2026-03-13 (citations filled)
**Note:** [CHECK] tags mark facts to verify against paper data.

---

## 3. Data and Methods

### 3.1 Data

#### 3.1.1 Ag Economy Barometer Survey

We use individual-level microdata from the Purdue University/CME Group Ag Economy Barometer (AEB), a monthly survey of U.S. agricultural producers conducted since October 2015 (Mintert and Widmar, 2016). The survey samples approximately 400 farmers and farm operators each month, with respondents drawn from a national panel of agricultural producers with annual gross sales of at least $500,000. The survey is designed to capture sentiment about current and future farm business conditions and is fielded during the first two weeks of each month.

Our analytical sample spans [CHECK: October 2015 through December 2024], comprising [CHECK: 123] monthly waves and [CHECK: 49,340] individual survey responses. The core outcome measures are the AEB index, the Index of Current Conditions (ICC), and the Index of Future Expectations (IFE). Each index is constructed from a subset of five survey questions using a diffusion index methodology analogous to the University of Michigan's Index of Consumer Sentiment (Curtin, 2007). The AEB is a composite of the ICC and IFE, with the IFE receiving greater weight to reflect the forward-looking orientation of the barometer.

In addition to the structured survey questions, a subset of respondents provide open-ended text responses to a prompt asking them to describe current conditions affecting their farm operation. These responses are archived as monthly word cloud files and constitute the text-based component of our VUCA measures. Our text corpus contains [CHECK: approximately 47,668] individual responses pooled across the full sample period.

---

### 3.2 Measuring VUCA in Agricultural Sentiment

The VUCA framework — originally developed in military strategic planning and subsequently adopted in organizational and management research (Bennett and Lemoine, 2014) — decomposes environmental turbulence into four conceptually distinct dimensions: Volatility (magnitude and speed of change), Uncertainty (lack of predictability), Complexity (multiplicity of forces), and Ambiguity (unclear causal relationships). We operationalize each dimension using two complementary sub-measures: a quantitative measure derived from the structured survey indices and a text-based measure derived from the open-ended responses. The two sub-measures are standardized and combined into a single monthly score for each dimension.

#### 3.2.1 Standardization

To ensure comparability across dimensions and interpretability relative to a stable reference period, we z-score each sub-measure against a pre-shock baseline window of January 2016 through December 2019:

$$z_{it} = \frac{x_{it} - \bar{x}_{i,\text{base}}}{\sigma_{i,\text{base}}}$$

where $\bar{x}_{i,\text{base}}$ and $\sigma_{i,\text{base}}$ are the mean and standard deviation of sub-measure $i$ computed over the baseline period. The 2016–2019 window captures a period of normal cyclical variation in agricultural sentiment prior to the major structural disruptions of the COVID-19 pandemic and the post-pandemic inflation cycle. The trade war years (2018–2019) are deliberately included in the baseline to anchor uncertainty at a level that reflects ongoing policy risk rather than an artificially tranquil pre-tariff period.

The final dimension score is the equal-weight average of the standardized quantitative and text sub-measures:

$$\text{VUCA}_{d,t} = \frac{1}{2}\left(z_{d,\text{quant},t} + z_{d,\text{text},t}\right)$$

where $d \in \{V, U, C, A\}$.

---

#### 3.2.2 Volatility

Volatility captures the magnitude and speed of change in aggregate farmer sentiment. Our quantitative measure ($V_{\text{quant}}$) is the rolling 12-month standard deviation of first differences in the monthly AEB mean:

$$V_{\text{quant},t} = \text{SD}\left(\Delta\overline{\text{AEB}}_{t-11}, \ldots, \Delta\overline{\text{AEB}}_{t}\right)$$

where $\Delta\overline{\text{AEB}}_t = \overline{\text{AEB}}_t - \overline{\text{AEB}}_{t-1}$ is the monthly change in the cross-sectional mean AEB index. A 12-month window is chosen to filter seasonal variation while remaining responsive to structural shifts; we report a 6-month window as a robustness check.

Our text-based volatility measure ($V_{\text{text}}$) captures turnover in the vocabulary of farmer concerns month to month. We compute the Jaccard distance between the sets of the 20 most frequent tokens in consecutive months:

$$V_{\text{text},t} = 1 - \frac{|T_t \cap T_{t-1}|}{|T_t \cup T_{t-1}|}$$

where $T_t$ is the set of the 20 highest-frequency tokens in month $t$ after removing standard English stopwords. A value of 1 indicates complete vocabulary turnover; a value of 0 indicates identical top-20 token sets. High lexical turnover reflects rapid shifts in the issues that dominate farmer discourse, consistent with a volatile information environment.

---

#### 3.2.3 Uncertainty

Uncertainty reflects the degree to which the future is unpredictable. Our quantitative measure ($U_{\text{quant}}$) is the inverted Index of Future Expectations:

$$U_{\text{quant},t} = -\overline{\text{IFE}}_t$$

where $\overline{\text{IFE}}_t$ is the monthly cross-sectional mean of the individual IFE scores. The IFE aggregates responses to questions about expected farm financial conditions, capital expenditures, and land values over the coming 12 months. A decline in IFE — farmers becoming more pessimistic about the future — corresponds to rising uncertainty, so the negation aligns the direction of $U_{\text{quant}}$ with the theoretical expectation. This specification is consistent with the use of consumer expectations indices as uncertainty proxies in the macroeconomics literature (Leduc and Liu, 2016).

Our text-based uncertainty measure ($U_{\text{text}}$) is a dictionary-based approach adapted from the Economic Policy Uncertainty (EPU) framework (Baker, Bloom, and Davis, 2016). For each month, we compute the share of open-ended responses containing at least one term from a combined dictionary of general uncertainty words (e.g., *uncertain*, *unpredictable*, *risk*) and agricultural policy-specific terms (e.g., *tariff*, *trade war*, *regulation*, *input costs*, *drought*):

$$U_{\text{text},t} = \frac{1}{N_t} \sum_{i=1}^{N_t} \mathbf{1}\left[\exists\, w \in \mathcal{D}_U : w \in r_{it}\right]$$

where $N_t$ is the number of responses in month $t$, $r_{it}$ is the text of response $i$, and $\mathcal{D}_U$ is the uncertainty dictionary. The full dictionary is provided in the supplementary materials.

---

#### 3.2.4 Complexity

Complexity captures the number of distinct forces acting simultaneously on farmer decision-making. We operationalize this using Latent Dirichlet Allocation (LDA) (Blei, Ng, and Jordan, 2003) applied to the pooled text corpus. We fit a $K = 10$ topic model on all monthly responses, then extract per-month topic share vectors representing the distribution of discourse across topics.

Our text-based complexity measure ($C_{\text{text}}$) is the mean Shannon entropy of the per-response topic distribution within each month:

$$C_{\text{text},t} = \frac{1}{N_t} \sum_{i=1}^{N_t} H(\boldsymbol{\theta}_{it})$$

where $H(\boldsymbol{\theta}_{it}) = -\sum_{k=1}^{K} \theta_{itk} \log \theta_{itk}$ is the entropy of response $i$'s topic distribution. Higher entropy indicates that a respondent's discourse draws on a more diverse set of topics, consistent with a more complex information environment.

Our quantitative complexity measure ($C_{\text{quant}}$) captures the dimensionality of the monthly topic distribution over time. We apply rolling Principal Component Analysis (PCA) over a 12-month window to the sequence of monthly mean topic share vectors, and define complexity as the inverse of the variance explained by the first principal component:

$$C_{\text{quant},t} = 1 - \lambda_1^{(t)}$$

where $\lambda_1^{(t)}$ is the share of variance explained by PC1 in the rolling window ending at month $t$. When a single dominant topic explains most variation ($\lambda_1^{(t)} \approx 1$), the information environment is low-complexity; when the topic space is multidimensional ($\lambda_1^{(t)} \approx 0$), it is high-complexity. All LDA models are estimated with a fixed random seed to ensure replicability.

---

#### 3.2.5 Ambiguity

Ambiguity arises when the causal structure of the environment itself is unclear — when the meaning of signals is contested or contradictory (Bennett and Lemoine, 2014). We capture this through both the distributional shape of individual AEB responses and the co-occurrence of contradictory sentiment in text responses.

Our quantitative ambiguity measure combines three components. First, we compute monthly excess kurtosis of the individual AEB distribution ($A_{\text{kurt},t}$), where a leptokurtic distribution (heavy tails, sharp center) indicates that most farmers agree but a substantial minority holds extreme views — a signature of an ambiguous signal. Second, we apply the Hartigan dip test (Hartigan and Hartigan, 1985) to the monthly AEB distribution as a formal test of bimodality ($A_{\text{dip},t}$); a bimodal distribution indicates that farmers cluster at two distinct sentiment levels, consistent with a mixed-signal environment. Third, we count the number of sign changes in monthly skewness over a 6-month rolling window ($A_{\text{flip},t}$), capturing instability in the direction of distributional asymmetry. The three components are standardized and averaged:

$$A_{\text{quant},t} = \frac{1}{3}\left(z_{A_{\text{kurt}},t} + z_{A_{\text{dip}},t} + z_{A_{\text{flip}},t}\right)$$

Our text-based ambiguity measure combines two indicators. The polarity conflict rate ($A_{\text{pol},t}$) is the share of monthly responses containing both positive-sentiment tokens (e.g., *profitable*, *confident*, *improve*) and negative-sentiment tokens (e.g., *struggling*, *loss*, *decline*) — responses in which the respondent expresses simultaneously optimistic and pessimistic signals. The ambiguity phrase rate ($A_{\text{phr},t}$) is the share of responses containing hedging expressions (e.g., *hard to tell*, *depends*, *mixed signals*, *wait and see*). Both are averaged after standardization:

$$A_{\text{text},t} = \frac{1}{2}\left(z_{A_{\text{pol}},t} + z_{A_{\text{phr}},t}\right)$$

---

### 3.3 Validation

We assess the construct validity of our VUCA measures using three complementary approaches.

**Face validity.** We examine whether each dimension score is elevated in the months surrounding five major structural events: the November 2016 U.S. presidential election, the March 2018 tariff announcements, the May 2019 U.S.–China trade war escalation, the March 2020 COVID-19 pandemic onset, and the March 2022 Federal Reserve rate hiking cycle. We compute average dimension scores in a ±2 month window around each event and compare them to the 2016–2019 baseline mean.

**Convergent validity.** We compute Pearson and Spearman correlations between each VUCA dimension score and the monthly mean AEB index. Theory predicts a negative relationship between uncertainty and overall sentiment (higher uncertainty depresses farm confidence), and a negative relationship between ambiguity and AEB. We do not impose a directional prior on volatility or complexity, as the relationship between these dimensions and aggregate sentiment is theoretically ambiguous.

**Discriminant validity.** We compute the full cross-correlation matrix of the four VUCA dimension scores. If each dimension captures a conceptually distinct aspect of environmental turbulence, we expect low to moderate inter-correlations. We flag pairs with Pearson $|r| > 0.70$ as potential evidence of construct overlap.

**Predictive validity.** We assess whether VUCA dimension scores contain leading information for downstream agricultural economic outcomes using Granger causality tests (Granger, 1969). Our external validation series are drawn from the Creighton University Main Street Economy survey (Goss and Natvig, 2023), a monthly survey of rural bank CEOs in agriculturally dependent regions of the United States: (i) a farm loan volume index, (ii) a farm equipment sales index, and (iii) a farmland price index. All three are diffusion indices with a neutral threshold of 50, analogous in construction to the AEB.

Prior to testing, we apply augmented Dickey-Fuller (ADF) tests to each series and first-difference any non-stationary series. We then estimate bivariate Granger causality models of the form:

$$y_t = \alpha + \sum_{l=1}^{L} \beta_l y_{t-l} + \sum_{l=1}^{L} \gamma_l x_{t-l} + \varepsilon_t$$

where $y_t$ is the external indicator, $x_t$ is the VUCA dimension score, and $L$ is the lag order. We test up to $L = 4$ monthly lags and report the F-statistic and p-value for the joint null hypothesis $H_0: \gamma_1 = \cdots = \gamma_L = 0$. Rejection of $H_0$ indicates that lagged VUCA scores contain predictive information for the external outcome beyond the outcome's own history. We interpret Granger causality as predictive relevance rather than structural causation (Sims, 1980).

---

*[END OF METHODS DRAFT]*

---

## Notes for revision

- **[CHECK]** AEB sample size per wave (~400) and exact survey window — confirm with Mintert/Widmar documentation
- **[CHECK]** Gross sales threshold ($500K) — verify eligibility criteria from AEB methodology docs
- **[CHECK]** Date range: confirm first wave (Oct 2015) and last wave in sample
- ~~**[CITE]** Mintert and Widmar~~ — filled ✓ → Mintert, J. and Widmar, D.A. (2016). Purdue University/CME Group Ag Economy Barometer. **[CHECK]** confirm exact working paper/report citation details with Mintert/Widmar docs.
- ~~**[CITE]** Bennett and Lemoine (2014)~~ — filled ✓
- ~~**[CITE]** Baker, Bloom, Davis (2016)~~ — filled ✓
- ~~**[CITE]** Blei, Ng, Jordan (2003)~~ — filled ✓
- ~~**[CITE]** Hartigan and Hartigan (1985)~~ — filled ✓
- ~~**[CITE]** Leduc and Liu (2016)~~ — filled ✓ → Leduc, S. and Liu, Z. (2016). "Uncertainty Shocks Are Aggregate Demand Shocks." *Journal of Monetary Economics* 82: 20–35. **[CHECK]** confirm this is the right Leduc/Liu paper.
- ~~**[CITE]** Curtin~~ — filled ✓ → Curtin, R. (2007). "Consumer Sentiment Surveys: Worldwide Review and Assessment." *Journal of Business Cycle Measurement and Analysis* 2007(1). **[CHECK]** confirm exact reference.
- ~~**[CITE]** Granger (1969)~~ — filled ✓ → Granger, C.W.J. (1969). "Investigating Causal Relations by Econometric Models and Cross-Spectral Methods." *Econometrica* 37(3): 424–438.
- ~~**[CITE]** Goss and Natvig~~ — filled ✓ → Goss, E. and Natvig, B. (2023). Creighton University Rural Mainstreet Economy Survey. **[CHECK]** verify correct citation format for this survey series.
- ~~**[CITE]** Sims (1980)~~ — filled ✓
- ~~Consider adding a summary table~~ — **RESOLVED:** Table 1 in `table1_measures_summary.md` ✓
