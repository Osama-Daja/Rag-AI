# Rag-AI

Local RAG platform with **one chat** and a **mode switch** across RAG strategies.

## Stack

| Layer | Choice |
|-------|--------|
| Frontend | Next.js + TypeScript (`apps/web`) |
| Backend | FastAPI + Python (`apps/api`) |
| LLM / embeddings | Ollama (local) |
| Vector DB | Qdrant (local) |

## How to run (Windows)

Prereqs: Docker Desktop, Node.js, Python, Ollama (for later RAG).

```bat
start.bat
```

Or per part:

```bat
scripts\check-env.bat
scripts\start-qdrant.bat
scripts\start-api.bat
scripts\start-web.bat
```

| Service | URL |
|---------|-----|
| Web | http://localhost:3000 |
| API | http://localhost:8000 |
| Health | http://localhost:8000/health |
| Qdrant | http://localhost:6333 |

Stop Qdrant: `scripts\stop-qdrant.bat`

See [scripts/README.md](scripts/README.md) for details.

## RAG modes

`simple` · `agentic` · `hybrid` · `graph` · `multi_hop`

Start with **simple**. Other modes are planned folders with docs only until implemented.

## Repo map

```text
apps/web/          Frontend (chat + ModeSwitcher)
apps/api/          FastAPI + RAG pipelines
data/              Raw uploads and processed artifacts
docker/            Qdrant compose
scripts/           Windows start/stop helpers
docs/              Architecture and mode guides
.cursor/agents/    TeamLeader + specialist agents
```

## Agents (Cursor)

Talk to **TeamLeader** for anything. It routes work:

| Agent | File |
|-------|------|
| TeamLeader | `.cursor/agents/TEAM_LEADER.md` |
| Frontend | `.cursor/agents/FRONTEND.md` |
| Design | `.cursor/agents/DESIGN.md` |
| Backend | `.cursor/agents/BACKEND.md` |
| RagAI | `.cursor/agents/RAGAI.md` |

An always-on rule (`.cursor/rules/team-leader.mdc`) keeps TeamLeader active.

## Build phases

1. Folders + docs — done
2. Scaffold web + api + run scripts — done
3. Wire Qdrant + Ollama — done
4. Simple RAG pipeline — done
5. Chat UI + mode switch — done
6. Add other RAG modes one by one

## Env

See [`.env.example`](.env.example). Per-app copies:

- `apps/api/.env.example` → `apps/api/.env`
- `apps/web/.env.example` → `apps/web/.env.local`

No secrets required for local v1.

## Docs

See [docs/00-overview.md](docs/00-overview.md) to start.
