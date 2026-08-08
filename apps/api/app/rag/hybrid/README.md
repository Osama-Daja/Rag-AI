# Hybrid RAG

**Status:** active (Phase 6)

## Job

Dense vector search (Qdrant) + BM25 over chunk text payloads, fused with Reciprocal Rank Fusion (RRF), then generate.

## Flow

1. Embed query → dense search (`RAG_HYBRID_CANDIDATE_K`)
2. Scroll payloads → BM25 rank (`RAG_HYBRID_SCROLL_LIMIT`)
3. RRF fuse → take `RAG_TOP_K`
4. Prompt + Ollama chat (reuses simple prompts)

## Code

- `pipeline.py` — `HybridRagPipeline`
- `bm25.py` — in-process BM25 over scrolled texts
- `fusion.py` — reciprocal rank fusion

## Storage

No schema change. Same Qdrant points as simple: dense vector + `payload.text`. BM25 is query-time only.

## Depends on

- `services/ollama` — embed + chat
- `services/qdrant` — `search` + `scroll_texts`
- `rag/simple/prompt.py` — grounded prompts

## Owned by

RagAI agent — `.cursor/agents/RAGAI.md`
