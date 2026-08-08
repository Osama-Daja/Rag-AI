# Frontend (`apps/web`)

Next.js + TypeScript UI for Rag-AI.

## Status

Phase 5–6: one chat surface, ModeSwitcher (`simple` + `hybrid` + `multi_hop`), document upload.

## Run

From repo root:

```bat
scripts\start-web.bat
```

- Web: http://localhost:3000
- Needs API at `NEXT_PUBLIC_API_URL` (default `http://localhost:8000`)

## Use

1. Upload a `.txt`, `.md`, or `.pdf` in **Documents**, or click **Scan folder** for `data/raw`
2. Keep mode on **simple** (other modes show “soon”)
3. Ask a question in **Chat**

## Layout

```text
src/
  app/
    layout.tsx          + globals.css (tokens)
    page.tsx            + page.module.css
  components/
    chat/               each TSX has sibling .module.css
    documents/          UploadPanel + .module.css
  hooks/useChat.ts
  lib/api.ts
  types/rag.ts
```

## CSS convention

Every UI `.tsx` has a sibling `.module.css`.  
`layout.tsx` uses `globals.css` only. Hooks/lib/types have no CSS.

## Agents

- Frontend — `.cursor/agents/FRONTEND.md`
- Design — `.cursor/agents/DESIGN.md`

## Does not belong here

- RAG retrieval logic
- Direct Ollama or Qdrant calls
