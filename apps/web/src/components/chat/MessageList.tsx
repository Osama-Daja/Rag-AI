"use client";

import type { ChatMessage } from "@/types/rag";

import styles from "./MessageList.module.css";

type MessageListProps = {
  messages: ChatMessage[];
};

export function MessageList({ messages }: MessageListProps) {
  if (messages.length === 0) {
    return (
      <div className={styles.root}>
        <p className={styles.empty}>Ask about your uploaded documents.</p>
      </div>
    );
  }

  return (
    <div className={styles.root}>
      {messages.map((message) => {
        const isUser = message.role === "user";
        return (
          <div
            key={message.id}
            className={`${styles.row} ${isUser ? styles.user : styles.assistant}`}
          >
            <div
              className={`${styles.bubble} ${
                isUser ? styles.userBubble : styles.assistantBubble
              }`}
            >
              <div>{message.content}</div>
              {!isUser && message.mode ? (
                <div className={styles.meta}>mode: {message.mode}</div>
              ) : null}
              {!isUser && message.sources && message.sources.length > 0 ? (
                <ul className={styles.sources}>
                  {message.sources.map((source) => (
                    <li key={source.id}>
                      {source.text.slice(0, 160)}
                      {source.text.length > 160 ? "…" : ""}
                      {typeof source.score === "number"
                        ? ` (${source.score.toFixed(3)})`
                        : ""}
                    </li>
                  ))}
                </ul>
              ) : null}
            </div>
          </div>
        );
      })}
    </div>
  );
}
