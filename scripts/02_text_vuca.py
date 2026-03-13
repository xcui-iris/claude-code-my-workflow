"""
02_text_vuca.py — VUCA AEB Extension
========================================
Compute text-based VUCA sub-measures from Word Cloud open-ended responses.

Inputs:
    output/text_monthly.parquet   (from 00_load_data.py)

Outputs:
    output/text_measures.parquet

Measures:
    V_text  — Jaccard distance of top-20 tokens, month t vs t-1
    U_text  — % responses containing ≥1 EPU/ag uncertainty word
    C_text  — mean Shannon entropy of per-response LDA topic distributions
    C_quant — inverse PC1 variance share over rolling LDA topic vectors (moved here as LDA-based)
    A_polarity_conflict — % responses with both positive and negative tokens
    A_phrase_rate — % responses containing ≥1 ambiguity phrase

Usage:
    python scripts/02_text_vuca.py

Note: LDA is compute-intensive. First run may take 5–15 minutes.
      LDA model is NOT cached — rerun re-trains from scratch.
"""

import sys
import pathlib
import re
import warnings
import numpy as np
import pandas as pd
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import config
import dictionaries as dicts

warnings.filterwarnings("ignore")

# Lazy imports for optional heavy dependencies
try:
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation, PCA
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("[WARNING] scikit-learn not found. C_text measures will be skipped.")

try:
    import nltk
    from nltk.corpus import stopwords
    try:
        STOPWORDS = set(stopwords.words("english"))
    except LookupError:
        nltk.download("stopwords", quiet=True)
        STOPWORDS = set(stopwords.words("english"))
except ImportError:
    STOPWORDS = set()
    print("[WARNING] nltk not found. Stopword removal skipped.")


# ── Text preprocessing ────────────────────────────────────────────────────────

def clean_text(text: str) -> str:
    """Lowercase, remove punctuation, collapse whitespace."""
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> list[str]:
    """Simple whitespace tokenizer after cleaning."""
    tokens = clean_text(text).split()
    tokens = [t for t in tokens if len(t) > 2 and t not in STOPWORDS]
    return tokens


# ── Load text data ────────────────────────────────────────────────────────────

def load_text_monthly(path: pathlib.Path) -> pd.DataFrame:
    """Load text_monthly.parquet, deserialize response lists."""
    df = pd.read_parquet(path)
    # Deserialize: responses were stored as \x00-joined strings
    df["responses"] = df["responses"].apply(lambda x: x.split("\x00"))
    df["responses_clean"] = df["responses"].apply(
        lambda lst: [clean_text(r) for r in lst if isinstance(r, str) and r.strip()]
    )
    df["tokens_per_response"] = df["responses_clean"].apply(
        lambda lst: [tokenize(r) for r in lst]
    )
    return df


# ── V — Volatility (text) ────────────────────────────────────────────────────

def compute_v_text(monthly: pd.DataFrame) -> pd.Series:
    """
    V_text = Jaccard distance between top-20 tokens in month t and t-1.
    Jaccard distance = 1 - |A∩B| / |A∪B|
    """
    def top20(responses_clean: list[str]) -> set[str]:
        all_tokens = []
        for r in responses_clean:
            all_tokens.extend(tokenize(r))
        if not all_tokens:
            return set()
        counts = Counter(all_tokens)
        return set(w for w, _ in counts.most_common(20))

    monthly = monthly.copy()
    monthly["top20"] = monthly["responses_clean"].apply(top20)

    jaccard = []
    dates = monthly.index.tolist()
    for i, date in enumerate(dates):
        if i == 0:
            jaccard.append(np.nan)
            continue
        a = monthly.loc[dates[i - 1], "top20"]
        b = monthly.loc[date, "top20"]
        if not a and not b:
            jaccard.append(np.nan)
        elif not a or not b:
            jaccard.append(1.0)
        else:
            jaccard.append(1 - len(a & b) / len(a | b))

    series = pd.Series(jaccard, index=monthly.index, name="V_text")
    print(f"[V_text] Non-null: {series.notna().sum()} months")
    print(f"[V_text] Mean: {series.mean():.3f}, SD: {series.std():.3f}")
    return series


# ── U — Uncertainty (text) ───────────────────────────────────────────────────

def compute_u_text(monthly: pd.DataFrame) -> pd.Series:
    """
    U_text = % responses per month containing ≥1 word from UNCERTAINTY_WORDS.
    """
    word_set = set(dicts.UNCERTAINTY_WORDS)

    def hit_rate(responses_clean: list[str]) -> float:
        if not responses_clean:
            return np.nan
        hits = sum(
            1 for r in responses_clean
            if any(w in r for w in word_set)
        )
        return hits / len(responses_clean)

    series = monthly["responses_clean"].apply(hit_rate)
    series.name = "U_text"
    print(f"[U_text] Non-null: {series.notna().sum()} months")
    print(f"[U_text] Mean: {series.mean():.3f}, SD: {series.std():.3f}")
    return series


