import { useRef, useState } from "react";

interface Props {
  onFile: (file: File) => void;
  disabled?: boolean;
  hint?: string;
}

export default function Dropzone({ onFile, disabled, hint }: Props) {
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  function handleFiles(files: FileList | null) {
    const file = files?.[0];
    if (file) onFile(file);
  }

  return (
    <div
      onDragOver={(e) => {
        e.preventDefault();
        if (!disabled) setDragging(true);
      }}
      onDragLeave={() => setDragging(false)}
      onDrop={(e) => {
        e.preventDefault();
        setDragging(false);
        if (!disabled) handleFiles(e.dataTransfer.files);
      }}
      onClick={() => !disabled && inputRef.current?.click()}
      className={`flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed px-8 py-16 text-center transition-colors ${
        disabled
          ? "cursor-not-allowed border-border bg-surface-sunken opacity-60"
          : dragging
            ? "border-accent bg-accent-soft"
            : "border-border bg-surface-sunken hover:border-accent/50"
      }`}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".zip"
        disabled={disabled}
        onChange={(e) => handleFiles(e.target.files)}
        className="hidden"
      />

      <svg
        className="mb-3 h-10 w-10 text-accent"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        strokeWidth={1.5}
        aria-hidden="true"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3"
        />
      </svg>

      <p className="text-sm font-medium text-ink">Drop a zip here, or click to browse</p>
      <p className="mt-1 text-xs text-ink-faint">
        {hint || "Images plus YOLO, COCO, or VOC labels · Max 200 MB"}
      </p>
    </div>
  );
}