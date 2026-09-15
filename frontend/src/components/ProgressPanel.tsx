interface Props {
  progress: string;
}

export default function ProgressPanel({ progress }: Props) {
  return (
    <div className="flex flex-col items-center gap-4 rounded-2xl border border-border bg-surface px-8 py-16 text-center">
      <div className="flex gap-1.5" aria-hidden="true">
        <span className="h-2 w-2 animate-bounce rounded-full bg-accent [animation-delay:-0.3s]" />
        <span className="h-2 w-2 animate-bounce rounded-full bg-accent [animation-delay:-0.15s]" />
        <span className="h-2 w-2 animate-bounce rounded-full bg-accent" />
      </div>
      <p className="text-sm font-medium text-ink">{progress || "Working"}</p>
    </div>
  );
}