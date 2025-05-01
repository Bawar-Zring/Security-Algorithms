/* src/app.jsx */
import React, { useState } from "react";
import "./index.css";           // keep Vite’s default Tailwind/Vanilla CSS import if you like

const API = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export default function App() {
  // ── UI state ────────────────────────────────────────────────────────────────
  const [algo, setAlgo]   = useState("caesar");   // caesar | mono
  const [mode, setMode]   = useState("encrypt");  // encrypt | decrypt | attack
  const [shift, setShift] = useState(3);
  const [text, setText]   = useState("");
  const [result, setRes]  = useState(null);

  // ── API call ────────────────────────────────────────────────────────────────
  async function run(e) {
    e.preventDefault();
    const url = `/${algo}/${mode}`;
    const body =
      mode === "attack" ? { text } : { text, shift: Number(shift) };

    try {
      const r = await fetch(API + url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!r.ok) throw new Error(await r.text());
      setRes(await r.json());
    } catch (err) {
      setRes({ error: err.message });
    }
  }

  // ── JSX ─────────────────────────────────────────────────────────────────────
  return (
    <main className="p-6 space-y-5 max-w-3xl mx-auto font-sans">
      <h1 className="text-3xl font-bold">
        Caesar & Mono-alphabetic Cipher Playground
      </h1>

      <form onSubmit={run} className="space-y-4">
        {/* Algorithm & mode pickers */}
        <div className="space-x-3">
          <select
            value={algo}
            onChange={(e) => {
              const v = e.target.value;
              setAlgo(v);
              if (v === "mono" && mode === "attack") setMode("encrypt");
            }}
            className="border p-2 rounded"
          >
            <option value="caesar">Caesar</option>
            <option value="mono">Mono-alphabetic (shift)</option>
          </select>

          <select
            value={mode}
            onChange={(e) => setMode(e.target.value)}
            className="border p-2 rounded"
          >
            <option value="encrypt">Encrypt</option>
            <option value="decrypt">Decrypt</option>
            {algo === "caesar" && <option value="attack">Brute-force</option>}
          </select>
        </div>

        {/* Shift (hide during brute-force) */}
        {mode !== "attack" && (
          <input
            type="number"
            min="0"
            max="255"
            value={shift}
            onChange={(e) => setShift(e.target.value)}
            className="border p-2 rounded w-24"
            placeholder="Shift"
          />
        )}

        {/* Textarea */}
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows="4"
          className="w-full border p-2 rounded"
          placeholder="Enter text here"
        />

        <button
          type="submit"
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Run
        </button>
      </form>

      {/* Result panel */}
      {result && (
        <section className="border p-4 rounded bg-gray-50">
          {result.error && (
            <p className="text-red-600 font-semibold">{result.error}</p>
          )}

          {/* Brute-force candidates */}
          {mode === "attack" && result.candidates && (
            <div className="h-64 overflow-y-auto space-y-1 text-sm">
              {result.candidates.map(({ shift, plaintext }) => (
                <p key={shift}>
                  <span className="font-mono w-12 inline-block">{shift}:</span>
                  {plaintext}
                </p>
              ))}
            </div>
          )}

          {/* Encrypt / decrypt output */}
          {mode !== "attack" && (
            <pre className="whitespace-pre-wrap break-all">
              {result.ciphertext || result.plaintext}
            </pre>
          )}
        </section>
      )}
    </main>
  );
}