# ── C — Complexity (LDA-based) ────────────────────────────────────────────────

def fit_lda_model(monthly: pd.DataFrame):
    """
    Fit LDA on pooled corpus (all months), return model + vectorizer.
    Topic shares are then extracted per-month.
    """
    if not HAS_SKLEARN:
        return None, None

    print(f"\n[C_text] Fitting LDA (K={config.LDA_N_TOPICS}) on pooled corpus...")
    all_docs = []
    for responses in monthly["responses_clean"]:
        # One document per response
        all_docs.extend(responses)

    if not all_docs:
        print("[C_text] No text documents found.")
        return None, None

    vectorizer = CountVectorizer(
        max_features=5000,
        min_df=5,
        max_df=0.95,
        stop_words="english",
    )
    dtm = vectorizer.fit_transform(all_docs)
    print(f"[C_text] Corpus: {len(all_docs)} docs, vocab: {dtm.shape[1]} terms")

    lda = LatentDirichletAllocation(
        n_components=config.LDA_N_TOPICS,
        max_iter=config.LDA_MAX_ITER,
        random_state=config.RANDOM_SEED,
        n_jobs=-1,
    )
    lda.fit(dtm)
    print("[C_text] LDA fitting complete.")
    return lda, vectorizer


def compute_c_measures(monthly: pd.DataFrame, lda, vectorizer) -> tuple[pd.Series, pd.Series]:
    """
    Compute C_text and C_quant from LDA topic shares.

    C_text  = mean per-response Shannon entropy of topic distribution
    C_quant = 1 - variance_explained[PC1] over rolling 12-month window of
              monthly mean topic share vectors
    """
    if lda is None or vectorizer is None:
        nan_series = pd.Series(np.nan, index=monthly.index)
        return nan_series.rename("C_text"), nan_series.rename("C_quant")

    # Per-month: transform each response, compute entropy, average
    monthly_topic_means = []
    monthly_c_text = []

    n_errors = 0
    for date in monthly.index:
        # Use .at[] to avoid iterrows() type-coercion of list columns
        responses = monthly.at[date, "responses_clean"]
        if not responses:
            monthly_topic_means.append(np.full(config.LDA_N_TOPICS, np.nan))
            monthly_c_text.append(np.nan)
            continue

        # Ensure responses is a plain list of strings
        responses = [str(r) for r in list(responses) if r]

        try:
            dtm_month = vectorizer.transform(responses)
            topic_dist = lda.transform(dtm_month)  # (n_responses, K)

            def entropy(p):
                p = p + 1e-10
                return -np.sum(p * np.log(p))

            entropies = np.apply_along_axis(entropy, 1, topic_dist)
            monthly_c_text.append(float(np.mean(entropies)))
            monthly_topic_means.append(topic_dist.mean(axis=0))

        except Exception as e:
            if n_errors < 3:  # print first 3 errors to diagnose without flooding
                print(f"  [C_text] WARNING month {date}: {type(e).__name__}: {e}")
            n_errors += 1
            monthly_c_text.append(np.nan)
            monthly_topic_means.append(np.full(config.LDA_N_TOPICS, np.nan))

    if n_errors:
        print(f"  [C_text] Total months with errors: {n_errors}/{len(monthly)}")

    c_text = pd.Series(monthly_c_text, index=monthly.index, name="C_text")

    # C_quant: rolling PCA on topic share matrix
    topic_df = pd.DataFrame(
        monthly_topic_means,
        index=monthly.index,
        columns=[f"topic_{i}" for i in range(config.LDA_N_TOPICS)]
    )

    window = 12
    c_quant_vals = []
    dates = topic_df.index.tolist()

    for i, date in enumerate(dates):
        start = max(0, i - window + 1)
        window_data = topic_df.iloc[start:i + 1].dropna()
        if len(window_data) < 4:
            c_quant_vals.append(np.nan)
            continue
        try:
            pca = PCA(n_components=1, random_state=config.RANDOM_SEED)
            pca.fit(window_data)
            var_pc1 = pca.explained_variance_ratio_[0]
            c_quant_vals.append(1 - var_pc1)  # inverse: less PC1 dominance = more complexity
        except Exception:
            c_quant_vals.append(np.nan)

    c_quant = pd.Series(c_quant_vals, index=topic_df.index, name="C_quant")

    print(f"[C_text] Non-null: {c_text.notna().sum()} months, Mean: {c_text.mean():.3f}")
    print(f"[C_quant] Non-null: {c_quant.notna().sum()} months, Mean: {c_quant.mean():.3f}")
    return c_text, c_quant


