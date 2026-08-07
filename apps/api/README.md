# Backend (`apps/api`)

FastAPI service for Rag-AI: ingest, chat, and pipeline registry.

## Status

Phase 4 complete: simple RAG ingest + `POST /chat`. Chat UI is Phase 5.

## Run

From repo root:

```bat
scripts\start-api.bat
```

- API: http://localhost:8000
- Health: http://localhost:8000/health
- Docs: http://localhost:8000/docs

## Endpoints

### Health

`GET /health` — API + Ollama + Qdrant status.

### Ingest (txt / md)

```bat
curl -X POST http://localhost:8000/documents/ingest -F "file=@sample.txt"
```

Saves to `data/raw`, chunks, embeds, upserts into Qdrant collection `rag_chunks`.

### Chat (simple RAG)

```bat
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d "{\"message\":\"What is in the document?\",\"mode\":\"simple\"}"
```

Other modes return `400` until implemented.

## Layout

```text
app/
  main.py
  api/
    deps.py
    routes/            health, documents, chat
  core/                config
  schemas/             chat, documents
  services/
    ollama/            embed + chat
    qdrant/            upsert + search
    chunking.py
    ingest.py
  rag/
    base.py
    registry.py
    simple/            active pipeline
```

## Owned by

- Wiring/routes: Backend agent — `.cursor/agents/BACKEND.md`
- Pipeline internals: RagAI agent — `.cursor/agents/RAGAI.md`
