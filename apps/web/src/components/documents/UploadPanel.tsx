"use client";

import { useState, type ChangeEvent } from "react";

import { ingestDocument, scanRawFolder } from "@/lib/api";
import type { IngestResponse, ScanFolderResponse } from "@/types/rag";

import styles from "./UploadPanel.module.css";

export function UploadPanel() {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isScanning, setIsScanning] = useState(false);
  const [status, setStatus] = useState<string | null>(null);
  const [result, setResult] = useState<IngestResponse | null>(null);
  const [scanResult, setScanResult] = useState<ScanFolderResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const busy = isUploading || isScanning;

  function onFileChange(event: ChangeEvent<HTMLInputElement>) {
    const next = event.target.files?.[0] ?? null;
    setFile(next);
    setResult(null);
    setScanResult(null);
    setError(null);
    setStatus(null);
  }

  async function onUpload() {
    if (!file || busy) {
      return;
    }
    setIsUploading(true);
    setError(null);
    setResult(null);
    setScanResult(null);
    setStatus("Scanning and embedding with Ollama…");
    try {
      const response = await ingestDocument(file);
      setResult(response);
      setStatus(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
      setStatus(null);
    } finally {
      setIsUploading(false);
    }
  }

  async function onScanFolder() {
    if (busy) {
      return;
    }
    setIsScanning(true);
    setError(null);
    setResult(null);
    setScanResult(null);
    setStatus("Scanning data/raw and embedding files…");
    try {
      const response = await scanRawFolder();
      setScanResult(response);
      setStatus(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Folder scan failed");
      setStatus(null);
    } finally {
      setIsScanning(false);
    }
  }

  return (
    <section className={styles.root} aria-label="Document upload">
      <h2 className={styles.title}>Documents</h2>
      <p className={styles.copy}>
        Upload `.txt`, `.md`, or `.pdf`, or scan everything in <code>data/raw</code>.
      </p>
      <input
        className={styles.input}
        type="file"
        accept=".txt,.md,.pdf,text/plain,text/markdown,application/pdf"
        onChange={onFileChange}
        disabled={busy}
      />
      <div className={styles.actions}>
        <button
          type="button"
          className={styles.button}
          onClick={() => void onUpload()}
          disabled={!file || busy}
        >
          {isUploading ? "Uploading…" : "Ingest"}
        </button>
        <button
          type="button"
          className={styles.secondary}
          onClick={() => void onScanFolder()}
          disabled={busy}
        >
          {isScanning ? "Scanning…" : "Scan folder"}
        </button>
      </div>
      {status ? <p className={styles.status}>{status}</p> : null}
      {result ? (
        <p className={styles.success}>
          Indexed {result.chunks_upserted} chunk(s) from {result.filename} into{" "}
          {result.collection}.
        </p>
      ) : null}
      {scanResult ? (
        <p className={styles.success}>
          Scanned {scanResult.scanned} file(s): {scanResult.ingested} ingested,{" "}
          {scanResult.failed} failed.
        </p>
      ) : null}
      {scanResult && scanResult.failed > 0 ? (
        <ul className={styles.failures}>
          {scanResult.results
            .filter((item) => item.status === "failed")
            .map((item) => (
              <li key={item.filename}>
                {item.filename}: {item.error}
              </li>
            ))}
        </ul>
      ) : null}
      {error ? (
        <p className={styles.error} role="alert">
          {error}
        </p>
      ) : null}
    </section>
  );
}
