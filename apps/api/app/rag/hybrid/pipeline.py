from __future__ import annotations

from typing import Any, Optional

from app.api.deps import get_ollama_client, get_qdrant_service
from app.core.config import get_settings
from app.rag.hybrid.bm25 import bm25_rank
from app.rag.hybrid.fusion import reciprocal_rank_fusion
from app.rag.simple.prompt import SYSTEM_PROMPT, build_user_prompt
from app.schemas.chat import ChatResponse, Source


class HybridRagPipeline:
    mode = "hybrid"

    def __init__(self) -> None:
        self._settings = get_settings()
        self._ollama = get_ollama_client()
        self._qdrant = get_qdrant_service()

    async def run(
        self,
        message: str,
        *,
        conversation_id: Optional[str] = None,
    ) -> ChatResponse:
        del conversation_id  # reserved for later phases

        candidate_k = max(1, self._settings.rag_hybrid_candidate_k)
        top_k = max(1, self._settings.rag_top_k)

        vectors = await self._ollama.embed([message])
        dense_hits = await self._qdrant.search(vectors[0], limit=candidate_k)
        dense_ids = [str(hit["id"]) for hit in dense_hits]

        scrolled = await self._qdrant.scroll_texts(
            limit=self._settings.rag_hybrid_scroll_limit
        )
        documents = [
            {
                "id": str(item["id"]),
                "text": str((item.get("payload") or {}).get("text") or ""),
            }
            for item in scrolled
        ]
        bm25_ids = bm25_rank(message, documents, limit=candidate_k)

        fused_ids = reciprocal_rank_fusion([dense_ids, bm25_ids])[:top_k]

        by_id: dict[str, dict[str, Any]] = {}
        for hit in dense_hits:
            by_id[str(hit["id"])] = hit
        for item in scrolled:
            doc_id = str(item["id"])
            if doc_id not in by_id:
                by_id[doc_id] = {
                    "id": doc_id,
                    "score": None,
                    "payload": item.get("payload") or {},
                }

        preview = max(120, self._settings.rag_source_preview_chars)
        contexts: list[str] = []
        sources: list[Source] = []
        for doc_id in fused_ids:
            hit = by_id.get(doc_id)
            if hit is None:
                continue
            payload = hit.get("payload") or {}
            text = str(payload.get("text") or "")
            if text:
                contexts.append(text if len(text) <= preview else f"{text[:preview]}…")
            sources.append(
                Source(
                    id=doc_id,
                    text=text,
                    score=hit.get("score"),
                )
            )

        user_prompt = build_user_prompt(message, contexts)
        answer = await self._ollama.chat(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ]
        )

        return ChatResponse(answer=answer, mode="hybrid", sources=sources)
