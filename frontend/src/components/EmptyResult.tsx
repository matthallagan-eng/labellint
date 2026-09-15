import type { AnalysisResult } from "../types";

export default function EmptyResult({ result }: { result: AnalysisResult }) {
  return (
    <div className="flex flex-col items-center gap-3 rounded-2xl border border-good/30 bg-good-soft px-8 py-16 text-center">
      <svg
        className="h-12 w-12 text-good"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        strokeWidth={1.5}
        aria-hidden="true"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
        />
      </svg>
      <h2 className="text-lg font-semibold text-ink">No issues found</h2>
      <p className="max-w-sm text-sm text-ink-soft">
        {result.image_count.toLocaleString()} images and{" "}
        {result.box_count.toLocaleString()} boxes checked, in {result.format} format,
        across {result.class_count} classes. Nothing flagged.
      </p>
    </div>
  );
}