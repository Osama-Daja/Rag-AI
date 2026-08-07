# Qdrant service

**Status:** planned

## Job

Vector store client for:

- Ensure collection exists
- Upsert chunk embeddings
- Search top-k by vector

## Planned config

- `QDRANT_URL` — `http://localhost:6333`

## Used by

- Ingest path (upsert)
- RAG pipelines (search)

## Rules

- Prefer Qdrant (not Chroma/FAISS)
- Collection vector size must match the Ollama embed model
- Keep collection name(s) in config
