from __future__ import annotations

from typing import Optional

from app.api.deps import get_ollama_client, get_qdrant_service
from app.core.config import get_settings
from app.rag.simple.prompt import SYSTEM_PROMPT, build_user_prompt
from app.schemas.chat import ChatResponse, Source


class SimpleRagPipeline:
    mode = "simple"

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

        vectors = await self._ollama.embed([message])
        query_vector = vectors[0]
        hits = await self._qdrant.search(query_vector, limit=self._settings.rag_top_k)

        preview = max(120, self._settings.rag_source_preview_chars)
        contexts: list[str] = []
        sources: list[Source] = []
        for hit in hits:
            payload = hit.get("payload") or {}
            text = str(payload.get("text") or "")
            if text:
                # Shorter context keeps local chat generation faster.
                contexts.append(text if len(text) <= preview else f"{text[:preview]}…")
            sources.append(
                Source(
                    id=str(hit.get("id")),
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

        return ChatResponse(answer=answer, mode="simple", sources=sources)
