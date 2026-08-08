from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SearchAction:
    query: str


@dataclass(frozen=True)
class FinishAction:
    answer: str


@dataclass(frozen=True)
class InvalidAction:
    reason: str


AgentAction = SearchAction | FinishAction | InvalidAction

_ACTION_RE = re.compile(r"^\s*ACTION\s*:\s*(search|finish)\s*$", re.IGNORECASE | re.MULTILINE)
_QUERY_RE = re.compile(r"^\s*QUERY\s*:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
_ANSWER_RE = re.compile(
    r"^\s*ANSWER\s*:\s*(.+?)(?:\n\s*(?:ACTION|QUERY)\s*:|$)",
    re.IGNORECASE | re.MULTILINE | re.DOTALL,
)


def _strip_wrapping_quotes(text: str) -> str:
    cleaned = text.strip().strip("\"'`")
    return cleaned.strip()


def parse_action(raw: str) -> AgentAction:
    text = (raw or "").strip()
    if not text:
        return InvalidAction(reason="empty model output")

    action_match = _ACTION_RE.search(text)
    if action_match is None:
        # Fallback: treat a plain non-empty reply as finish answer.
        return FinishAction(answer=text)

    kind = action_match.group(1).lower()
    if kind == "search":
        query_match = _QUERY_RE.search(text)
        if query_match is None:
            return InvalidAction(reason="search action missing QUERY")
        query = _strip_wrapping_quotes(query_match.group(1))
        if not query:
            return InvalidAction(reason="empty search query")
        return SearchAction(query=query)

    answer_match = _ANSWER_RE.search(text)
    if answer_match is None:
        # ACTION: finish without ANSWER line — use remainder after ACTION line.
        remainder = text[action_match.end() :].strip()
        remainder = re.sub(r"^\s*ANSWER\s*:\s*", "", remainder, flags=re.IGNORECASE).strip()
        answer = _strip_wrapping_quotes(remainder)
    else:
        answer = _strip_wrapping_quotes(answer_match.group(1))

    if not answer:
        return InvalidAction(reason="finish action missing ANSWER")
    return FinishAction(answer=answer)
