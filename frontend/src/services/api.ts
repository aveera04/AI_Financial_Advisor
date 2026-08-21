import type {
  ChatRequest,
  ChatResponse,
  ApiError,
  HealthResponse,
  InitializeResponse,
  SampleQueriesResponse,
} from "@/types/api";

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";

async function request<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const url = `${BASE_URL}${path}`;
  let res: Response;

  try {
    res = await fetch(url, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
  } catch (netErr: unknown) {
    const errorMsg =
      netErr instanceof Error ? netErr.message : "Network request failed";
    throw new ApiServiceError(
      `Cannot connect to backend server at ${BASE_URL || "http://localhost:8000"}. (${errorMsg})`,
      0,
      "network_error"
    );
  }

  if (!res.ok) {
    const body = await res.json().catch(() => null);

    if (res.status === 429 && body) {
      const error = body as ApiError;
      throw new RateLimitError(
        error.error,
        error.retry_after ?? "a few minutes"
      );
    }

    throw new ApiServiceError(
      body?.error ?? body?.detail ?? `Request failed (${res.status})`,
      res.status,
      (body as ApiError)?.error_type ?? "system_error"
    );
  }

  return res.json() as Promise<T>;
}

export const api = {
  health: () => request<HealthResponse>("/api/health"),

  initialize: () =>
    request<InitializeResponse>("/api/initialize", { method: "POST" }),

  chat: (query: string) =>
    request<ChatResponse>("/api/chat", {
      method: "POST",
      body: JSON.stringify({ query } satisfies ChatRequest),
    }),

  sampleQueries: () => request<SampleQueriesResponse>("/api/sample-queries"),
};

export class ApiServiceError extends Error {
  constructor(
    message: string,
    public status: number,
    public errorType: string
  ) {
    super(message);
    this.name = "ApiServiceError";
  }
}

export class RateLimitError extends ApiServiceError {
  constructor(
    message: string,
    public retryAfter: string
  ) {
    super(message, 429, "rate_limit");
    this.name = "RateLimitError";
  }
}
