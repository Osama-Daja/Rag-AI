from fastapi import APIRouter, HTTPException

from app.rag.registry import UnsupportedModeError, get_pipeline
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest) -> ChatResponse:
    try:
        pipeline = get_pipeline(body.mode)
    except UnsupportedModeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return await pipeline.run(body.message, conversation_id=body.conversation_id)
