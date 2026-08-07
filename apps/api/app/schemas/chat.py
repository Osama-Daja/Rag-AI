from typing import Literal, Optional

from pydantic import BaseModel, Field

RagMode = Literal["simple", "agentic", "hybrid", "graph", "multi_hop"]


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    mode: RagMode = "simple"
    conversation_id: Optional[str] = None


class Source(BaseModel):
    id: str
    text: str
    score: Optional[float] = None


class ChatResponse(BaseModel):
    answer: str
    mode: RagMode
    sources: list[Source] = Field(default_factory=list)
