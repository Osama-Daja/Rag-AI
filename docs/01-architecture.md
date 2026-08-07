# Architecture

## High-level flow

```text
User (chat + mode)
    → apps/web (Next.js)          [Phase 5 UI]
    → POST /chat { message, mode }
    → apps/api (FastAPI)
    → rag registry (mode → pipeline)
    → pipeline uses Qdrant (retrieve) + Ollama (embed/chat)
    → ChatResponse { answer, mode, sources }
    → UI shows answer + sources
```

## Layers

| Layer | Path | Job |
|-------|------|-----|
| UI | `apps/web` | Chat, ModeSwitcher, upload (Phase 5) |
| Routes | `apps/api/app/api/routes` | Thin HTTP entry |
| Schemas | `apps/api/app/schemas` | Request/response contracts |
| Registry | `apps/api/app/rag` | Map `mode` → pipeline |
| Pipelines | `apps/api/app/rag/{mode}` | Mode-specific logic |
| Ollama | `apps/api/app/services/ollama` | Chat + embeddings |
| Qdrant | `apps/api/app/services/qdrant` | Upsert + search |
| Data | `data/raw`, `data/processed` | Files on disk |

## Mode switch

- UI stores current `mode` (Phase 5)
- Every chat request sends that `mode`
- Backend registry picks the pipeline
- Same conversation can use different modes across messages
- Currently registered: `simple` only

## Contracts (implemented)

```text
RagMode = simple | agentic | hybrid | graph | multi_hop

ChatRequest  { message, mode, conversation_id? }
ChatResponse { answer, mode, sources[] }
IngestResponse { filename, chunks_upserted, collection }
```

## Ingest flow (implemented)

```text
POST /documents/ingest (.txt / .md)
  → data/raw
  → chunk
  → embed (Ollama)
  → upsert (Qdrant rag_chunks)
```

## Chat flow (implemented)

```text
POST /chat { mode: "simple" }
  → SimpleRagPipeline
  → embed query → search → prompt → generate
```

## Design rules

- Routes stay thin
- Each RAG mode lives in its own folder
- No cloud LLM/vector APIs in v1
- Frontend never runs retrieval itself
