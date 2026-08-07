from __future__ import annotations

from typing import Optional, Protocol

from app.schemas.chat import ChatResponse, RagMode


class RagPipeline(Protocol):
    mode: RagMode

    async def run(
        self,
        message: str,
        *,
        conversation_id: Optional[str] = None,
    ) -> ChatResponse: ...
