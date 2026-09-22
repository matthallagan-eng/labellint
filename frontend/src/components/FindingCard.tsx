import { useState } from "react";
import type { Finding } from "../types";
import SeverityBadge, { severityConfig } from "./SeverityBadge";

const PREVIEW_COUNT = 6;

export default function FindingCard({ finding }: { finding: Finding }) {
  const [expanded, setExpanded] = useState(false);
  const shown = expanded ? finding.images : finding.images.slice(0, PREVIEW_COUNT);
  const remaining = finding.images.length - shown.length;
  const c = severityConfig(finding.severity);

  return (
    <article
      className={`rounded-xl border border-border border-l-4 bg-surface p-6 ${c.border}`}
    >
      <div className="mb-3 flex items-center gap-3">
        <SeverityBadge severity={finding.severity} />
        <h3 className="text-base font-semibold text-ink">{finding.title}</h3>
      </div>

      <p className="max-w-3xl text-sm leading-relaxed text-ink-soft">
        {finding.detail}
      </p>

      {finding.images.length > 0 && (
        <div className="mt-4 flex flex-wrap gap-2">
          {shown.map((name) => (
            <span
              key={name}
              title={name}
              className="max-w-[220px] truncate rounded-md bg-surface-sunken px-2.5 py-1 font-mono text-xs text-ink-soft"
            >
              {name}
            </span>
          ))}
          {!expanded && remaining > 0 && (
            <button
              onClick={() => setExpanded(true)}
              className="rounded-md px-2.5 py-1 text-xs font-medium text-accent hover:underline"
            >
              +{remaining} more
            </button>
          )}
        </div>
      )}
    </article>
  );
}