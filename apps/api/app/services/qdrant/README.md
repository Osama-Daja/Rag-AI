# Qdrant service

**Status:** active (Phase 3)

## Job

Vector store client for:

- Connectivity ping
- Ensure collection exists
- Upsert chunk embeddings
- Search top-k by vector
- Scroll payloads (for hybrid BM25)

## Config

- `QDRANT_URL` — `http://localhost:6333`
- `QDRANT_COLLECTION` — default `rag-ai-db`
- Vector size from `OLLAMA_EMBED_DIM` (default `768`)

## Code

- `client.py` — `QdrantService` (`ping`, `ensure_collection`, `upsert`, `search`, `scroll_texts`)
- Wired via `app.api.deps.get_qdrant_service`

## Payload convention

| Field | Meaning |
|-------|---------|
| `text` | Chunk text |
| `source` | Filename or path |
| `chunk_index` | Order within source |

## Used by

- `GET /health` (ping)
- Ingest + RAG pipelines (Phase 4+)

## Rules

- Prefer Qdrant (not Chroma/FAISS)
- Collection vector size must match the Ollama embed model
- Keep collection name(s) in config
