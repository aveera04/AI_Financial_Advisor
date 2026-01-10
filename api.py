#!/usr/bin/env python3
"""
FastAPI Backend for Multi-Agent Financial Advisor
REST API to interact with the orchestrator system from the React frontend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
from datetime import datetime
from dotenv import load_dotenv
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Load environment variables
load_dotenv()

# Import the agent
from agent.agentic_workflow import OrchestratorAgent
from utils.config_loader import load_config

# Initialize FastAPI app
app = FastAPI(
    title="Financial Advisor API",
    description="AI-powered financial advisor backend API",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://localhost:5173",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:5173",
        "http://[::]:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Thread pool for running sync agent code
executor = ThreadPoolExecutor(max_workers=4)

# Initialize the orchestrator agent (lazy loading)
_orchestrator: Optional[OrchestratorAgent] = None

def get_orchestrator() -> OrchestratorAgent:
    """Get or create the orchestrator agent (singleton pattern)"""
    global _orchestrator
    if _orchestrator is None:
        print("🚀 Initializing Orchestrator Agent...")
        _orchestrator = OrchestratorAgent()
        _orchestrator.build_graph()
        print("✅ Orchestrator Agent ready!")
    return _orchestrator


# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    tone: Optional[str] = "concise"  # concise or detailed
    

class Source(BaseModel):
    id: str
    title: str
    url: str
    hostname: str
    reason: str
    quality: str  # high, medium, low


class ChatResponse(BaseModel):
    content: str
    sources: List[Source]
    model: str
    is_regulatory: bool
    timestamp: str
    session_id: str


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    model_info: dict


class ModelInfo(BaseModel):
    orchestrator: str
    ipo_agent: str
    stock_agent: str
    tools: List[str]


# Helper functions
def extract_sources_from_response(response: str) -> List[Source]:
    """Extract sources from the response if they are mentioned"""
    # This is a simplified extraction - in production, you'd parse actual citations
    sources = []
    
    # Check for common financial source mentions
    source_patterns = [
        ("Investopedia", "https://www.investopedia.com", "Educational financial content"),
        ("Bloomberg", "https://www.bloomberg.com", "Financial news and data"),
        ("Reuters", "https://www.reuters.com", "Financial news coverage"),
        ("Yahoo Finance", "https://finance.yahoo.com", "Stock data and news"),
        ("MoneyControl", "https://www.moneycontrol.com", "Indian market data"),
        ("NSE India", "https://www.nseindia.com", "Official NSE data"),
        ("BSE India", "https://www.bseindia.com", "Official BSE data"),
        ("SEC", "https://www.sec.gov", "Regulatory information"),
        ("SEBI", "https://www.sebi.gov.in", "Indian market regulations"),
    ]
    
    response_lower = response.lower()
    source_id = 1
    
    for name, url, reason in source_patterns:
        if name.lower() in response_lower:
            hostname = url.replace("https://", "").replace("http://", "").split("/")[0]
            sources.append(Source(
                id=str(source_id),
                title=f"{name} - Financial Reference",
                url=url,
                hostname=hostname,
                reason=reason,
                quality="high" if name in ["SEC", "SEBI", "NSE India", "BSE India"] else "medium"
            ))
            source_id += 1
            
    # If no sources found, add a generic one
    if not sources:
        sources.append(Source(
            id="1",
            title="AI Analysis",
            url="#",
            hostname="AI Generated",
            reason="Response generated based on trained financial knowledge",
            quality="medium"
        ))
    
    return sources[:5]  # Limit to 5 sources


def check_regulatory_content(message: str, response: str) -> bool:
    """Check if the content involves regulatory/compliance topics"""
    regulatory_keywords = [
        "tax", "trading order", "buy order", "sell order", "legal", 
        "compliance", "irs", "sec", "sebi", "regulatory", "law",
        "execute trade", "place order"
    ]
    combined = (message + " " + response).lower()
    return any(keyword in combined for keyword in regulatory_keywords)


def run_agent_sync(message: str) -> str:
    """Run the agent synchronously (to be called in thread pool)"""
    orchestrator = get_orchestrator()
    return orchestrator.run(message)


# API Endpoints
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API info"""
    return {
        "name": "Financial Advisor API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    try:
        config = load_config()
        model_info = {
            "orchestrator": config.get("llm", {}).get("groq_oss_120b", {}).get("model_name", "unknown"),
            "ipo_agent": config.get("llm", {}).get("groq_deepseek", {}).get("model_name", "unknown"),
            "stock_agent": config.get("llm", {}).get("groq_oss", {}).get("model_name", "unknown"),
        }
    except Exception:
        model_info = {"status": "config not loaded"}
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        model_info=model_info
    )


@app.get("/models", response_model=ModelInfo, tags=["Info"])
async def get_model_info():
    """Get information about the models being used"""
    try:
        orchestrator = get_orchestrator()
        tools = [tool.name for tool in orchestrator.all_tools]
        config = load_config()
        
        return ModelInfo(
            orchestrator=config.get("llm", {}).get("groq_oss_120b", {}).get("model_name", "unknown"),
            ipo_agent=config.get("llm", {}).get("groq_deepseek", {}).get("model_name", "unknown"),
            stock_agent=config.get("llm", {}).get("groq_oss", {}).get("model_name", "unknown"),
            tools=tools
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Send a message to the financial advisor and get a response.
    
    - **message**: The user's question or query
    - **session_id**: Optional session identifier for conversation tracking
    - **tone**: Response tone preference (concise/detailed)
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        # Run the agent in a thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        response_content = await loop.run_in_executor(
            executor, 
            run_agent_sync, 
            request.message
        )
        
        # Extract sources and check regulatory content
        sources = extract_sources_from_response(response_content)
        is_regulatory = check_regulatory_content(request.message, response_content)
        
        # Generate session ID if not provided
        session_id = request.session_id or f"session_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return ChatResponse(
            content=response_content,
            sources=sources,
            model="Multi-Agent Orchestrator",
            is_regulatory=is_regulatory,
            timestamp=datetime.now().isoformat(),
            session_id=session_id
        )
        
    except Exception as e:
        print(f"❌ Error processing chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.post("/chat/stream", tags=["Chat"])
async def chat_stream(request: ChatRequest):
    """
    Streaming endpoint for real-time responses (placeholder for future implementation)
    """
    # For now, redirect to regular chat
    return await chat(request)


# Run with: python api.py
if __name__ == "__main__":
    print("🚀 Starting Financial Advisor API...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔗 Frontend should connect to: http://localhost:8000")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
