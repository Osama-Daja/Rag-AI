# Ollama and Qdrant

Local-only AI stack for Rag-AI.

## Ollama

| Item | Default |
|------|---------|
| Base URL | `http://localhost:11434` |
| Chat model | `llama3.2` |
| Embed model | `nomic-embed-text` |
| Embed dim | `768` |

Env:

- `OLLAMA_BASE_URL`
- `OLLAMA_CHAT_MODEL`
- `OLLAMA_EMBED_MODEL`
- `OLLAMA_EMBED_DIM`

Client: `apps/api/app/services/ollama/client.py` (`OllamaClient`)

Methods: `ping`, `embed`, `chat`

## Qdrant

| Item | Default |
|------|---------|
| URL | `http://localhost:6333` |
| Collection | `rag_chunks` |
| Distance | Cosine |
| Role | Vector store for chunk embeddings |

Env:

- `QDRANT_URL`
- `QDRANT_COLLECTION`

Client: `apps/api/app/services/qdrant/client.py` (`QdrantService`)

Methods: `ping`, `ensure_collection`, `upsert`, `search`

Payload fields: `text`, `source`, `chunk_index`

## Health

`GET /health` reports:

```json
{
  "status": "ok | degraded",
  "dependencies": {
    "ollama": { "ok": true },
    "qdrant": { "ok": true }
  }
}
```

## Docker

Qdrant runs via Compose:

```bat
scripts\start-qdrant.bat
```

Compose file: `docker/docker-compose.yml` (ports `6333` / `6334`).

Ollama usually runs as a native local install.

## Rules

- Prefer Qdrant (not Chroma/FAISS)
- Prefer Ollama (no cloud keys for v1)
- Keep model and collection names in config, not hard-coded in pipelines
