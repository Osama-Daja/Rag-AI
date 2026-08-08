from __future__ import annotations

from app.rag.base import RagPipeline
from app.rag.hybrid.pipeline import HybridRagPipeline
from app.rag.simple.pipeline import SimpleRagPipeline
from app.schemas.chat import RagMode

AVAILABLE_MODES: tuple[str, ...] = ("simple", "hybrid")

_PIPELINES: dict[str, type] = {
    "simple": SimpleRagPipeline,
    "hybrid": HybridRagPipeline,
}


class UnsupportedModeError(ValueError):
    def __init__(self, mode: str) -> None:
        available = ", ".join(AVAILABLE_MODES)
        super().__init__(f"Unsupported mode '{mode}'. Available: {available}")
        self.mode = mode


def get_pipeline(mode: RagMode | str) -> RagPipeline:
    cls = _PIPELINES.get(mode)
    if cls is None:
        raise UnsupportedModeError(str(mode))
    return cls()
