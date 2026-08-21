"""Pydantic v2 request/response models for the FastAPI endpoints."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    """Request body for POST /api/chat."""
    query: str = Field(..., min_length=1, max_length=2000, description="User query text")


class ChatResponse(BaseModel):
    """Successful response from POST /api/chat."""
    response: str
    agent_used: str
    route_info: str
    processing_time: float


class ErrorResponse(BaseModel):
    """Error response body."""
    error: str
    error_type: str  # "rate_limit" | "api_error" | "system_error"
    retry_after: Optional[str] = None


class HealthResponse(BaseModel):
    """Response from GET /api/health."""
    status: str  # "ok" | "not_initialized"
    agent: str = "OrchestratorAgent"
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


class InitializeResponse(BaseModel):
    """Response from POST /api/initialize."""
    status: str = "initialized"
    model_provider: str = "groq_oss"


class SampleQueriesResponse(BaseModel):
    """Response from GET /api/sample-queries."""
    queries: list[str]
