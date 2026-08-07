from typing import Literal, Optional

from pydantic import BaseModel, Field


class IngestResponse(BaseModel):
    filename: str
    chunks_upserted: int
    collection: str


class ScanFileResult(BaseModel):
    filename: str
    chunks_upserted: int = 0
    status: Literal["ok", "failed"]
    error: Optional[str] = None


class ScanFolderResponse(BaseModel):
    scanned: int
    ingested: int
    failed: int
    results: list[ScanFileResult] = Field(default_factory=list)
