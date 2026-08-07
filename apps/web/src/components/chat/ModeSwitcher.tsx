"use client";

import { ALL_MODES, ENABLED_MODES, type RagMode } from "@/types/rag";

import styles from "./ModeSwitcher.module.css";

type ModeSwitcherProps = {
  mode: RagMode;
  onChange: (mode: RagMode) => void;
};

export function ModeSwitcher({ mode, onChange }: ModeSwitcherProps) {
  return (
    <div className={styles.root} role="group" aria-label="RAG mode">
      {ALL_MODES.map((item) => {
        const enabled = ENABLED_MODES.includes(item);
        const active = mode === item;
        return (
          <button
            key={item}
            type="button"
            className={`${styles.button} ${active ? styles.active : ""}`}
            disabled={!enabled}
            title={enabled ? item : `${item} — soon`}
            onClick={() => onChange(item)}
          >
            {item}
            {!enabled ? <span className={styles.soon}>soon</span> : null}
          </button>
        );
      })}
    </div>
  );
}