# ── A — Ambiguity (text) ──────────────────────────────────────────────────────

def compute_a_polarity_conflict(monthly: pd.DataFrame) -> pd.Series:
    """
    A_polarity_conflict = % responses per month containing BOTH
    positive and negative tokens.
    """
    pos_set = set(dicts.POSITIVE_WORDS)
    neg_set = set(dicts.NEGATIVE_WORDS)

    def conflict_rate(responses_clean: list[str]) -> float:
        if not responses_clean:
            return np.nan
        n_conflict = 0
        for r in responses_clean:
            tokens = set(tokenize(r))
            has_pos = bool(tokens & pos_set)
            has_neg = bool(tokens & neg_set)
            if has_pos and has_neg:
                n_conflict += 1
        return n_conflict / len(responses_clean)

    series = monthly["responses_clean"].apply(conflict_rate)
    series.name = "A_polarity_conflict"
    print(f"[A_polarity_conflict] Non-null: {series.notna().sum()} months")
    print(f"[A_polarity_conflict] Mean: {series.mean():.3f}, SD: {series.std():.3f}")
    return series


def compute_a_phrase_rate(monthly: pd.DataFrame) -> pd.Series:
    """
    A_phrase_rate = % responses per month containing ≥1 ambiguity phrase.
    """
    phrases = dicts.AMBIGUITY_PHRASES  # all lowercase

    def phrase_rate(responses_clean: list[str]) -> float:
        if not responses_clean:
            return np.nan
        hits = sum(
            1 for r in responses_clean
            if any(ph in r for ph in phrases)
        )
        return hits / len(responses_clean)

    series = monthly["responses_clean"].apply(phrase_rate)
    series.name = "A_phrase_rate"
    print(f"[A_phrase_rate] Non-null: {series.notna().sum()} months")
    print(f"[A_phrase_rate] Mean: {series.mean():.3f}, SD: {series.std():.3f}")
    return series


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("02_text_vuca.py — Text-Based VUCA Measures")
    print("=" * 60)

    if not config.TEXT_MONTHLY_FILE.exists():
        raise FileNotFoundError(
            f"Text monthly file not found: {config.TEXT_MONTHLY_FILE}\n"
            "Run 00_load_data.py first."
        )

    monthly = load_text_monthly(config.TEXT_MONTHLY_FILE)
    print(f"\n[INPUT] Text monthly: {monthly.shape}")
    print(f"[INPUT] Date range: {monthly.index[0]} → {monthly.index[-1]}")

    # Compute all text measures
    print("\n--- V_text ---")
    v_text = compute_v_text(monthly)

    print("\n--- U_text ---")
    u_text = compute_u_text(monthly)

    print("\n--- C_text + C_quant (LDA) ---")
    lda, vectorizer = fit_lda_model(monthly)
    c_text, c_quant = compute_c_measures(monthly, lda, vectorizer)

    print("\n--- A_polarity_conflict ---")
    a_polarity = compute_a_polarity_conflict(monthly)

    print("\n--- A_phrase_rate ---")
    a_phrase = compute_a_phrase_rate(monthly)

    # Combine
    out = pd.DataFrame({
        "V_text": v_text,
        "U_text": u_text,
        "C_text": c_text,
        "C_quant": c_quant,
        "A_polarity_conflict": a_polarity,
        "A_phrase_rate": a_phrase,
    })

    print(f"\n[OUTPUT] Text measures shape: {out.shape}")
    print("\n[OUTPUT] Summary (non-null counts):")
    print(out.notna().sum().to_string())
    print("\n[OUTPUT] Descriptive statistics:")
    print(out.describe().round(3).to_string())

    # Spot check at key events
    print("\n[SPOT CHECK] Values at key events:")
    events = ["2019-05", "2020-03", "2022-03"]
    for e in events:
        try:
            row = out.loc[e]
            if isinstance(row, pd.DataFrame):
                row = row.iloc[0]
            print(f"  {e}: V_text={row['V_text']:.3f}, U_text={row['U_text']:.3f}, "
                  f"A_polarity={row['A_polarity_conflict']:.3f}")
        except KeyError:
            print(f"  {e}: not in index")

    # Save
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out.to_parquet(config.TEXT_MEASURES_FILE)
    print(f"\n[SAVED] {config.TEXT_MEASURES_FILE}")
    print("  Next: python scripts/03_combine_standardize.py")


if __name__ == "__main__":
    main()
