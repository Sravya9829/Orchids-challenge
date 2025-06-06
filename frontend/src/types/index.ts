export interface CloneRequest {
  url: string;
}

export interface CloneResponse {
  job_id: string;
  status: CloneStatus;
  message: string;
}

export interface CloneResult {
  job_id: string;
  status: CloneStatus;
  original_url: string;
  cloned_html?: string;
  error_message?: string;
}

export enum CloneStatus {
  PENDING = "pending",
  PROCESSING = "processing", 
  COMPLETED = "completed",
  FAILED = "failed"
}