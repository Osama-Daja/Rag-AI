from __future__ import annotations

from typing import Any, Optional

from app.api.deps import get_ollama_client, get_qdrant_service
from app.core.config import get_settings
from app.rag.graph.extract import (
    EXTRACT_SYSTEM_PROMPT,
    build_extract_user_prompt,
    format_triple_lines,
    parse_triples,
)
from app.rag.graph.store import build_graph, expand_entities, seed_entities
from app.rag.simple.prompt import SYSTEM_PROMPT, build_user_prompt
from app.schemas.chat import ChatResponse, Source


class GraphRagPipeline:
    mode = "graph"

    def __init__(self) -> None:
        self._settings = get_settings()
        self._ollama = get_ollama_client()
        self._qdrant = get_qdrant_service()

    def _preview_text(self, text: str) -> str:
        preview = max(120, self._settings.rag_source_preview_chars)
        if len(text) <= preview:
            return text
        return f"{text[:preview]}…"

    async def _retrieve(self, query: str, *, limit: int) -> list[dict[str, Any]]:
        vectors = await self._ollama.embed([query])
        return await self._qdrant.search(vectors[0], limit=limit)

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

        seed_k = max(1, self._settings.rag_graph_seed_k)
        expand_k = max(1, self._settings.rag_graph_expand_k)
        hops = max(0, self._settings.rag_graph_hops)

        seed_hits = await self._retrieve(message, limit=seed_k)
        seed_contexts, seed_sources = self._hits_to_contexts_and_sources(seed_hits)
        seed_ids = {source.id for source in seed_sources}

        triples = []
        if seed_contexts:
            extract_raw = await self._ollama.chat(
                [
                    {"role": "system", "content": EXTRACT_SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": build_extract_user_prompt(seed_contexts),
                    },
                ]
            )
            triples = parse_triples(extract_raw)

        graph = build_graph(triples)
        seeds = seed_entities(message, triples)
        expanded = expand_entities(graph, seeds, hops=hops)

        expand_sources: list[Source] = []
        if expanded:
            expand_query = " ".join(expanded)
            # Over-fetch so we can skip seed ids and still fill expand_k.
            expand_hits_raw = await self._retrieve(
                expand_query,
                limit=max(expand_k * 2, expand_k + 2),
            )
            expand_hits: list[dict[str, Any]] = []
            for hit in expand_hits_raw:
                hit_id = str(hit.get("id"))
                if hit_id in seed_ids:
                    continue
                expand_hits.append(hit)
                if len(expand_hits) >= expand_k:
                    break
            _, expand_sources = self._hits_to_contexts_and_sources(expand_hits)

        merged_sources: list[Source] = []
        seen: set[str] = set()
        for source in seed_sources + expand_sources:
            if source.id in seen:
                continue
            seen.add(source.id)
            merged_sources.append(source)

        contexts = [
            self._preview_text(source.text)
            for source in merged_sources
            if source.text
        ]
        triple_lines = format_triple_lines(triples)
        if triple_lines:
            contexts.append("Graph relations:\n" + "\n".join(triple_lines))

        answer = await self._ollama.chat(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": build_user_prompt(message, contexts),
                },
            ]
        )

        return ChatResponse(answer=answer, mode="graph", sources=merged_sources)
