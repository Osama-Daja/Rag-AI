from typing import Any

from fastapi import APIRouter

from app.api.deps import get_ollama_client, get_qdrant_service

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, Any]:
    ollama_ok = await get_ollama_client().ping()
    qdrant_ok = await get_qdrant_service().ping()

    status = "ok" if ollama_ok and qdrant_ok else "degraded"
    return {
        "status": status,
        "dependencies": {
            "ollama": {"ok": ollama_ok},
            "qdrant": {"ok": qdrant_ok},
        },
    }
