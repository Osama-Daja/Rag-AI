"use client";

import { useChat } from "@/hooks/useChat";

import styles from "./ChatWindow.module.css";
import { MessageInput } from "./MessageInput";
import { MessageList } from "./MessageList";
import { ModeSwitcher } from "./ModeSwitcher";

export function ChatWindow() {
  const { messages, mode, isSending, status, error, setMode, sendMessage, clearError } =
    useChat();

  return (
    <section className={styles.root} aria-label="Chat">
      <div className={styles.header}>
        <h2 className={styles.title}>Chat</h2>
        <ModeSwitcher mode={mode} onChange={setMode} />
      </div>
      <MessageList messages={messages} />
      {status ? <p className={styles.status}>{status}</p> : null}
      {error ? (
        <p className={styles.error} role="alert" onClick={clearError}>
          {error}
        </p>
      ) : null}
      <MessageInput disabled={isSending} onSend={sendMessage} />
    </section>
  );
}
