import type { AnalysisResult } from "../types";

export default function SummaryBar({ result }: { result: AnalysisResult }) {
  const errors = result.findings.filter((f) => f.severity === "error").length;
  const warnings = result.findings.filter((f) => f.severity === "warning").length;
  const notes = result.findings.filter((f) => f.severity === "info").length;

  return (
    <div className="rounded-xl border border-border bg-surface p-6">
      <div className="flex flex-wrap items-center justify-between gap-6">
        <div className="flex flex-wrap items-baseline gap-x-6 gap-y-1">
          <Stat value={result.image_count.toLocaleString()} label="images" />
          <Stat value={result.box_count.toLocaleString()} label="boxes" />
          <Stat value={String(result.class_count)} label="classes" />
          <span className="rounded-md bg-surface-sunken px-2 py-0.5 text-xs font-semibold uppercase tracking-wide text-ink-soft">
            {result.format}
          </span>
        </div>

        <div className="flex items-center gap-5 text-sm">
          <span className="flex items-center gap-1.5 font-medium text-error">
            <span className="h-2 w-2 rounded-full bg-error" /> {errors} error
            {errors === 1 ? "" : "s"}
          </span>
          <span className="flex items-center gap-1.5 font-medium text-warn">
            <span className="h-2 w-2 rounded-full bg-warn" /> {warnings} warning
            {warnings === 1 ? "" : "s"}
          </span>
          <span className="flex items-center gap-1.5 font-medium text-note">
            <span className="h-2 w-2 rounded-full bg-note" /> {notes} note
            {notes === 1 ? "" : "s"}
          </span>
        </div>
      </div>
    </div>
  );
}

function Stat({ value, label }: { value: string; label: string }) {
  return (
    <span className="flex items-baseline gap-1.5">
      <span className="text-xl font-bold text-ink">{value}</span>
      <span className="text-sm text-ink-soft">{label}</span>
    </span>
  );
}