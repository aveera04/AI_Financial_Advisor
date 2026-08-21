"""
Singleton manager for the OrchestratorAgent instance.
Ensures exactly one OrchestratorAgent per FastAPI process.
"""

import os
import re
import time
from dotenv import load_dotenv
from logger.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

_orchestrator_instance = None
_is_initialized: bool = False


def get_orchestrator():
    """Return the current OrchestratorAgent instance, or None if not initialized."""
    return _orchestrator_instance


def is_initialized() -> bool:
    """Check if the orchestrator has been initialized."""
    return _is_initialized


def initialize_orchestrator(model_provider: str = "groq_oss") -> None:
    """
    Initialize the OrchestratorAgent singleton.
    Raises ValueError if required env vars are missing.
    """
    global _orchestrator_instance, _is_initialized

    if not os.getenv("GROQ_API_KEY") or not os.getenv("TAVILY_API_KEY"):
        raise ValueError("Missing required API keys: GROQ_API_KEY and TAVILY_API_KEY")

    # Import here to avoid circular imports and heavy loading at module level
    from agent.agentic_workflow import OrchestratorAgent

    logger.info(f"Initializing OrchestratorAgent with provider: {model_provider}")
    _orchestrator_instance = OrchestratorAgent(model_provider=model_provider)
    _is_initialized = True
    logger.info("OrchestratorAgent initialized successfully")


def process_chat_query(query: str) -> dict:
    """
    Run a query through the orchestrator and return structured metadata.
    Replicates the agent-detection logic from app.py's get_response().
    """
    if not _is_initialized or _orchestrator_instance is None:
        raise RuntimeError("OrchestratorAgent is not initialized. Call POST /api/initialize first.")

    start_time = time.time()

    try:
        response = _orchestrator_instance.run(query)
        processing_time = time.time() - start_time

        # Agent detection — mirrors app.py lines 206-217
        if "IPO Advisor Response:" in response:
            agent_used = "IPO Advisor Agent"
            route_info = "Specialized IPO Analysis"
        elif "Stock Advisor Response:" in response:
            agent_used = "Stock Advisor Agent"
            route_info = "Specialized Stock Analysis"
        elif "Search Results" in response or "search_web" in response.lower():
            agent_used = "Web Search Tool (Tavily)"
            route_info = "General Market Research"
        else:
            agent_used = "Orchestrator"
            route_info = "Direct Response"

        return {
            "response": response,
            "agent_used": agent_used,
            "route_info": route_info,
            "processing_time": round(processing_time, 2),
        }

    except Exception as e:
        processing_time = time.time() - start_time
        error_msg = str(e)

        # Rate limit detection
        if "rate_limit" in error_msg.lower() or "429" in error_msg:
            wait_match = re.search(r'try again in (\d+m?\d*\.?\d*s?)', error_msg, re.IGNORECASE)
            retry_after = wait_match.group(1) if wait_match else "a few minutes"
            raise RateLimitError(retry_after=retry_after) from e

        # API key / config error
        if "api" in error_msg.lower() or "key" in error_msg.lower():
            raise APIConfigError(detail=error_msg[:200]) from e

        # Unknown error — re-raise
        raise


class RateLimitError(Exception):
    """Rate limit exceeded."""
    def __init__(self, retry_after: str = "a few minutes"):
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded. Try again in {retry_after}")


class APIConfigError(Exception):
    """API configuration error."""
    def __init__(self, detail: str = ""):
        self.detail = detail
        super().__init__(f"API configuration error: {detail}")
