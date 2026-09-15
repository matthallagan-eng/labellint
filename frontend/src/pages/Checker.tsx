import Dropzone from "../components/Dropzone";
import EmptyResult from "../components/EmptyResult";
import ErrorPanel from "../components/ErrorPanel";
import FindingCard from "../components/FindingCard";
import ProgressPanel from "../components/ProgressPanel";
import SummaryBar from "../components/SummaryBar";
import { useAnalysis } from "../hooks/useAnalysis";

export default function Checker() {
  const { status, progress, result, error, analyze, runDemo, reset } = useAnalysis();

  return (
    <div className="mx-auto max-w-4xl space-y-6 px-6 py-10">
      {status === "idle" && (
        <>
          <Dropzone onFile={analyze} />
          <div className="text-center">
            <button
              onClick={runDemo}
              className="text-sm font-medium text-accent hover:underline"
            >
              or try it on a sample dataset →
            </button>
          </div>
        </>
      )}

      {(status === "uploading" || status === "running") && (
        <ProgressPanel progress={progress} />
      )}

      {status === "failed" && (
        <ErrorPanel message={error || "Something went wrong"} onRetry={reset} />
      )}

      {status === "done" && result && (
        <>
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-medium text-ink-soft">Results</h2>
            <button
              onClick={reset}
              className="text-sm font-medium text-accent hover:underline"
            >
              Check another dataset
            </button>
          </div>

          <SummaryBar result={result} />

          {result.findings.length === 0 ? (
            <EmptyResult result={result} />
          ) : (
            <div className="space-y-3">
              {result.findings.map((f) => (
                <FindingCard key={f.check} finding={f} />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}