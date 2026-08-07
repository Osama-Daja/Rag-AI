"use client";

import { ChatWindow } from "@/components/chat/ChatWindow";
import { UploadPanel } from "@/components/documents/UploadPanel";

import styles from "./page.module.css";

export default function HomePage() {
  return (
    <main className={styles.page}>
      <div className={styles.shell}>
        <header className={styles.brand}>
          <h1 className={styles.brandName}>Rag-AI</h1>
          <p className={styles.tagline}>
            Local RAG chat with a mode switch — start with simple retrieval, grow into more.
          </p>
        </header>
        <div className={styles.grid}>
          <UploadPanel />
          <ChatWindow />
        </div>
      </div>
    </main>
  );
}
