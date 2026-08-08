from __future__ import annotations

import math
import re
from collections import Counter

_TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in _TOKEN_RE.findall(text)]


def bm25_rank(
    query: str,
    documents: list[dict[str, str]],
    *,
    limit: int,
    k1: float = 1.5,
    b: float = 0.75,
) -> list[str]:
    """Rank document ids by BM25 over their text. documents: [{id, text}]."""
    if not documents or limit <= 0:
        return []

    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    tokenized: list[tuple[str, list[str]]] = []
    for doc in documents:
        doc_id = doc.get("id")
        text = doc.get("text") or ""
        if not doc_id or not text:
            continue
        tokens = tokenize(text)
        if tokens:
            tokenized.append((doc_id, tokens))

    if not tokenized:
        return []

    doc_count = len(tokenized)
    avg_len = sum(len(tokens) for _, tokens in tokenized) / doc_count
    df: Counter[str] = Counter()
    for _, tokens in tokenized:
        df.update(set(tokens))

    scores: list[tuple[str, float]] = []
    query_tf = Counter(query_tokens)
    for doc_id, tokens in tokenized:
        tf = Counter(tokens)
        doc_len = len(tokens)
        score = 0.0
        for term, q_weight in query_tf.items():
            term_df = df.get(term, 0)
            if term_df == 0:
                continue
            idf = math.log(1.0 + (doc_count - term_df + 0.5) / (term_df + 0.5))
            freq = tf.get(term, 0)
            denom = freq + k1 * (1.0 - b + b * doc_len / avg_len)
            score += q_weight * idf * ((freq * (k1 + 1.0)) / denom)
        if score > 0:
            scores.append((doc_id, score))

    scores.sort(key=lambda item: item[1], reverse=True)
    return [doc_id for doc_id, _ in scores[:limit]]
