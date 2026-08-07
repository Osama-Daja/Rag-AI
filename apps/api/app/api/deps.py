from functools import lru_cache

from app.core.config import get_settings
from app.services.ollama import OllamaClient
from app.services.qdrant import QdrantService


@lru_cache
def get_ollama_client() -> OllamaClient:
    return OllamaClient(get_settings())


@lru_cache
def get_qdrant_service() -> QdrantService:
    return QdrantService(get_settings())
