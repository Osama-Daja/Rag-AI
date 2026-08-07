# Scripts

Windows helpers to run the Rag-AI local stack.

## Required tools

- Docker Desktop
- Node.js + npm
- Python 3.11+ full install (via `py` launcher preferred; embeddable Python without `venv` will fail)
- Ollama (needed for RAG phases; optional for scaffold smoke test)

## Scripts

| Script | Action |
|--------|--------|
| `check-env.bat` | Verify docker, node, npm, python; warn if ollama missing |
| `ensure-docker.bat` | Launch Docker Desktop if needed and wait until the engine is ready |
| `start-qdrant.bat` | Ensure Docker, then start Qdrant (or reuse whatever is on `:6333`) |
| `stop-qdrant.bat` | Stop Qdrant |
| `start-api.bat` | Create venv if needed, install deps, run FastAPI `:8000` |
| `start-web.bat` | `npm install` if needed, run Next.js `:3000` |
| `start-all.bat` | Ensure Docker + Qdrant, then open API + Web in new windows |

Root shortcut: [`start.bat`](../start.bat) → `scripts\start-all.bat`

## Quick start

```bat
start.bat
```

URLs after launch:

- Web: http://localhost:3000
- API: http://localhost:8000
- Health: http://localhost:8000/health
- Qdrant: http://localhost:6333
