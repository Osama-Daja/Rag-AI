# Frontend (`apps/web`)

Next.js + TypeScript UI for Rag-AI.

## Status

Scaffolded. Minimal home page is live. Chat + ModeSwitcher come later.

## Run

From repo root:

```bat
scripts\start-web.bat
```

Or manually:

```bat
cd apps\web
npm install
npm run dev
```

- Web: http://localhost:3000

Copy `.env.example` → `.env.local` (the start script does this if missing).

## Layout

```text
src/
  app/                 Next app router pages
  components/
    chat/              ChatWindow, MessageList, MessageInput, ModeSwitcher
    documents/         UploadPanel
  hooks/               e.g. useChat
  lib/                 API client helpers
  types/               RagMode, ChatRequest, ChatResponse
```

## Job

- One chat surface
- ModeSwitcher for RAG modes
- Call FastAPI (`/chat`, ingest)
- Show answer + sources

## Owned by

Frontend agent — `.cursor/agents/FRONTEND.md`

## Does not belong here

- RAG retrieval logic
- Direct Ollama or Qdrant calls
