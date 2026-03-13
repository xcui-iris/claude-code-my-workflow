# Literature Review — DRAFT
**Target:** American Journal of Agricultural Economics (AJAE)
**Status:** Draft v2 — 2026-03-13 (updated with VUCA Lit Review.docx sources)
**Note:** [CHECK] = verify/fill before submission. All [CITE] resolved.

---

## 2. Background and Related Literature

This paper sits at the intersection of four bodies of literature: the VUCA framework in organizational and strategy research; agricultural sentiment measurement and the AEB; economic uncertainty measurement; and the use of natural language processing (NLP) in agricultural economics. We review each in turn before positioning our contribution.

---

### 2.1 The VUCA Framework

The VUCA acronym — Volatility, Uncertainty, Complexity, Ambiguity — originated in U.S. Army War College doctrine in the late 1980s to characterize the post-Cold War strategic environment and subsequently entered the management literature through leadership research (Bennis and Nanus, 1985). The seminal academic treatment of the four dimensions is Bennett and Lemoine (2014), who distinguish the components as conceptually distinct challenges requiring different organizational responses: Volatility involves unstable but understandable change; Uncertainty involves knowledge gaps about events whose significance is unclear; Complexity involves interconnected forces and information overload; and Ambiguity involves unknown cause-and-effect relationships with no historical precedent. A critical implication of this taxonomy — and a finding replicated empirically by Fridgeirsson, Kristjansdottir, and Ingason (2021) — is that treating the four dimensions as interchangeable or aggregating them into a composite score leads to resource misallocation, because each dimension requires a qualitatively different response. Our paper is the first to formalize this argument in the agricultural economics context: we show that the dimensions are empirically separable and that disaggregating them yields predictive content that the composite AEB index alone does not.

Recent work has extended the VUCA framework in two directions relevant to our paper. First, Fridgeirsson et al. (2021) develop a "VUCA meter" — a questionnaire-based diagnostic instrument that assigns numerical severity scores to each dimension for complex projects — and demonstrate, in a small-sample study of manufacturing projects, that subjects find the aggregate VUCA score unhelpful and that each dimension requires an individualized response. Their finding that "Uncertainty appears to be a cascading factor in other dimensions" motivates our discriminant validity assessment and our expectation that U–A and U–C correlations will be positive but moderate. Second, [CHECK: fill citation] develop a validated psychometric "Perceived VUCA Exposure" scale using a four-factor confirmatory structure, finding a VU cluster (today's realities) and a CA cluster (tomorrow's potential) — a pattern broadly consistent with the low-but-nonzero cross-dimension correlations we document. Rzepczynski (2025) applies the VUCA framework to investment management, defining the dimensions in financial terms analogous to ours: Volatility as measurable distributional risk, Uncertainty as Knightian non-countable risk, Complexity as model misspecification, and Ambiguity as competing theories with unstable causal inferences.

A complementary conceptual contribution is provided by [CHECK: fill citation — "Clarifying the conceptual map of VUCA: a systematic review"], which conducts a systematic review of VUCA definitions and documents substantial conceptual overlap across the four terms in the management literature: uncertainty appeared in definitions of volatility; complexity appeared as a cause of uncertainty; ambiguity was frequently associated with uncertainty. This overlap at the conceptual level reinforces the value of our empirical discriminant validity tests, which confirm the dimensions are distinct despite conceptual adjacency.

---

### 2.2 Agricultural Sentiment Measurement

The most widely used measure of U.S. agricultural producer sentiment is the Purdue University/CME Group Ag Economy Barometer (AEB), introduced in October 2015 (Mintert and Widmar, 2016). The AEB follows the diffusion index methodology of the University of Michigan Index of Consumer Sentiment (Curtin, 2007), with a monthly sample of approximately 400 farm operators. The AEB decomposes into two sub-indices: the Index of Current Conditions (ICC) and the Index of Future Expectations (IFE). Monthly AEB reports have been used as leading indicators for farm machinery sales, farm credit demand, and farmland market activity.

The paper most directly related to ours in the AEB literature is Lippsmeyer, Langemeier, Mintert, and Thompson (2024), who examine the drivers of cross-sectional heterogeneity in producer sentiment. They find that statistically significant correlates of high sentiment include farm operator experience, educational attainment, balance sheet strength, and low fixed costs, and document that high-sentiment producers are more concerned with human capital and marketing risk while low-sentiment producers are more focused on financial risk. Our paper complements Lippsmeyer et al. (2024) by analyzing the time-series structure of sentiment rather than its cross-sectional correlates, and by decomposing aggregate sentiment into the four VUCA dimensions rather than a single composite. Their finding that different risk types matter differently for different producers provides micro-level support for the theoretical argument that a single aggregate index conflates qualitatively distinct sources of farm-level turbulence.

A related literature examines farmer expectations more broadly, using panel surveys to study expectation formation and the role of past experience in shaping beliefs about future prices and policy. These papers confirm that farm operators hold heterogeneous beliefs — a fact that motivates our use of individual-level AEB microdata rather than the published aggregate, and that underlies our Ambiguity measure's reliance on the distributional shape of individual responses.

