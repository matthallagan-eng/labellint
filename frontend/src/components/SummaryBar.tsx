import type { AnalysisResult } from "../types";

export default function SummaryBar({ result }: { result: AnalysisResult }) {
  const errors = result.findings.filter((f) => f.severity === "error").length;
  const warnings = result.findings.filter((f) => f.severity === "warning").length;
  const notes = result.findings.filter((f) => f.severity === "info").length;

  return (
    <div className="rounded-xl border border-border bg-surface p-5">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <p className="text-sm text-ink-soft">
          <span className="font-semibold text-ink">
            {result.image_count.toLocaleString()}
          </span>{" "}
          images ·{" "}
          <span className="font-semibold text-ink">
            {result.box_count.toLocaleString()}
          </span>{" "}
          boxes ·{" "}
          <span className="font-semibold text-ink">{result.class_count}</span>{" "}
          classes ·{" "}
          <span className="font-semibold uppercase text-ink">{result.format}</span>
        </p>

        <div className="flex items-center gap-4 text-sm">
          <span className="flex items-center gap-1.5 text-error">
            <span className="h-2 w-2 rounded-full bg-error" /> {errors} error
            {errors === 1 ? "" : "s"}
          </span>
          <span className="flex items-center gap-1.5 text-warn">
            <span className="h-2 w-2 rounded-full bg-warn" /> {warnings} warning
            {warnings === 1 ? "" : "s"}
          </span>
          <span className="flex items-center gap-1.5 text-note">
            <span className="h-2 w-2 rounded-full bg-note" /> {notes} note
            {notes === 1 ? "" : "s"}
          </span>
        </div>
      </div>
    </div>
  );
}