export type RagMode =
  | "simple"
  | "agentic"
  | "hybrid"
  | "graph"
  | "multi_hop";

export const ALL_MODES: RagMode[] = [
  "simple",
  "agentic",
  "hybrid",
  "graph",
  "multi_hop",
];

/** Modes currently supported by the backend registry. */
export const ENABLED_MODES: RagMode[] = [
  "simple",
  "hybrid",
  "multi_hop",
  "agentic",
];

export type ChatRequest = {
  message: string;
  mode: RagMode;
  conversation_id?: string;
};

export type Source = {
  id: string;
  text: string;
  score?: number;
};

export type ChatResponse = {
  answer: string;
  mode: RagMode;
  sources: Source[];
};

export type IngestResponse = {
  filename: string;
  chunks_upserted: number;
  collection: string;
};

export type ScanFileResult = {
  filename: string;
  chunks_upserted: number;
  status: "ok" | "failed";
  error?: string | null;
};

export type ScanFolderResponse = {
  scanned: number;
  ingested: number;
  failed: number;
  results: ScanFileResult[];
};

export type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
  mode?: RagMode;
  sources?: Source[];
};
