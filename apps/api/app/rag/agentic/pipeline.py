from __future__ import annotations

from typing import Any, Optional

from app.api.deps import get_ollama_client, get_qdrant_service
from app.core.config import get_settings
from app.rag.agentic.actions import FinishAction, InvalidAction, SearchAction, parse_action
from app.rag.agentic.prompts import (
    AGENT_SYSTEM_PROMPT,
    build_agent_user_prompt,
    format_observation,
)
from app.rag.simple.prompt import SYSTEM_PROMPT, build_user_prompt
from app.schemas.chat import ChatResponse, Source


class AgenticRagPipeline:
    mode = "agentic"

    def __init__(self) -> None:
        self._settings = get_settings()
        self._ollama = get_ollama_client()
        self._qdrant = get_qdrant_service()

    def _preview_text(self, text: str) -> str:
        preview = max(120, self._settings.rag_source_preview_chars)
        if len(text) <= preview:
            return text
        return f"{text[:preview]}…"

    async def _search(self, query: str, *, limit: int) -> list[dict[str, Any]]:
        vectors = await self._ollama.embed([query])
        return await self._qdrant.search(vectors[0], limit=limit)

    def _hits_to_snippets_and_sources(
        self,
        hits: list[dict[str, Any]],
    ) -> tuple[list[str], list[Source]]:
        snippets: list[str] = []
        sources: list[Source] = []
        for hit in hits:
            payload = hit.get("payload") or {}
            text = str(payload.get("text") or "")
            if text:
                snippets.append(self._preview_text(text))
            sources.append(
                Source(
                    id=str(hit.get("id")),
                    text=text,
                    score=hit.get("score"),
                )
            )
        return snippets, sources

    def _merge_sources(
        self,
        existing: list[Source],
        incoming: list[Source],
    ) -> list[Source]:
        seen = {source.id for source in existing}
        merged = list(existing)
        for source in incoming:
            if source.id in seen:
                continue
            seen.add(source.id)
            merged.append(source)
        return merged

    async def _force_answer(self, question: str, sources: list[Source]) -> str:
        contexts = [
            self._preview_text(source.text) for source in sources if source.text
        ]
        return await self._ollama.chat(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": build_user_prompt(question, contexts),
                },
            ]
        )

    async def run(
        self,
        message: str,
        *,
        conversation_id: Optional[str] = None,
    ) -> ChatResponse:
        del conversation_id  # reserved for later phases

        max_steps = max(1, self._settings.rag_agentic_max_steps)
        top_k = max(1, self._settings.rag_agentic_top_k)

        observations: list[str] = []
        sources: list[Source] = []
        messages: list[dict[str, str]] = [
            {"role": "system", "content": AGENT_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": build_agent_user_prompt(message, observations),
            },
        ]

        for _ in range(max_steps):
            raw = await self._ollama.chat(messages)
            action = parse_action(raw)

            if isinstance(action, FinishAction):
                return ChatResponse(
                    answer=action.answer,
                    mode="agentic",
                    sources=sources,
                )

            if isinstance(action, SearchAction):
                hits = await self._search(action.query, limit=top_k)
                snippets, new_sources = self._hits_to_snippets_and_sources(hits)
                sources = self._merge_sources(sources, new_sources)
                observation = format_observation(snippets)
                observations.append(observation)
                messages.append({"role": "assistant", "content": raw})
                messages.append(
                    {
                        "role": "user",
                        "content": (
                            f"{observation}\n\n"
                            "Choose the next ACTION (search or finish):"
                        ),
                    }
                )
                continue

            # Invalid / unparseable — nudge once via user message, continue loop.
            reason = (
                action.reason if isinstance(action, InvalidAction) else "invalid action"
            )
            messages.append({"role": "assistant", "content": raw})
            messages.append(
                {
                    "role": "user",
                    "content": (
                        f"Invalid action ({reason}). "
                        "Reply using only:\n"
                        "ACTION: search\nQUERY: ...\n"
                        "or\n"
                        "ACTION: finish\nANSWER: ..."
                    ),
                }
            )

        answer = await self._force_answer(message, sources)
        return ChatResponse(answer=answer, mode="agentic", sources=sources)
