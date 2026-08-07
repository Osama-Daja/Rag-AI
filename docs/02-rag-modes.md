# RAG modes

All modes share one chat. The difference is the pipeline behind `mode`.

| Mode | Idea | Status |
|------|------|--------|
| `simple` | Embed query → top-k from Qdrant → prompt → Ollama | First to build |
| `hybrid` | Dense (vectors) + sparse/keyword fusion | Planned |
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

Each folder has a README. Implementation code comes later, mode by mode.

## Registry idea

```text
PIPELINES = {
  "simple": SimpleRagPipeline,
  # "hybrid": HybridRagPipeline,
  # ...
}
```

UI only enables modes registered and ready on the backend.

## When to use which (later)

- **simple** — baseline Q&A over docs
- **hybrid** — better keyword + semantic recall
- **multi_hop** — questions needing several facts chained
- **agentic** — open-ended tasks needing tool loops
- **graph** — relationship-heavy knowledge
