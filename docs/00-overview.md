# Overview

Rag-AI is a local monorepo for experimenting with multiple RAG strategies in **one chat UI**.

## Goals

- Run fully local: Ollama + Qdrant
- Switch RAG mode per message without leaving the chat
- Keep frontend, backend, and RAG logic cleanly separated
- Grow modes one folder at a time

## Stack

- **Web:** Next.js + TypeScript
- **API:** FastAPI + Python
- **Models:** Ollama (chat + embeddings)
- **Vectors:** Qdrant

## Phase roadmap

| Phase | Deliverable |
|-------|-------------|
| 1 | Folders, agents, docs — done |
| 2 | Scaffold `apps/web` and `apps/api` + run scripts — current |
| 3 | Qdrant + Ollama clients |
| 4 | Simple RAG (ingest + retrieve + generate) |
| 5 | Chat UI + ModeSwitcher |
| 6 | Hybrid, multi-hop, agentic, graph — one by one |

## How to run

From repo root on Windows:

```bat
start.bat
```

See root [README.md](../README.md) and [scripts/README.md](../scripts/README.md).

## Ownership

| Area | Specialist |
|------|------------|
| UI | Frontend agent |
| API wiring | Backend agent |
| Pipelines / vectors / prompts | RagAI agent |
| Routing all of the above | TeamLeader |

## Next read

- [01-architecture.md](01-architecture.md)
- [02-rag-modes.md](02-rag-modes.md)
- [03-ollama-qdrant.md](03-ollama-qdrant.md)
