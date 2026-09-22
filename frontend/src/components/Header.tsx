interface Props {
  view: "check" | "convert";
  onChange: (view: "check" | "convert") => void;
}

export default function Header({ view, onChange }: Props) {
  return (
    <header className="border-b border-border bg-accent">
      <div className="mx-auto flex max-w-4xl items-center justify-between gap-6 px-6 py-4">
        <div>
          <h1 className="text-lg font-semibold text-white">LabelLint</h1>
          <p className="mt-0.5 text-xs text-white/75">
            Find the problems in your computer vision dataset before it stops you in your tracks.
          </p>
        </div>

        <div
          className="inline-flex shrink-0 rounded-lg bg-white/15 p-1"
          role="tablist"
        >
          <button
            role="tab"
            aria-selected={view === "check"}
            onClick={() => onChange("check")}
            className={`rounded-md px-4 py-1.5 text-sm font-medium transition-colors ${
              view === "check"
                ? "bg-white text-accent shadow-sm"
                : "text-white/80 hover:text-white"
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
                ? "bg-white text-accent shadow-sm"
                : "text-white/80 hover:text-white"
            }`}
          >
            Convert format
          </button>
        </div>
      </div>
    </header>
  );
}