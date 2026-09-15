import { useState } from "react";
import Dropzone from "../components/Dropzone";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";
type Target = "yolo" | "coco" | "voc";

export default function Converter() {
  const [file, setFile] = useState<File | null>(null);
  const [target, setTarget] = useState<Target>("coco");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleConvert() {
    if (!file) return;
    setBusy(true);
    setError(null);

    try {
      const form = new FormData();
      form.append("file", file);
      form.append("target", target);

      const res = await fetch(`${API}/convert`, { method: "POST", body: form });
      if (!res.ok) {
        const d = await res.json().catch(() => ({}));
        throw new Error(d.detail || "Conversion failed");
      }

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${target}-annotations.zip`;
      a.click();
      URL.revokeObjectURL(url);

      setFile(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Conversion failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="mx-auto max-w-4xl space-y-6 px-6 py-10">
      <Dropzone
        onFile={setFile}
        disabled={busy}
        hint="Images plus annotations in any supported format"
      />

      {file && (
        <div className="rounded-xl border border-border bg-surface p-5">
          <p className="mb-4 text-sm text-ink">
            <span className="font-medium">{file.name}</span> ready to convert
          </p>

          <div className="flex flex-wrap items-center gap-4">
            <label className="text-sm text-ink-soft" htmlFor="target">
              Convert to
            </label>
            <select
              id="target"
              value={target}
              onChange={(e) => setTarget(e.target.value as Target)}
              className="rounded-lg border border-border bg-surface px-3 py-1.5 text-sm text-ink outline-none focus:border-accent"
            >
              <option value="yolo">YOLO</option>
              <option value="coco">COCO</option>
              <option value="voc">Pascal VOC</option>
            </select>

            <button
              onClick={handleConvert}
              disabled={busy}
              className="ml-auto rounded-lg bg-accent px-4 py-2 text-sm font-medium text-white transition-opacity hover:opacity-90 disabled:opacity-50"
            >
              {busy ? "Converting…" : "Convert & download"}
            </button>
          </div>

          <p className="mt-3 text-xs text-ink-faint">
            Downloads annotations only, in the target format. Your original images
            are not included, since you already have them.
          </p>
        </div>
      )}

      {error && (
        <div className="rounded-xl border border-error/30 bg-error-soft px-6 py-5">
          <p className="text-sm font-medium text-error">{error}</p>
        </div>
      )}
    </div>
  );
}