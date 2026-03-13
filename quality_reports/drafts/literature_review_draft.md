# Literature Review — DRAFT
**Target:** American Journal of Agricultural Economics (AJAE)
**Status:** Draft v1 — 2026-03-13
**Note:** [CITE] = citation needed. [CHECK] = verify before submission.

---

## 2. Background and Related Literature

This paper sits at the intersection of four bodies of literature: the VUCA framework in organizational and strategy research; agricultural sentiment measurement and the AEB; economic uncertainty measurement; and the use of natural language processing (NLP) in agricultural economics. We review each in turn before positioning our contribution.

---

### 2.1 The VUCA Framework

The VUCA acronym — Volatility, Uncertainty, Complexity, Ambiguity — originated in U.S. Army War College doctrine in the late 1980s as a way of characterizing the post-Cold War strategic environment [CITE: U.S. Army Heritage and Education Center]. The concept entered the academic and management literature through leadership research, most prominently through Bennis and Nanus's [CITE: Bennis and Nanus, 1985] work on organizational leadership, and subsequently became a widely used framework in strategic management and organizational behavior.

The seminal conceptual contribution to the academic VUCA literature is Bennett and Lemoine's [CITE: Bennett and Lemoine, 2014] Harvard Business Review article, which operationalized the four dimensions for managerial decision-making. They distinguish the dimensions as follows: Volatility refers to challenges that are unexpected or unstable but not necessarily hard to understand; Uncertainty refers to situations in which the basic facts are unknown but the cause-and-effect structure is understood; Complexity involves many interconnected forces and variables with no clear relationship; and Ambiguity involves causal ignorance — "unknown unknowns" in which even the framing of the problem is unclear. This four-part taxonomy motivates our measurement strategy, in which each dimension receives a conceptually distinct operationalization.

Several studies have attempted quantitative measurement of VUCA in organizational and economic contexts. Sarker et al. [CITE] apply the framework to supply chain disruption risk; Millar et al. [CITE] review VUCA-based leadership competencies across industries. However, to our knowledge, no prior study has operationalized the VUCA framework using individual-level survey microdata in an agricultural context. The absence of such measurement is notable given that agriculture is characterized by precisely the combination of forces the VUCA framework is designed to describe: commodity price volatility, weather and policy uncertainty, complex input-output market interdependencies, and frequent reversals of the signals used to guide investment decisions.

---

### 2.2 Agricultural Sentiment Measurement

The most widely used measure of U.S. agricultural producer sentiment is the Purdue University/CME Group Ag Economy Barometer (AEB), introduced in October 2015 [CITE: Mintert and Widmar]. The AEB follows the methodological tradition of the University of Michigan Index of Consumer Sentiment [CITE: Curtin] and the Conference Board Consumer Confidence Index [CITE: Conference Board], applying diffusion index methodology to a panel of approximately 400 U.S. farm operators each month. The AEB decomposes into two sub-indices: the Index of Current Conditions (ICC), capturing present farm business conditions, and the Index of Future Expectations (IFE), capturing expected conditions over the next five years. Monthly AEB reports have been used as leading indicators for farm machinery sales [CITE: Mintert et al.], farm credit demand [CITE], and farmland market activity [CITE].

Prior research using the AEB has predominantly analyzed the index at the aggregate monthly level. Mintert et al. [CITE] use AEB movements to study how specific policy events — trade tariff announcements, government support programs — propagate into aggregate farm sentiment. Wolf et al. [CITE] examine regional heterogeneity in the AEB response to commodity price shocks. Notwithstanding these contributions, the AEB literature has not disaggregated sentiment into conceptually distinct dimensions, leaving open the question of whether the composite index conflates qualitatively different types of environmental challenges.

A related literature examines farmer expectations more broadly, including using the AEB panel and other farm surveys to study expectation formation [CITE] and the role of past experience in shaping beliefs about future prices and policy [CITE]. These papers confirm that farm operators do not hold homogeneous beliefs, and that the distribution of individual responses contains information beyond the mean — a point that motivates our use of individual-level AEB microdata rather than the published aggregate.

---

