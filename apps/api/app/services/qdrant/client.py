from __future__ import annotations

import asyncio
from typing import Any
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.http.models import Distance, PointStruct, VectorParams

from app.core.config import Settings, get_settings


class QdrantServiceError(RuntimeError):
    """Raised when a Qdrant operation fails."""


class QdrantService:
    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._client = QdrantClient(
            url=self._settings.qdrant_url,
            check_compatibility=False,
        )

    @property
    def collection_name(self) -> str:
        return self._settings.qdrant_collection

    async def ping(self) -> bool:
        try:
            await asyncio.to_thread(self._client.get_collections)
            return True
        except Exception:
            return False

    async def ensure_collection(self, vector_size: int | None = None) -> None:
        size = vector_size or self._settings.ollama_embed_dim
        name = self.collection_name

        def _ensure() -> None:
            exists = self._client.collection_exists(collection_name=name)
            if exists:
                return
            self._client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(size=size, distance=Distance.COSINE),
            )

        try:
            await asyncio.to_thread(_ensure)
        except UnexpectedResponse as exc:
            raise QdrantServiceError(f"Failed to ensure collection '{name}': {exc}") from exc

    async def upsert(self, points: list[dict[str, Any]]) -> None:
        """Upsert points shaped as {id?, vector, payload}."""
        if not points:
            return

        structs: list[PointStruct] = []
        for point in points:
            vector = point.get("vector")
            if not isinstance(vector, list):
                raise QdrantServiceError("Each point requires a vector list")
            payload = point.get("payload") or {}
            if not isinstance(payload, dict):
                raise QdrantServiceError("Each point payload must be a dict")
            point_id = point.get("id") or str(uuid4())
            structs.append(PointStruct(id=point_id, vector=vector, payload=payload))

        def _upsert() -> None:
            self._client.upsert(collection_name=self.collection_name, points=structs)

        try:
            await asyncio.to_thread(_upsert)
        except UnexpectedResponse as exc:
            raise QdrantServiceError(f"Qdrant upsert failed: {exc}") from exc

    async def search(
        self,
        vector: list[float],
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        def _search() -> Any:
            return self._client.query_points(
                collection_name=self.collection_name,
                query=vector,
                limit=limit,
                with_payload=True,
            )

        try:
            response = await asyncio.to_thread(_search)
        except UnexpectedResponse as exc:
            raise QdrantServiceError(f"Qdrant search failed: {exc}") from exc

        points = getattr(response, "points", None) or []
        return [
            {
                "id": str(hit.id),
                "score": float(hit.score) if hit.score is not None else None,
                "payload": hit.payload or {},
            }
            for hit in points
        ]
