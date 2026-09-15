import { useCallback, useEffect, useRef, useState } from "react";
import type { AnalysisResult, JobStatus } from "../types";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";
const POLL_INTERVAL_MS = 1200;

export function useAnalysis() {
  const [status, setStatus] = useState<JobStatus>("idle");
  const [progress, setProgress] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const timer = useRef<number | null>(null);

  const stop = useCallback(() => {
    if (timer.current !== null) {
      window.clearInterval(timer.current);
      timer.current = null;
    }
  }, []);

  useEffect(() => stop, [stop]);

  const poll = useCallback(
    (jobId: string) => {
      timer.current = window.setInterval(async () => {
        try {
          const res = await fetch(`${API}/analyze/${jobId}`);
          if (!res.ok) throw new Error("Job not found");
          const data = await res.json();

          setProgress(data.progress || "");

          if (data.status === "done") {
            stop();
            setResult(data.result as AnalysisResult);
            setStatus("done");
          } else if (data.status === "failed") {
            stop();
            setError(data.error || "Analysis failed");
            setStatus("failed");
          }
        } catch (e) {
          stop();
          setError(e instanceof Error ? e.message : "Lost contact with the server");
          setStatus("failed");
        }
      }, POLL_INTERVAL_MS);
    },
    [stop]
  );

  const analyze = useCallback(
    async (file: File) => {
      setStatus("uploading");
      setError(null);
      setResult(null);
      setProgress("Uploading");

      try {
        const form = new FormData();
        form.append("file", file);

        const res = await fetch(`${API}/analyze`, { method: "POST", body: form });
        if (!res.ok) {
          const d = await res.json().catch(() => ({}));
          throw new Error(d.detail || "Upload failed");
        }

        const { job_id } = await res.json();
        setStatus("running");
        poll(job_id);
      } catch (e) {
        setError(e instanceof Error ? e.message : "Upload failed");
        setStatus("failed");
      }
    },
    [poll]
  );

  const runDemo = useCallback(async () => {
    setStatus("uploading");
    setError(null);
    setResult(null);
    setProgress("Loading sample dataset");

    try {
      const res = await fetch(`${API}/analyze/demo`, { method: "POST" });
      if (!res.ok) throw new Error("Could not start demo analysis");

      const { job_id } = await res.json();
      setStatus("running");
      poll(job_id);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Demo failed to start");
      setStatus("failed");
    }
  }, [poll]);

  const reset = useCallback(() => {
    stop();
    setStatus("idle");
    setResult(null);
    setError(null);
    setProgress("");
  }, [stop]);

  return { status, progress, result, error, analyze, runDemo, reset };
}