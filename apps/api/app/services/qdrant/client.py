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


def _vector_size_from_collection(vectors_config: Any) -> int | None:
    """Read unnamed or single named vector size from collection config."""
    if vectors_config is None:
        return None
    size = getattr(vectors_config, "size", None)
    if isinstance(size, int):
        return size
    if isinstance(vectors_config, dict):
        if "size" in vectors_config and isinstance(vectors_config["size"], int):
            return vectors_config["size"]
        for value in vectors_config.values():
            nested = getattr(value, "size", None)
            if isinstance(nested, int):
                return nested
            if isinstance(value, dict) and isinstance(value.get("size"), int):
                return value["size"]
    return None


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
                info = self._client.get_collection(collection_name=name)
                current = _vector_size_from_collection(info.config.params.vectors)
                if current == size:
                    return
                # Wrong dim (e.g. 1024 vs 768) — recreate so ingest can succeed.
                self._client.delete_collection(collection_name=name)

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

    async def scroll_texts(self, limit: int | None = None) -> list[dict[str, Any]]:
        """Scroll collection points (id + payload) for keyword/BM25 retrieval."""
        name = self.collection_name
        max_points = limit if limit is not None else self._settings.rag_hybrid_scroll_limit
        if max_points <= 0:
            return []

        def _scroll() -> list[dict[str, Any]]:
            if not self._client.collection_exists(collection_name=name):
                return []

            collected: list[dict[str, Any]] = []
            next_offset: Any = None
            page_size = min(256, max_points)

            while len(collected) < max_points:
                remaining = max_points - len(collected)
                batch_limit = min(page_size, remaining)
                points, next_offset = self._client.scroll(
                    collection_name=name,
                    limit=batch_limit,
                    offset=next_offset,
                    with_payload=True,
                    with_vectors=False,
                )
                for point in points:
                    collected.append(
                        {
                            "id": str(point.id),
                            "payload": point.payload or {},
                        }
                    )
                if next_offset is None or not points:
                    break

            return collected

        try:
            return await asyncio.to_thread(_scroll)
        except UnexpectedResponse as exc:
            raise QdrantServiceError(f"Qdrant scroll failed: {exc}") from exc
