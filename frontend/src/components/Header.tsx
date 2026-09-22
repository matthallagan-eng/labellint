interface Props {
  view: "check" | "convert";
  onChange: (view: "check" | "convert") => void;
}

export default function Header({ view, onChange }: Props) {
  return (
    <header className="border-b border-border bg-accent">
      <div className="mx-auto flex max-w-4xl flex-col gap-6 px-6 py-8">
        <div>
          <h1 className="text-2xl font-semibold text-white">LabelLint</h1>
          <p className="mt-1 text-sm text-white/70">
            Find the problems in your dataset before you it causes issues down the line!
          </p>
        </div>
        <div
          className="inline-flex w-fit rounded-lg border border-border bg-surface-sunken p-1"
          role="tablist"
        >
          <button
            role="tab"
            aria-selected={view === "check"}
            onClick={() => onChange("check")}
            className={`rounded-md px-4 py-1.5 text-sm font-medium transition-colors ${
              view === "check"
                ? "bg-surface text-ink shadow-sm"
                : "text-ink-soft hover:text-ink"
            }`}
          >
            Check dataset
          </button>
          <button
            role="tab"
            aria-selected={view === "convert"}
            onClick={() => onChange("convert")}
            className={`rounded-md px-4 py-1.5 text-sm font-medium transition-colors ${
              view === "convert"
                ? "bg-surface text-ink shadow-sm"
                : "text-ink-soft hover:text-ink"
            }`}
          >
            Convert format
          </button>
        </div>
      </div>
    </header>
  );
}