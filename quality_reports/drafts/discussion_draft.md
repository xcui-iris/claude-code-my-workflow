# Discussion and Limitations — DRAFT
**Target:** American Journal of Agricultural Economics (AJAE)
**Status:** Draft v2 — 2026-03-13 (citations filled)
**Note:** [CHECK] = verify before submission.

---

## 5. Discussion and Limitations

### 5.1 Interpretation of Key Findings

Our results support the core premise of this paper: the VUCA framework captures distinct and economically meaningful dimensions of agricultural turbulence that a single composite sentiment index cannot. Three substantive findings merit particular discussion.

**Volatility as a leading indicator of land markets.** The finding that our Volatility measure Granger-causes farmland price changes at all four tested lag lengths is, to our knowledge, a novel result. Prior research on farmland price determinants has emphasized capitalization of expected cash rents, interest rates, and macroeconomic fundamentals (Featherstone and Baker, 1987; Moss and Katchova, 2005), but has paid less attention to the informational content of sentiment volatility. Our result suggests that rapid fluctuations in farmer confidence — as captured by the rolling standard deviation of AEB changes — contain forward-looking information that land market participants act upon with a one to four month lag. This is consistent with a model in which farmland buyers and sellers use aggregate sentiment surveys as noisy signals of future agricultural conditions, with land price adjustments following the signal with a delay that reflects market search frictions and transaction costs.

**Ambiguity and farm credit demand.** The finding that our Ambiguity measure leads farm loan volume by approximately two months offers a plausible mechanism: when farmers receive mixed signals about future conditions — evidenced by both polarity conflict in their open-ended responses and distributional bimodality in their structured AEB scores — they may defer productive investment while increasing operating credit as a precautionary buffer. This interpretation is consistent with the real options literature on investment under uncertainty (Dixit and Pindyck, 1994), extended here to a context of genuine ambiguity rather than quantified risk.

**The complexity of 2021–2022.** The sharp rise in our Complexity measure during 2021–2022 reflects a genuinely unusual period in which farmers simultaneously navigated commodity price surges, tripling fertilizer costs, equipment supply shortages, and tightening credit markets. That our LDA-based complexity measure — which captures the dimensionality of the topic space in farmers' text responses — rises sharply in this period, while the AEB itself remained relatively elevated, illustrates the value of decomposing sentiment: the 2021–2022 period was simultaneously "good" (high commodity prices, high AEB) and "complex" (an unusually multidimensional operating environment), a distinction lost in a single composite index.

---

### 5.2 Limitations

Several limitations of this study warrant acknowledgment.

**Baseline period sensitivity.** Our standardization protocol anchors all VUCA scores to a 2016–2019 baseline. This period includes the onset of the U.S.–China trade war (2018–2019), which means our baseline already embeds elevated uncertainty. As a result, the Uncertainty dimension tends to register negative values for much of the post-2019 sample — not because farmers became less uncertain, but because the reference level is already high. Future work should explore alternative baseline periods, such as 2015–2017, and assess the sensitivity of key results to this choice.

**Ambiguity signal strength.** The Ambiguity dimension exhibits weaker event-window responses than the other three dimensions. This likely reflects two sources of measurement limitation. First, the polarity conflict rate and ambiguity phrase rate rely on relatively short open-ended responses, which may not provide sufficient text for reliable mixed-signal detection. Second, the ambiguity phrase dictionary is constructed from general English hedging expressions; agricultural-domain hedging language may differ in ways not captured by our current dictionary. Future work could develop a domain-specific ambiguity lexicon using supervised learning approaches (e.g., Loughran and McDonald, 2011, for domain-adapted financial lexicons).

**Text response coverage.** The open-ended text responses used for our text-based measures are available only for the subset of AEB respondents who choose to provide them. If text-response propensity is correlated with sentiment or farm characteristics, our text-based measures may not be representative of the full survey population. We do not have access to respondent-level covariates that would allow a formal assessment of text-response selection.

**Statistical power of the Hartigan dip test.** The Hartigan dip test for bimodality (Hartigan and Hartigan, 1985), used in our Ambiguity measure, has low power when monthly response counts fall below approximately 50. We flag these months in our diagnostic output and exclude them from the bimodality component of the Ambiguity measure. Approximately [CHECK: N] months fall below this threshold, concentrated in the early sample (2015–2016) when the AEB panel was still building.

**External validation scope.** Our predictive validity tests use three indicators from a single external survey (Creighton Main Street Economy). While these series span a broad set of agricultural financial outcomes, they are also diffusion indices subject to similar measurement limitations as the AEB itself. Future validation work should incorporate hard data — realized farmland transaction prices, call report farm loan volumes, USDA machinery sales — to provide a more rigorous test of predictive content.

**Granger causality and structural inference.** Granger causality tests establish predictive precedence, not structural causation (Sims, 1980). Our finding that Volatility Granger-causes farmland prices does not establish that sentiment volatility causes land price changes; it establishes only that lagged Volatility scores contain information about future land price movements not captured by the land price series itself. Establishing structural causation would require an identification strategy beyond the scope of the current paper.

---

*[END OF DISCUSSION DRAFT]*

---

## Notes for revision

- ~~**[CITE]** Featherstone and Baker (1987)~~ — filled ✓ → Featherstone, A.M. and Baker, T.G. (1987). "An Examination of Farm Sector Real Asset Dynamics." *AJAE* 69(3): 532–546.
- ~~**[CITE]** Moss and Katchova (2005)~~ — filled ✓ → Moss, C.B. and Katchova, A.L. (2005). "Farmland Valuation and Asset Performance." *Agricultural Finance Review* 65(1): 119–130. **[CHECK]** confirm exact year/journal.
- ~~**[CITE]** Dixit and Pindyck (1994)~~ — filled ✓ → Dixit, A.K. and Pindyck, R.S. (1994). *Investment under Uncertainty.* Princeton University Press.
- ~~**[CITE]** Sims (1980)~~ — filled ✓ → Sims, C.A. (1980). "Macroeconomics and Reality." *Econometrica* 48(1): 1–48.
- ~~**[CITE]** Hartigan and Hartigan (1985)~~ — filled ✓ → Hartigan, J.A. and Hartigan, P.M. (1985). "The Dip Test of Unimodality." *Annals of Statistics* 13(1): 70–84.
- **[CHECK]** Number of months with N < 50 for dip test — pull from `01_quant_vuca.py` diagnostic output
- ~~**[CHECK]** 2021–2022 AEB level~~ — **CONFIRMED by user** ✓ AEB was elevated in 2021–2022.
- Consider adding a subsection on policy implications if journal reviewers request it
