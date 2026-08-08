from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_REPO_ROOT = Path(__file__).resolve().parents[4]
_DEFAULT_DATA_RAW = str(_REPO_ROOT / "data" / "raw")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ollama_base_url: str = "http://localhost:11434"
    ollama_chat_model: str = "llama3.2"
    ollama_embed_model: str = "nomic-embed-text"
    ollama_embed_dim: int = 768
    ollama_embed_batch_size: int = 32
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "rag_chunks"
    api_cors_origins: str = "http://localhost:3000"
    rag_chunk_size: int = 1200
    rag_chunk_overlap: int = 150
    rag_top_k: int = 4
    rag_source_preview_chars: int = 500
    rag_hybrid_candidate_k: int = 12
    rag_hybrid_scroll_limit: int = 2000
    rag_multi_hop_top_k: int = 4
    data_raw_dir: str = _DEFAULT_DATA_RAW

    def model_post_init(self, __context: object) -> None:
        # Machine env can inject spaced/odd values that break Qdrant lookups.
        object.__setattr__(self, "qdrant_collection", self.qdrant_collection.strip())
        object.__setattr__(self, "qdrant_url", self.qdrant_url.strip())
        object.__setattr__(self, "ollama_base_url", self.ollama_base_url.strip())
        object.__setattr__(self, "ollama_embed_model", self.ollama_embed_model.strip())
        object.__setattr__(self, "ollama_chat_model", self.ollama_chat_model.strip())

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.api_cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
