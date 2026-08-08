# RAG modes

All modes share one chat. The difference is the pipeline behind `mode`.

| Mode | Idea | Status |
|------|------|--------|
| `simple` | Embed query → top-k from Qdrant → prompt → Ollama | Active |
| `hybrid` | Dense (vectors) + BM25 keyword fusion (RRF) | Active |
| `multi_hop` | Retrieve → reason → retrieve again → answer | Planned |
| `agentic` | LLM decides tools (search, re-query) | Planned |
| `graph` | Entity/relation graph + retrieval | Planned |

## Folder layout

```text
apps/api/app/rag/
  simple/
  agentic/
  hybrid/
  graph/
  multi_hop/
```

Each folder has a README. Remaining modes are implemented one by one.

## Registry

```text
PIPELINES = {
  "simple": SimpleRagPipeline,
  "hybrid": HybridRagPipeline,
}
```

UI only enables modes registered and ready on the backend (`ENABLED_MODES` in the web app).

## When to use which

- **simple** — baseline Q&A over docs
- **hybrid** — better keyword + semantic recall (exact terms, IDs, rare names)
- **multi_hop** — questions needing several facts chained
- **agentic** — open-ended tasks needing tool loops
- **graph** — relationship-heavy knowledge
