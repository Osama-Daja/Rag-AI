from pydantic import BaseModel


class IngestResponse(BaseModel):
    filename: str
    chunks_upserted: int
    collection: str
