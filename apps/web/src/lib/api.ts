import type {
  ChatRequest,
  ChatResponse,
  IngestResponse,
  ScanFolderResponse,
} from "@/types/rag";

export function getApiUrl(): string {
  return process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
}

async function readError(response: Response): Promise<string> {
  try {
    const data = (await response.json()) as { detail?: unknown };
    if (typeof data.detail === "string") {
      return data.detail;
    }
    return JSON.stringify(data.detail ?? data);
  } catch {
    return response.statusText || `HTTP ${response.status}`;
  }
}

export async function postChat(request: ChatRequest): Promise<ChatResponse> {
  const response = await fetch(`${getApiUrl()}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(await readError(response));
  }

  return (await response.json()) as ChatResponse;
}

export async function ingestDocument(file: File): Promise<IngestResponse> {
  const form = new FormData();
  form.append("file", file);

  const response = await fetch(`${getApiUrl()}/documents/ingest`, {
    method: "POST",
    body: form,
  });

  if (!response.ok) {
    throw new Error(await readError(response));
  }

  return (await response.json()) as IngestResponse;
}

export async function scanRawFolder(): Promise<ScanFolderResponse> {
  const response = await fetch(`${getApiUrl()}/documents/scan`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error(await readError(response));
  }

  return (await response.json()) as ScanFolderResponse;
}
