# Ollama and Qdrant

Local-only AI stack for Rag-AI.

## Ollama

| Item | Planned default |
|------|-----------------|
| Base URL | `http://localhost:11434` |
| Chat model | `llama3.2` (or your choice) |
| Embed model | `nomic-embed-text` |

Env names (later):

- `OLLAMA_BASE_URL`
- `OLLAMA_CHAT_MODEL`
- `OLLAMA_EMBED_MODEL`

Service code will live in `apps/api/app/services/ollama/`.

Typical use:

1. Embed chunks and queries
2. Chat completion with retrieved context

## Qdrant

| Item | Planned default |
|------|-----------------|
| URL | `http://localhost:6333` |
| Role | Vector store for chunk embeddings |

Env name (later):

- `QDRANT_URL`

Service code will live in `apps/api/app/services/qdrant/`.

Typical use:

1. Ensure collection exists (vector size matches embed model)
2. Upsert chunk points after ingest
3. Search top-k for the query vector

## Docker

Qdrant runs via Compose:

```bat
scripts\start-qdrant.bat
```

Compose file: `docker/docker-compose.yml` (ports `6333` / `6334`).

Ollama usually runs as a native local install; Compose is optional for Ollama.

## Rules

- Prefer Qdrant (not Chroma/FAISS)
- Prefer Ollama (no cloud keys for v1)
- Keep model and collection names in config, not hard-coded in pipelines