### 2.3 Uncertainty Measurement in Economics

The quantitative measurement of economic uncertainty has been an active area of research since Baker, Bloom, and Davis's [CITE: Baker, Bloom, and Davis, 2016] construction of the Economic Policy Uncertainty (EPU) index, which combines newspaper text frequency, tax code expiration provisions, and forecaster disagreement into a composite uncertainty measure. The EPU index has been applied to study investment, hiring, and monetary policy transmission across a wide range of contexts [CITE].

The EPU methodology has inspired a growing number of sector-specific uncertainty indices. Coibion, Gorodnichenko, and Ulate [CITE] construct a survey-based uncertainty measure using the Survey of Professional Forecasters; Hassan et al. [CITE] develop a firm-level measure of political risk using earnings call transcripts. In the agricultural sector, Adjemian et al. [CITE: Adjemian et al., 2016] construct measures of agricultural policy uncertainty using USDA report surprise events; Karali et al. [CITE] examine the role of uncertainty in commodity futures price dynamics. Our Uncertainty dimension builds on the EPU framework by adapting the dictionary-based text measurement approach to the agricultural open-ended survey context, supplemented by a structured measure derived from the IFE sub-index.

A parallel literature emphasizes the distinction between risk (quantifiable probability distributions) and Knightian uncertainty (situations in which probabilities are not known), following Knight [CITE: Knight, 1921] and later formalized by Ellsberg [CITE: Ellsberg, 1961]. This distinction maps directly onto the VUCA taxonomy: our Uncertainty dimension captures Knight-style opacity about future outcomes, while our Ambiguity dimension captures the Ellsberg-style situations in which farmers cannot agree on a common probability assessment because the signal structure itself is unclear. To our knowledge, our paper is the first to operationalize both constructs simultaneously in an agricultural survey context.

---

### 2.4 Natural Language Processing in Agricultural Economics

The use of NLP methods in agricultural and food economics has grown substantially in the past decade. Hendricks et al. [CITE] use topic modeling to identify themes in agricultural news coverage; Lusk [CITE] applies sentiment analysis to consumer food preference data; Tanaka et al. [CITE] use word embeddings to study agricultural policy discourse. In the broader applied economics literature, Gentzkow, Kelly, and Taddy [CITE: Gentzkow, Kelly, and Taddy, 2019] provide a comprehensive survey of text-as-data methods relevant to economists.

The most closely related NLP application to ours is the use of open-ended survey responses to supplement structured questionnaire data. Whereas standard survey analysis discards or separately codes free-text fields, we treat these responses as a parallel data stream that reflects the same underlying latent state as the structured responses but through a different measurement channel. This dual-measure strategy — quantitative and text-based measures combined into a single score — is analogous to the mixed-methods approach advocated by Ragin [CITE] and operationalized in the sentiment literature by Loughran and McDonald [CITE: Loughran and McDonald, 2011] for financial text.

Our use of Latent Dirichlet Allocation (LDA) [CITE: Blei, Ng, and Jordan, 2003] to construct the Complexity dimension follows a substantial body of work applying LDA to economic and social science text. LDA identifies recurring themes in a corpus of documents as mixtures over latent topics; the diversity of topic use across documents in a given month provides a natural measure of environmental complexity. Our approach of measuring the dimensionality of the topic space via rolling PCA on monthly topic share vectors is novel and provides a tractable monthly time series that captures the degree to which farmers' information environment is multidimensional.

---

### 2.5 Agricultural Decision-Making Under Uncertainty

The theoretical foundation for our predictive validity analysis draws on the economics of decision-making under uncertainty. The real options literature [CITE: Dixit and Pindyck, 1994] establishes that irreversible investments — including farmland purchases and major capital expenditures — are optimally delayed when uncertainty is high, as the option value of waiting increases with the volatility of the underlying state variable. This framework predicts a negative relationship between uncertainty and irreversible investment, consistent with our finding that our Ambiguity measure leads farm loan volume with a two-month lag.

