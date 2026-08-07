"use client";

import { useState, type KeyboardEvent } from "react";

import styles from "./MessageInput.module.css";

type MessageInputProps = {
  disabled?: boolean;
  onSend: (message: string) => void | Promise<void>;
};

export function MessageInput({ disabled = false, onSend }: MessageInputProps) {
  const [value, setValue] = useState("");

  async function handleSend() {
    const next = value.trim();
    if (!next || disabled) {
      return;
    }
    setValue("");
    await onSend(next);
  }

  function onKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      void handleSend();
    }
  }

  return (
    <div className={styles.root}>
      <div className={styles.row}>
        <textarea
          className={styles.textarea}
          value={value}
          onChange={(event) => setValue(event.target.value)}
          onKeyDown={onKeyDown}
          placeholder="Ask a question about your documents…"
          disabled={disabled}
          rows={3}
        />
        <button
          type="button"
          className={styles.send}
          onClick={() => void handleSend()}
          disabled={disabled || !value.trim()}
        >
          Send
        </button>
      </div>
      <p className={styles.hint}>Enter to send · Shift+Enter for a new line</p>
    </div>
  );
}
