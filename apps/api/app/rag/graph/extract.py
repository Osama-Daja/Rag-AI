from __future__ import annotations

import json
import re
from dataclasses import dataclass

EXTRACT_SYSTEM_PROMPT = (
    "You extract entity-relation triples from text for a knowledge graph. "
    "Return ONLY a JSON array of objects with keys subject, relation, object. "
    "Use short entity names. No markdown, no commentary."
)


@dataclass(frozen=True)
class Triple:
    subject: str
    relation: str
    object: str


def build_extract_user_prompt(contexts: list[str]) -> str:
    if contexts:
        joined = "\n\n---\n\n".join(contexts)
    else:
        joined = "(no context)"
    return (
        f"Text:\n{joined}\n\n"
        "Return ONLY a JSON array like:\n"
        '[{"subject":"...","relation":"...","object":"..."}]'
    )


def _extract_json_array(raw: str) -> object | None:
    text = (raw or "").strip()
    if not text:
        return None

    fenced = re.search(r"```(?:json)?\s*(\[[\s\S]*?\])\s*```", text, re.IGNORECASE)
    if fenced:
        text = fenced.group(1).strip()
    else:
        start = text.find("[")
        end = text.rfind("]")
        if start != -1 and end != -1 and end > start:
            text = text[start : end + 1]

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def parse_triples(raw: str) -> list[Triple]:
    data = _extract_json_array(raw)
    if data is None:
        return []

    if isinstance(data, dict):
        for key in ("triples", "entities", "data", "results"):
            nested = data.get(key)
            if isinstance(nested, list):
                data = nested
                break
        else:
            return []

    if not isinstance(data, list):
        return []

    triples: list[Triple] = []
    seen: set[tuple[str, str, str]] = set()
    for item in data:
        if not isinstance(item, dict):
            continue
        subject = str(item.get("subject") or item.get("source") or "").strip()
        relation = str(item.get("relation") or item.get("predicate") or "").strip()
        obj = str(item.get("object") or item.get("target") or "").strip()
        if not subject or not relation or not obj:
            continue
        key = (subject.lower(), relation.lower(), obj.lower())
        if key in seen:
            continue
        seen.add(key)
        triples.append(Triple(subject=subject, relation=relation, object=obj))
    return triples


def format_triple_lines(triples: list[Triple]) -> list[str]:
    return [f"{t.subject} --{t.relation}--> {t.object}" for t in triples]
