export type RagMode =
  | "simple"
  | "agentic"
  | "hybrid"
  | "graph"
  | "multi_hop";

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
