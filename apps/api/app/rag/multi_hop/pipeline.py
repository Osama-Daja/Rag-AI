from __future__ import annotations

from typing import Any, Optional

from app.api.deps import get_ollama_client, get_qdrant_service
from app.core.config import get_settings
from app.rag.multi_hop.planner import (
    PLANNER_SYSTEM_PROMPT,
    build_planner_user_prompt,
    parse_follow_up,
)
from app.rag.simple.prompt import SYSTEM_PROMPT, build_user_prompt
from app.schemas.chat import ChatResponse, Source


class MultiHopRagPipeline:
    mode = "multi_hop"

    def __init__(self) -> None:
        self._settings = get_settings()
        self._ollama = get_ollama_client()
        self._qdrant = get_qdrant_service()

    async def _retrieve(self, query: str, *, limit: int) -> list[dict[str, Any]]:
        vectors = await self._ollama.embed([query])
        return await self._qdrant.search(vectors[0], limit=limit)

    def _preview_text(self, text: str) -> str:
        preview = max(120, self._settings.rag_source_preview_chars)
        if len(text) <= preview:
            return text
        return f"{text[:preview]}…"

    def _hits_to_contexts_and_sources(
        self,
        hits: list[dict[str, Any]],
    ) -> tuple[list[str], list[Source]]:
        contexts: list[str] = []
        sources: list[Source] = []
        for hit in hits:
            payload = hit.get("payload") or {}
            text = str(payload.get("text") or "")
            if text:
                contexts.append(self._preview_text(text))
            sources.append(
                Source(
                    id=str(hit.get("id")),
                    text=text,
                    score=hit.get("score"),
                )
            )
        return contexts, sources

    async def run(
        self,
        message: str,
        *,
        conversation_id: Optional[str] = None,
    ) -> ChatResponse:
        del conversation_id  # reserved for later phases

        per_hop = max(1, self._settings.rag_multi_hop_top_k)
        # Over-fetch hop 2 so we can skip hop-1 ids and still fill the budget.
        hop2_fetch = max(per_hop * 2, per_hop + 2)
        final_cap = per_hop * 2

        hop1_hits = await self._retrieve(message, limit=per_hop)
        hop1_contexts, hop1_sources = self._hits_to_contexts_and_sources(hop1_hits)
        hop1_ids = {source.id for source in hop1_sources}

        planner_raw = await self._ollama.chat(
            [
                {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": build_planner_user_prompt(message, hop1_contexts),
                },
            ]
        )
        follow_up = parse_follow_up(planner_raw, fallback=message)

        hop2_hits_raw = await self._retrieve(follow_up, limit=hop2_fetch)
        hop2_hits: list[dict[str, Any]] = []
        for hit in hop2_hits_raw:
            hit_id = str(hit.get("id"))
            if hit_id in hop1_ids:
                continue
            hop2_hits.append(hit)
            if len(hop2_hits) >= per_hop:
                break

        _, hop2_sources = self._hits_to_contexts_and_sources(hop2_hits)

        merged_sources: list[Source] = []
        seen: set[str] = set()
        for source in hop1_sources + hop2_sources:
            if source.id in seen:
                continue
            seen.add(source.id)
            merged_sources.append(source)
            if len(merged_sources) >= final_cap:
                break

        contexts = [
            self._preview_text(source.text)
            for source in merged_sources
            if source.text
        ]

        answer = await self._ollama.chat(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": build_user_prompt(message, contexts),
                },
            ]
        )

        return ChatResponse(answer=answer, mode="multi_hop", sources=merged_sources)
