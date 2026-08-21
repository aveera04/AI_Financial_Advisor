export interface ChatRequest {
  query: string;
}

export interface ChatResponse {
  response: string;
  agent_used: string;
  route_info: string;
  processing_time: number;
}

export interface ApiError {
  error: string;
  error_type: "rate_limit" | "api_error" | "system_error";
  retry_after?: string | null;
}

export interface HealthResponse {
  status: "ok" | "not_initialized";
  agent: string;
  timestamp: string;
}

export interface InitializeResponse {
  status: string;
  model_provider: string;
}

export interface SampleQueriesResponse {
  queries: string[];
}
