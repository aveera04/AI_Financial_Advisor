"""
FastAPI application bridging the React frontend with the OrchestratorAgent.

Start with:
    uvicorn api.main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from logger.logger import get_logger
from api.models import (
    ChatRequest, ChatResponse, ErrorResponse,
    HealthResponse, InitializeResponse, SampleQueriesResponse,
)
from api.orchestrator_singleton import (
    get_orchestrator, is_initialized, initialize_orchestrator,
    process_chat_query, RateLimitError, APIConfigError,
)

logger = get_logger(__name__)

app = FastAPI(
    title="AI Financial Advisor API",
    description="REST API bridge for the multi-agent financial advisor system",
    version="0.1.0",
)

# CORS — allow Vite dev server and common local origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SAMPLE_QUERIES = [
    "What are the current IPO opportunities in India?",
    "Should I invest in upcoming IPOs this week?",
    "What are today's stock market trends?",
    "Compare IPO vs mutual fund returns",
    "Tell me about Hyundai Motor India IPO",
    "Analyze RELIANCE stock for investment",
    "What is the GMP for recent IPOs?",
]


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Liveness probe — confirms FastAPI + OrchestratorAgent status."""
    status = "ok" if is_initialized() else "not_initialized"
    return HealthResponse(status=status)


import asyncio

@app.post("/api/initialize", response_model=InitializeResponse)
async def initialize_system():
    """Initialize or re-initialize the OrchestratorAgent singleton."""
    try:
        await asyncio.to_thread(initialize_orchestrator, model_provider="groq_oss")
        return InitializeResponse()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to initialize orchestrator: {e}")
        raise HTTPException(status_code=500, detail=f"Initialization failed: {str(e)[:300]}")


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Send a user query to the orchestrator."""
    try:
        result = await asyncio.to_thread(process_chat_query, request.query)
        return ChatResponse(**result)

    except RuntimeError as e:
        # Not initialized
        raise HTTPException(status_code=503, detail=str(e))

    except RateLimitError as e:
        return JSONResponse(
            status_code=429,
            content=ErrorResponse(
                error=str(e),
                error_type="rate_limit",
                retry_after=e.retry_after,
            ).model_dump(),
        )

    except APIConfigError as e:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error=str(e),
                error_type="api_error",
            ).model_dump(),
        )

    except Exception as e:
        logger.error(f"Unexpected error in /api/chat: {e}")
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error=f"Internal server error: {str(e)[:300]}",
                error_type="system_error",
            ).model_dump(),
        )


@app.get("/api/sample-queries", response_model=SampleQueriesResponse)
async def get_sample_queries():
    """Return curated sample queries for the sidebar."""
    return SampleQueriesResponse(queries=SAMPLE_QUERIES)
