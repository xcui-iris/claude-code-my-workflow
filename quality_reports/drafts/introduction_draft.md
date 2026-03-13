# Introduction — DRAFT
**Target:** American Journal of Agricultural Economics (AJAE)
**Status:** Draft v2 — 2026-03-13 (citations filled)
**Note:** [CITE] = citation needed. [CHECK] = verify/expand before submission.

---

## 1. Introduction

Agricultural producers operate in environments characterized by rapid change, deep uncertainty, and the simultaneous interplay of forces that range from commodity market dynamics to climate variability and policy shifts. Despite a long tradition of measuring aggregate farm sentiment through diffusion indices — most notably the Purdue University/CME Group Ag Economy Barometer (AEB) — existing measures collapse the multidimensional nature of agricultural turbulence into a single composite score. This aggregation, while useful for tracking directional trends in farm confidence, obscures the distinct channels through which environmental complexity affects farm decision-making, investment behavior, and financial outcomes.

This paper proposes a framework for decomposing agricultural sentiment into four conceptually distinct dimensions drawn from the VUCA construct — Volatility, Uncertainty, Complexity, and Ambiguity — originally developed in military strategic planning (Bennis and Nanus, 1985) and subsequently applied to organizational management (Bennett and Lemoine, 2014). We operationalize each VUCA dimension using individual-level microdata from the AEB survey (October 2015 through December 2024), combining structured survey indices with open-ended text responses from approximately [CHECK: 47,668] individual farmer observations. To our knowledge, this is the first application of the VUCA framework to agricultural producer sentiment data.

Our approach makes three methodological contributions. First, we construct dual measures for each VUCA dimension — one quantitative, derived from the AEB's structured index questions, and one text-based, derived from farmers' open-ended responses — and combine them into standardized monthly scores. This dual-measure strategy leverages the complementary strengths of structured and unstructured data and allows us to assess the internal consistency of each dimension. Second, we develop an agricultural-domain adaptation of the Economic Policy Uncertainty (EPU) dictionary (Baker, Bloom, and Davis, 2016) that captures policy risk terms specific to the farm economy, including trade policy, input cost inflation, and weather-related uncertainty. Third, we apply Latent Dirichlet Allocation (Blei, Ng, and Jordan, 2003) to the full corpus of monthly text responses to construct a topic-based complexity measure that captures the dimensionality of the information environment facing farmers each month.

We validate our VUCA measures using three complementary approaches. Face validity assessments confirm that the Volatility dimension spikes around the 2019 U.S.–China trade war escalation and the 2020 COVID-19 pandemic onset, and that Complexity rises sharply during the 2021–2022 period of simultaneous commodity price surges and input cost inflation. Convergent validity is supported by a strong negative correlation between our Uncertainty measure and the AEB (Pearson $r = -0.758$), consistent with the theoretical expectation that forward-looking pessimism and aggregate farm confidence move in opposite directions. Granger causality tests against external agricultural economic indicators from the Creighton University Main Street Economy survey reveal that Volatility predicts farmland price changes at one to four month lags, and that Ambiguity leads farm loan volume by approximately two months — findings that demonstrate the predictive content of our VUCA measures for downstream agricultural financial outcomes.

Our results contribute to several literatures. For agricultural economists, we provide a richer characterization of the information environment facing farm operators and a set of monthly VUCA scores that can be used as regressors or conditioning variables in studies of farm investment, land markets, and credit demand. For the broader sentiment and uncertainty measurement literature, we demonstrate that the VUCA framework can be operationalized in a sectoral context using a combination of survey microdata and natural language processing methods. For practitioners and policymakers, our measures offer a more granular diagnostic tool for identifying not just whether farm sentiment is declining, but which dimension of turbulence is driving the deterioration — a distinction with direct implications for policy response.

The remainder of the paper is organized as follows. Section 2 reviews the relevant literature. Section 3 describes the data and methodology. Section 4 presents validation results. Section 5 discusses implications and limitations. Section 6 concludes.

---

*[END OF INTRODUCTION DRAFT]*

---

## Notes for revision

- **[CHECK]** Opening paragraph framing — confirm this aligns with the paper's broader argument before submission
- **[CHECK]** "first application of VUCA to agricultural sentiment" — verify with a literature search
- ~~**[CITE]** Bennis and Nanus (1985)~~ — filled ✓ → Bennis, W.G. and Nanus, B. (1985). *Leaders: The Strategies for Taking Charge.* Harper & Row.
- ~~**[CITE]** Bennett and Lemoine (2014)~~ — filled ✓ → Bennett, N. and Lemoine, G.J. (2014). "What a Difference a Word Makes: Understanding Threats to Performance in a VUCA World." *Business Horizons* 57(3): 311–317. (**NOTE:** journal is *Business Horizons*, not HBR)
- ~~**[CITE]** Baker, Bloom, Davis (2016)~~ — filled ✓ → Baker, S.R., Bloom, N. and Davis, S.J. (2016). "Measuring Economic Policy Uncertainty." *Quarterly Journal of Economics* 131(4): 1593–1636.
- ~~**[CITE]** Blei, Ng, Jordan (2003)~~ — filled ✓ → Blei, D.M., Ng, A.Y. and Jordan, M.I. (2003). "Latent Dirichlet Allocation." *Journal of Machine Learning Research* 3: 993–1022.
- **[TODO]** Add 1–2 sentences on the literature gap more explicitly (what prior work has NOT done)
- ~~Section 2 (literature review) is not drafted here~~ — **RESOLVED:** `literature_review_draft.md` created ✓
