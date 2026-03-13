"""
dictionaries.py — VUCA AEB Extension
======================================
Word lists and phrase lists used by 02_text_vuca.py.

All lists are lowercase. Text is lowercased before matching.

Sources:
  - EPU words: Baker, Bloom & Davis (2016) Economic Policy Uncertainty
  - Ag-specific terms: adapted from AEB survey context and trade war literature
  - Ambiguity phrases: common English hedging expressions
"""

# ── U — Uncertainty: EPU core words ─────────────────────────────────────────
EPU_WORDS = [
    "uncertain", "uncertainty", "unclear", "unpredictable", "unpredictability",
    "unknown", "unknowns", "unforeseeable", "volatile", "volatility",
    "risk", "risks", "risky", "doubt", "doubtful", "unsure",
    "hesitant", "hesitancy", "worried", "worry", "concern", "concerns",
    "anxious", "anxiety", "nervous", "nervousness",
]

# ── U — Uncertainty: Agricultural / policy-specific terms ───────────────────
AG_UNCERTAINTY_WORDS = [
    # Trade policy
    "tariff", "tariffs", "trade", "trade war", "trade deal", "trade policy",
    "sanction", "sanctions", "export", "exports", "import", "imports",
    "china", "soybean", "soybeans", "corn", "grain",
    # Farm policy
    "regulation", "regulations", "regulatory", "policy", "policies",
    "government", "legislation", "fsa", "usda", "subsidy", "subsidies",
    "farm bill", "mfp",
    # Input costs
    "fertilizer", "fuel", "diesel", "chemical", "chemicals",
    "input", "inputs", "cost", "costs", "price", "prices", "inflation",
    # Weather / environment
    "weather", "drought", "flood", "flooding", "rain", "rainfall",
    "freeze", "frost", "moisture", "crop", "yield", "harvest",
    # Financial / credit
    "interest", "interest rate", "loan", "loans", "credit", "debt",
    "banker", "bankers", "cash flow", "operating loan",
    # Labor
    "labor", "labour", "worker", "workers", "h2a", "workforce",
]

# Combined uncertainty dictionary
UNCERTAINTY_WORDS = list(set(EPU_WORDS + AG_UNCERTAINTY_WORDS))


# ── A — Ambiguity: Mixed-signal phrases ─────────────────────────────────────
AMBIGUITY_PHRASES = [
    "hard to tell", "hard to say", "hard to know",
    "difficult to tell", "difficult to predict", "difficult to say",
    "depends", "it depends", "depends on",
    "mixed signals", "mixed results", "mixed feelings",
    "unclear", "not clear", "no clear",
    "don't know", "do not know", "not sure", "unsure",
    "could go either way", "too early to tell", "wait and see",
    "both good and bad", "good and bad", "mixed bag",
    "not sure what to expect", "hard to predict",
    "on the fence", "uncertain about",
]


# ── A — Ambiguity: Positive sentiment words ──────────────────────────────────
# For polarity conflict detection: response has BOTH positive and negative
POSITIVE_WORDS = [
    "good", "great", "excellent", "positive", "optimistic", "optimism",
    "improve", "improving", "improvement", "better", "best",
    "strong", "strength", "confident", "confidence",
    "profitable", "profit", "profitable", "opportunity", "opportunities",
    "recover", "recovery", "recovering", "growth", "growing",
    "stable", "stability", "steady", "encourage", "encouraging",
    "increase", "increases", "increased", "higher", "up",
    "favorable", "favourable", "hopeful", "hope",
]

NEGATIVE_WORDS = [
    "bad", "terrible", "poor", "negative", "pessimistic", "pessimism",
    "decline", "declining", "decline", "worse", "worst",
    "weak", "weakness", "worried", "worry", "concern",
    "unprofitable", "loss", "losses", "threat", "threats",
    "struggling", "struggle", "difficult", "difficulty", "hard",
    "decrease", "decreased", "lower", "down", "drop", "falling",
    "unfavorable", "unfavourable", "bleak", "dire", "grim",
    "hurt", "hurting", "damage", "damaging", "suffering",
]
