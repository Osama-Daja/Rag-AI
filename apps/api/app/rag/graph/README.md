# Graph RAG

**Status:** active (Phase 6)

## Job

Query-time entity/relation graph over seed chunks, expand neighbors, retrieve again, then answer.

## Flow

1. Dense seed retrieve (`RAG_GRAPH_SEED_K`)
2. LLM extracts JSON triples `{subject, relation, object}`
3. Build in-memory NetworkX graph
4. Expand 1-hop entities (`RAG_GRAPH_HOPS`)
5. Dense retrieve on expanded entity names (`RAG_GRAPH_EXPAND_K`)
6. Merge chunk contexts + triple lines → answer

No Neo4j / no ingest change. Empty triples → seed-only (like simple).

## Code

- `pipeline.py` — `GraphRagPipeline`
- `extract.py` — triple prompts + `parse_triples`
- `store.py` — graph build / seed / expand

## Config

- `RAG_GRAPH_SEED_K` — seed retrieve size (default `4`)
- `RAG_GRAPH_EXPAND_K` — expand retrieve size (default `4`)
- `RAG_GRAPH_HOPS` — neighbor hops (default `1`)

## Depends on

- `networkx`
- `services/ollama` — embed + chat
- `services/qdrant` — dense search
- `rag/simple/prompt.py` — final answer prompt

## Owned by

RagAI agent — `.cursor/agents/RAGAI.md`