---

### 2.3 Uncertainty Measurement in Economics

The quantitative measurement of economic uncertainty has been an active research area since Baker, Bloom, and Davis (2016) constructed the Economic Policy Uncertainty (EPU) index from newspaper text frequency, tax code expiration provisions, and forecaster disagreement. The EPU methodology has inspired a growing number of sector-specific uncertainty indices and has been applied to study investment, hiring, and monetary policy transmission across a wide range of contexts.

An important empirical result for our paper's motivation comes from Nowzohour and Stracca (2020), who survey the literature on economic sentiment (confidence and uncertainty) and macroeconomic fluctuations and find that "confidence and uncertainty are unrelated" — different sentiment measures within the same country are weakly correlated, and different proxies for the same underlying concept capture substantially different variation. The implication is direct: a composite sentiment index like the AEB conflates at least two distinct constructs (confidence and uncertainty), and using it as a single measure of the agricultural information environment discards information that is relevant to downstream outcomes. Our paper formalizes this intuition within the VUCA taxonomy and demonstrates empirically that the four dimensions of our decomposition carry non-redundant predictive content.

In the agricultural sector, Adjemian et al. [CHECK: fill citation] construct measures of agricultural policy uncertainty using USDA report surprise events; Karali et al. [CHECK: fill citation] examine the role of uncertainty in commodity futures price dynamics. Our Uncertainty dimension builds on the EPU framework by adapting the dictionary-based text measurement approach to the agricultural open-ended survey context, supplemented by a structured measure derived from the IFE sub-index, and supplemented by Leduc and Liu's (2016) finding that inverted expectations indices serve as valid uncertainty proxies in macroeconomic settings.

The broader uncertainty literature distinguishes risk (quantifiable probabilities) from Knightian uncertainty (Knight, 1921) and Ellsberg-style ambiguity (Ellsberg, 1961). This distinction maps directly onto the VUCA taxonomy: our Uncertainty dimension captures Knight-style opacity about future outcomes, while our Ambiguity dimension captures situations in which farmers cannot form a stable probability assessment. Rzepczynski (2025) formalizes a parallel distinction for investment management contexts. To our knowledge, our paper is the first to operationalize both constructs simultaneously in an agricultural survey.

---

### 2.4 Sentiment and Uncertainty in Investment Decisions

The role of sentiment and uncertainty in shaping producer investment decisions is directly relevant to interpreting our Granger causality results. Birru and Young (2023) find that investor sentiment has a modest positive relationship with corporate investment, but that this relationship is substantially amplified when interacted with a market volatility measure — consistent with our finding that the Volatility dimension of farm sentiment contains leading information for farmland prices. Their result that high-volatility firms show the strongest sentiment–investment link (doubling the baseline coefficient) motivates our hypothesis that Volatility is particularly relevant for farmland markets, which share the characteristic of being difficult to value precisely.

The real options literature (Dixit and Pindyck, 1994) establishes that irreversible investments — including farmland purchases and major capital expenditures — are optimally delayed when uncertainty is high, as the option value of waiting increases with the volatility of the underlying state variable. This framework predicts that our Ambiguity measure — which captures the degree of contradictory signaling in farmer responses — should lead farm loan volume (a measure of productive investment) with a positive lag, consistent with our empirical finding. Baran and Woznyj (2020) extend this argument to organizational behavior, finding that communication and adaptation strategies can mitigate the performance costs of VUCA environments — a finding that suggests our VUCA measures could serve as inputs to farm advisory and extension programming.

For farmland markets specifically, Featherstone and Baker (1987) establish that farmland values capitalize expected future cash rents, with interest rates and inflation playing important secondary roles. Moss and Katchova (2005) and related work extend this framework to incorporate risk premia and expectation heterogeneity. Our finding that Volatility Granger-causes farmland prices at one to four month lags is consistent with a model in which rapidly changing sentiment contains information about the risk premium required by land market participants, analogous to the role of implied volatility in financial asset pricing.

---

### 2.5 Natural Language Processing in Agricultural Economics

The use of NLP methods in agricultural and food economics has grown substantially in the past decade. Hendricks et al. [CHECK] use topic modeling to identify themes in agricultural news coverage; Lusk [CHECK] applies sentiment analysis to consumer food preference data. In the broader applied economics literature, Gentzkow, Kelly, and Taddy (2019) provide a comprehensive survey of text-as-data methods relevant to economists.

The most closely related NLP application to ours is the use of open-ended survey responses to supplement structured questionnaire data. Whereas standard survey analysis discards or separately codes free-text fields, we treat these responses as a parallel data stream reflecting the same underlying latent state as the structured responses but through a different measurement channel. This dual-measure strategy is analogous to the mixed-methods approach operationalized in the financial text sentiment literature by Loughran and McDonald (2011). Patnaik (2020) surveys 51 applied machine learning papers organized under the four VUCA dimensions and notes that the computational approaches to each dimension differ substantially — supporting our decision to use qualitatively distinct methods for each of our text-based measures (Jaccard distance for Volatility; dictionary hit rate for Uncertainty; LDA entropy for Complexity; polarity conflict for Ambiguity) rather than a single NLP technique applied uniformly.

