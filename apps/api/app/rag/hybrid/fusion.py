from __future__ import annotations

from collections import defaultdict


def reciprocal_rank_fusion(
    rank_lists: list[list[str]],
    *,
    k: int = 60,
) -> list[str]:
    """Fuse ranked id lists with Reciprocal Rank Fusion (higher is better)."""
    scores: dict[str, float] = defaultdict(float)
    for ranking in rank_lists:
        for rank, doc_id in enumerate(ranking, start=1):
            scores[doc_id] += 1.0 / (k + rank)

    return sorted(scores.keys(), key=lambda doc_id: scores[doc_id], reverse=True)
