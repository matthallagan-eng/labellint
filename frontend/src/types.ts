export type Severity = "error" | "warning" | "info";

export interface Finding {
  check: string;
  severity: Severity;
  title: string;
  detail: string;
  images: string[];
  count: number;
}

export interface AnalysisResult {
  format: string;
  image_count: number;
  box_count: number;
  class_count: number;
  class_names: Record<number, string>;
  findings: Finding[];
}

export type JobStatus = "idle" | "uploading" | "running" | "done" | "failed";