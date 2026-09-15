import type { Severity } from "../types";

const CONFIG: Record<Severity, { label: string; text: string; bg: string; dot: string }> = {
  error: {
    label: "Error",
    text: "text-error",
    bg: "bg-error-soft",
    dot: "bg-error",
  },
  warning: {
    label: "Warning",
    text: "text-warn",
    bg: "bg-warn-soft",
    dot: "bg-warn",
  },
  info: {
    label: "Note",
    text: "text-note",
    bg: "bg-note-soft",
    dot: "bg-note",
  },
};

export default function SeverityBadge({ severity }: { severity: Severity }) {
  const c = CONFIG[severity];
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-semibold uppercase tracking-wide ${c.bg} ${c.text}`}
    >
      <span className={`h-1.5 w-1.5 rounded-full ${c.dot}`} aria-hidden="true" />
      {c.label}
    </span>
  );
}