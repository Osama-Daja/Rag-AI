export default function HomePage() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

  return (
    <main style={{ padding: "2rem", maxWidth: "40rem" }}>
      <h1 style={{ marginBottom: "0.5rem" }}>Rag-AI</h1>
      <p style={{ color: "#444" }}>Rag-AI web — scaffold ready</p>
      <p style={{ color: "#666", fontSize: "0.9rem" }}>
        API target: <code>{apiUrl}</code>
      </p>
    </main>
  );
}
