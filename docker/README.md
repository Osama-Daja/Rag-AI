# Docker

Local supporting services for Rag-AI.

## Services

| Service | Port | Compose file |
|---------|------|--------------|
| Qdrant | `6333` (REST), `6334` (gRPC) | `docker-compose.yml` |

Ollama is not in Compose — install and run it natively.

## Start / stop

From repo root:

```bat
scripts\start-qdrant.bat
scripts\stop-qdrant.bat
```

Or:

```bat
docker compose -f docker\docker-compose.yml up -d
docker compose -f docker\docker-compose.yml down
```

Dashboard/API: http://localhost:6333/dashboard