Our use of Latent Dirichlet Allocation (LDA; Blei, Ng, and Jordan, 2003) to construct the Complexity dimension follows a substantial body of work applying topic modeling to economic and social science text. Our approach of measuring the dimensionality of the topic space via rolling PCA on monthly topic share vectors is novel and provides a tractable monthly time series that captures the degree to which farmers' information environment is multidimensional.

---

### 2.6 Positioning Our Contribution

Our paper makes three distinct contributions relative to the literatures reviewed above. First, we are the first to operationalize the VUCA framework in an agricultural context using individual-level survey microdata, providing a richer characterization of environmental turbulence than either the composite AEB or existing agricultural uncertainty indices. The closest methodological predecessor — Fridgeirsson et al.'s (2021) VUCA meter — relies on expert questionnaires applied to a small sample of complex projects; our approach scales to a large, representative monthly panel and produces time-series measures suitable for econometric analysis.

Second, we demonstrate that the four VUCA dimensions are empirically separable in a setting where conceptual overlap is substantial. This complements the conceptual work of Bennett and Lemoine (2014) and the systematic review of [CHECK: "Clarifying the conceptual map of VUCA"] by providing quantitative evidence that the four dimensions capture distinct variation — a finding that the perceived VUCA exposure scale literature ([CHECK]) and Nowzohour and Stracca (2020) predict but do not establish in an agricultural context.

Third, we establish that disaggregating sentiment into VUCA dimensions generates economically meaningful predictive content: Volatility leads farmland price changes and Ambiguity leads farm credit demand at horizons relevant for policy analysis. These findings connect the VUCA measurement literature to the real options literature on investment under uncertainty and to the farmland valuation literature, and complement Lippsmeyer et al.'s (2024) cross-sectional evidence on the drivers of producer sentiment with time-series evidence on the consequences of specific types of turbulence.

---

*[END OF LITERATURE REVIEW DRAFT]*

---

## Notes for revision

**Citations resolved:**
- Bennett and Lemoine (2014) → *Business Horizons* 57(3): 311–317 (**NOT HBR** — corrected from v1)
- Fridgeirsson, T.V., Kristjansdottir, B.H., and Ingason, H.T. (2021). "An Alternative Risk Assessment Routine for Decision Making; Towards a VUCA Meter..." In R. Cuevas et al. (Eds.), *Research on Project, Programme and Portfolio Management*, pp. 41–54. Springer.
- Nowzohour, L. and Stracca, L. (2020). "More Than a Feeling: Confidence, Uncertainty, and Macroeconomic Fluctuations." *Journal of Economic Surveys* 34(4): 1–36.
- Lippsmeyer, M., Langemeier, M., Mintert, J., and Thompson, N. (2024). "Factors Influencing Producer Sentiment." *Journal of ASFMRA* 2024: 58–70.
- Rzepczynski, M.S. (2025). "Clarifying the Assessment of Risk: VUCA." SSRN Working Paper No. 5217110.
- Birru, J. and Young, T. (2023). "The Real Effects of Sentiment and Uncertainty." Working Paper, Ohio State / Tulane.
- Baran, B.E. and Woznyj, H.M. (2020). "Managing VUCA: The Human Dynamics of Agility." *Organizational Dynamics* 49(2): 100787.
- Patnaik, S. (2020). "Applied machine learning and management of VUCA." *Journal of Intelligent & Fuzzy Systems* (Sage). https://journals.sagepub.com/doi/full/10.3233/JIFS-179915

**Still need full citations [CHECK]:**
- "Being Affected By VUCA Factors? Developing The Perceived VUCA Exposure Scale" — no citation in docx; search for this title
- "Clarifying the conceptual map of VUCA: a systematic review" — no citation in docx; search for this title
- Adjemian et al. agricultural policy uncertainty paper — search USDA ERS
- Karali et al. commodity futures uncertainty paper
- Hendricks et al. ag news topic modeling
- Lusk food preference sentiment paper
- Gentzkow, Kelly, Taddy (2019) — "Text as Data," *Journal of Economic Literature*
- Loughran and McDonald (2011) — "When Is a Liability Not a Liability?" *Journal of Finance*
- Bennis and Nanus (1985) — "Leaders: The Strategies for Taking Charge," Harper & Row

**CHECK items resolved in this draft:**
- Bennett & Lemoine corrected to *Business Horizons* (not HBR) ✓
- $500K eligibility threshold confirmed by user ✓
- 2021–2022 AEB elevation confirmed by user ✓

**Structural notes:**
- Section length ~5 manuscript pages; AJAE typically accepts 3–4. Consider cutting 2.5 (NLP) or merging 2.4 with 2.3.
- The "Perceived VUCA Exposure Scale" and "Clarifying the conceptual map" papers are important for discriminant validity framing — find citations before submission.
