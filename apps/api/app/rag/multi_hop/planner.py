from __future__ import annotations

import re

PLANNER_SYSTEM_PROMPT = (
    "You write follow-up search queries for a retrieval system. "
    "Given a user question and context already retrieved, output exactly one "
    "search query that would find missing facts needed to answer. "
    "Do not answer the question. Do not explain. Output a single line only."
)


def build_planner_user_prompt(question: str, contexts: list[str]) -> str:
    if contexts:
        numbered = "\n".join(
            f"{index}. {snippet}" for index, snippet in enumerate(contexts, start=1)
        )
    else:
        numbered = "(no context retrieved yet)"
    return (
        f"Question: {question}\n\n"
        f"Retrieved context:\n{numbered}\n\n"
        "Follow-up search query:"
    )


def parse_follow_up(raw: str, *, fallback: str) -> str:
    """Normalize planner output; empty/NONE falls back so hop 2 still runs."""
    text = (raw or "").strip()
    if not text:
        return fallback.strip()

    # Prefer first non-empty line.
    for line in text.splitlines():
        candidate = line.strip()
        if candidate:
            text = candidate
            break

    text = text.strip("\"'`")
    text = re.sub(
        r"^(follow[- ]?up(\s+search)?\s+query|search\s+query|query)\s*[:\-]\s*",
        "",
        text,
        flags=re.IGNORECASE,
    ).strip()

    if not text or text.upper() in {"NONE", "N/A", "NA"}:
        return fallback.strip()
    return text
