import { useState } from "react";
import type { Finding } from "../types";
import SeverityBadge from "./SeverityBadge";

const BORDER_BY_SEVERITY = {
  error: "border-l-error",
  warning: "border-l-warn",
  info: "border-l-note",
} as const;

const PREVIEW_COUNT = 6;

export default function FindingCard({ finding }: { finding: Finding }) {
  const [expanded, setExpanded] = useState(false);
  const shown = expanded ? finding.images : finding.images.slice(0, PREVIEW_COUNT);
  const remaining = finding.images.length - shown.length;

  return (
    <article
      className={`rounded-xl border border-border border-l-4 bg-surface p-5 ${
        BORDER_BY_SEVERITY[finding.severity]
      }`}
    >
      <div className="mb-2 flex items-center gap-3">
        <SeverityBadge severity={finding.severity} />
        <h3 className="text-sm font-semibold text-ink">{finding.title}</h3>
      </div>

      <p className="text-sm leading-relaxed text-ink-soft">{finding.detail}</p>

      {finding.images.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-1.5">
          {shown.map((name) => (
            <span
              key={name}
              className="rounded-md bg-surface-sunken px-2 py-1 font-mono text-xs text-ink-soft"
            >
              {name}
            </span>
          ))}
          {!expanded && remaining > 0 && (
            <button
              onClick={() => setExpanded(true)}
              className="rounded-md px-2 py-1 text-xs font-medium text-accent hover:underline"
            >
              +{remaining} more
            </button>
          )}
        </div>
      )}
    </article>
  );
}