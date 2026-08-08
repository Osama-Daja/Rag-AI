"use client";

import { useCallback, useState } from "react";

import { postChat } from "@/lib/api";
import type { ChatMessage, RagMode } from "@/types/rag";
import { ENABLED_MODES } from "@/types/rag";

function createId(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [mode, setModeState] = useState<RagMode>("simple");
  const [conversationId] = useState<string>(() => createId());
  const [isSending, setIsSending] = useState(false);
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const setMode = useCallback((next: RagMode) => {
    if (!ENABLED_MODES.includes(next)) {
      return;
    }
    setModeState(next);
  }, []);

  const clearError = useCallback(() => setError(null), []);

  const sendMessage = useCallback(
    async (text: string) => {
      const trimmed = text.trim();
      if (!trimmed || isSending) {
        return;
      }

      setError(null);
      const userMessage: ChatMessage = {
        id: createId(),
        role: "user",
        content: trimmed,
        mode,
      };
      setMessages((prev) => [...prev, userMessage]);
      setIsSending(true);
      setStatus(
        mode === "multi_hop" ? "Multi-hop retrieving…" : "Retrieving context…",
      );

      try {
        setStatus(
          mode === "multi_hop" ? "Multi-hop retrieving…" : "Thinking with Ollama…",
        );
        const response = await postChat({
          message: trimmed,
          mode,
          conversation_id: conversationId,
        });
        const assistantMessage: ChatMessage = {
          id: createId(),
          role: "assistant",
          content: response.answer,
          mode: response.mode,
          sources: response.sources,
        };
        setMessages((prev) => [...prev, assistantMessage]);
      } catch (err) {
        const message = err instanceof Error ? err.message : "Chat request failed";
        setError(message);
      } finally {
        setIsSending(false);
        setStatus(null);
      }
    },
    [conversationId, isSending, mode],
  );

  return {
    messages,
    mode,
    conversationId,
    isSending,
    status,
    error,
    setMode,
    sendMessage,
    clearError,
  };
}
