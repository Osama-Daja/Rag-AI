from __future__ import annotations

from typing import Any

import httpx

from app.core.config import Settings, get_settings


class OllamaError(RuntimeError):
    """Raised when an Ollama API call fails."""


class OllamaClient:
    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._base_url = self._settings.ollama_base_url.rstrip("/")

    @property
    def chat_model(self) -> str:
        return self._settings.ollama_chat_model

    @property
    def embed_model(self) -> str:
        return self._settings.ollama_embed_model

    async def ping(self) -> bool:
        try:
            async with httpx.AsyncClient(base_url=self._base_url, timeout=5.0) as client:
                response = await client.get("/api/tags")
                return response.status_code == 200
        except httpx.HTTPError:
            return False

    async def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        batch_size = max(1, self._settings.ollama_embed_batch_size)
        vectors: list[list[float]] = []

        async with httpx.AsyncClient(base_url=self._base_url, timeout=300.0) as client:
            for start in range(0, len(texts), batch_size):
                batch = texts[start : start + batch_size]
                try:
                    batch_vectors = await self._embed_batch(client, batch)
                except OllamaError:
                    # Older Ollama builds may lack /api/embed batching.
                    batch_vectors = await self._embed_legacy(client, batch)
                vectors.extend(batch_vectors)

        if len(vectors) != len(texts):
            raise OllamaError(
                f"Embedding count mismatch: expected {len(texts)}, got {len(vectors)}"
            )
        return vectors

    async def _embed_batch(
        self,
        client: httpx.AsyncClient,
        batch: list[str],
    ) -> list[list[float]]:
        response = await client.post(
            "/api/embed",
            json={"model": self.embed_model, "input": batch},
        )
        if response.status_code >= 400:
            raise OllamaError(
                f"Ollama embed failed ({response.status_code}): {response.text}"
            )
        data = response.json()
        embeddings = data.get("embeddings")
        if not isinstance(embeddings, list) or len(embeddings) != len(batch):
            raise OllamaError("Ollama /api/embed response missing embeddings list")
        for item in embeddings:
            if not isinstance(item, list):
                raise OllamaError("Ollama /api/embed returned a non-list vector")
        return embeddings

    async def _embed_legacy(
        self,
        client: httpx.AsyncClient,
        batch: list[str],
    ) -> list[list[float]]:
        vectors: list[list[float]] = []
        for text in batch:
            response = await client.post(
                "/api/embeddings",
                json={"model": self.embed_model, "prompt": text},
            )
            if response.status_code >= 400:
                raise OllamaError(
                    f"Ollama embed failed ({response.status_code}): {response.text}"
                )
            data = response.json()
            embedding = data.get("embedding")
            if not isinstance(embedding, list):
                raise OllamaError("Ollama embed response missing embedding list")
            vectors.append(embedding)
        return vectors

    async def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str | None = None,
    ) -> str:
        payload = {
            "model": model or self.chat_model,
            "messages": messages,
            "stream": False,
        }
        async with httpx.AsyncClient(base_url=self._base_url, timeout=180.0) as client:
            response = await client.post("/api/chat", json=payload)
            if response.status_code >= 400:
                raise OllamaError(
                    f"Ollama chat failed ({response.status_code}): {response.text}"
                )
            data = response.json()
            message = data.get("message") or {}
            content = message.get("content")
            if not isinstance(content, str):
                raise OllamaError("Ollama chat response missing message.content")
            return content