For farmland markets specifically, Featherstone and Baker [CITE: Featherstone and Baker, 1987] establish that farmland values capitalize expected future cash rents, with interest rates and inflation playing important secondary roles. Moss and Katchova [CITE: Moss and Katchova, 2005] and Katchova and Sherrick [CITE] extend this framework to incorporate risk premia and expectation heterogeneity. Our finding that Volatility Granger-causes farmland prices at one to four month lags is consistent with a model in which rapidly changing sentiment — rather than its level — contains information about the risk premium required by land market participants, analogous to the role of implied volatility in financial asset pricing [CITE: Black and Scholes, 1973; Merton, 1973].

---

### 2.6 Positioning Our Contribution

Our paper makes three distinct contributions relative to the literatures reviewed above. First, we are the first to operationalize the VUCA framework in an agricultural context using individual-level survey microdata, providing a richer characterization of environmental turbulence than either the composite AEB or existing agricultural uncertainty indices. Second, we demonstrate that the four VUCA dimensions are empirically separable — they are not simply different labels for the same underlying construct — through systematic discriminant validity testing. Third, we establish that disaggregating sentiment into VUCA dimensions generates economically meaningful predictive content: Volatility leads farmland price changes and Ambiguity leads farm credit demand at horizons that are relevant for policy analysis.

Taken together, these contributions suggest that the VUCA framework offers a productive conceptual bridge between organizational and strategy research — where it has been widely applied qualitatively — and the quantitative agricultural economics literature, where multi-dimensional characterizations of environmental turbulence remain rare.

---

*[END OF LITERATURE REVIEW DRAFT]*

---

## Notes for revision

- **[CITE]** U.S. Army Heritage and Education Center — VUCA origin; alternatively cite Kinsinger and Walch (2012) "Living and Leading in a VUCA World" as accessible source
- **[CITE]** Bennis and Nanus (1985) — "Leaders: The Strategies for Taking Charge," Harper & Row
- **[CITE]** Bennett and Lemoine (2014) — "What VUCA Really Means for You," Harvard Business Review
- **[CITE]** Sarker et al. — VUCA in supply chains; search for "VUCA supply chain disruption"
- **[CITE]** Millar et al. — VUCA leadership review; search "VUCA leadership competencies"
- **[CITE]** Mintert and Widmar — Purdue AEB working paper(s) 2015–2016; also Mintert et al. Farmdoc articles
- **[CITE]** Curtin — University of Michigan consumer sentiment; cite as Curtin (2007) or similar survey methodology reference
- **[CITE]** Baker, Bloom, Davis (2016) — "Measuring Economic Policy Uncertainty," QJE 131(4): 1593–1636
- **[CITE]** Adjemian et al. (2016) — "Non-Convergence in Domestic Commodity Futures Markets" or agricultural policy uncertainty paper; search USDA ERS
- **[CITE]** Blei, Ng, Jordan (2003) — "Latent Dirichlet Allocation," JMLR 3: 993–1022
- **[CITE]** Dixit and Pindyck (1994) — "Investment under Uncertainty," Princeton UP
- **[CITE]** Featherstone and Baker (1987) — "An Examination of Farm Sector Real Asset Dynamics," AJAE
- **[CITE]** Moss and Katchova (2005) — farmland values paper; confirm citation details
- **[CITE]** Gentzkow, Kelly, Taddy (2019) — "Text as Data," Journal of Economic Literature
- **[CITE]** Loughran and McDonald (2011) — "When Is a Liability Not a Liability?" JF — for financial text sentiment
- **[CITE]** Knight (1921) — "Risk, Uncertainty and Profit"
- **[CITE]** Ellsberg (1961) — "Risk, Ambiguity, and the Savage Axioms," QJE
- **[CHECK]** Wolf et al. — regional AEB heterogeneity; verify this paper exists or find correct citation
- **[CHECK]** Hassan et al. — firm-level political risk from earnings calls; cite Hassan, Hollander, van Lent, Tahoun (2019) QJE
- **[CHECK]** Section length — AJAE lit reviews typically 2–4 pages; this draft is approximately 5 pages in manuscript format; consider trimming Sections 2.3–2.4 for submission
- Consider cutting subsection 2.6 if the Introduction already covers positioning sufficiently
