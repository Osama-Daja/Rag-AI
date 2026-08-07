# Backend (`apps/api`)

FastAPI service for Rag-AI: ingest, chat, and pipeline registry.

## Status

Phase 3 complete: Ollama + Qdrant clients wired. Health reports dependency status. RAG pipelines come next.

## Run

From repo root:

```bat
scripts\start-api.bat
```

Or manually:

```bat
cd apps\api
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API: http://localhost:8000
- Health: http://localhost:8000/health
- Docs: http://localhost:8000/docs

Copy `.env.example` → `.env` (the start script does this if missing).

### Health response

```json
{
  "status": "ok",
  "dependencies": {
    "ollama": { "ok": true },
    "qdrant": { "ok": true }
  }
}
```

`status` is `"degraded"` if either dependency is down (API still responds `200`).

## Layout

```text
app/
  main.py              FastAPI entry
  api/
    deps.py            Ollama/Qdrant DI helpers
    routes/            health, chat, documents
  core/                config, logging
  schemas/             Pydantic contracts
  services/
    ollama/            chat + embeddings client (active)
    qdrant/            vector upsert/search (active)
  rag/
    simple/            first pipeline
    agentic/           planned
    hybrid/            planned
    graph/             planned
    multi_hop/         planned
  db/                  optional persistence later
tests/
```

## Registry idea

Thin routes call `get_pipeline(mode)` then `pipeline.run(...)`.

## Target endpoints

- `GET /health` (implemented + dependency checks)
- `POST /documents/ingest` (later)
- `POST /chat` (later)

## Owned by

- Wiring/routes: Backend agent — `.cursor/agents/BACKEND.md`
- Pipeline internals: RagAI agent — `.cursor/agents/RAGAI.md`
