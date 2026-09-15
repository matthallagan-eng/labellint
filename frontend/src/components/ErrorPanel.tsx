interface Props {
  message: string;
  onRetry: () => void;
}

export default function ErrorPanel({ message, onRetry }: Props) {
  return (
    <div className="rounded-xl border border-error/30 bg-error-soft px-6 py-5">
      <p className="text-sm font-medium text-error">{message}</p>
      <button
        onClick={onRetry}
        className="mt-3 text-sm font-medium text-accent hover:underline"
      >
        Try again
      </button>
    </div>
  );
}