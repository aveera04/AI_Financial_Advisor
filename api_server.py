#!/usr/bin/env python3
"""
FastAPI backend server for AI Financial Advisor
Provides REST API endpoints for the React frontend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import time
from agent.agentic_workflow import OrchestratorAgent
from utils.config_loader import load_config
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Financial Advisor API",
    description="Backend API for the AI Financial Advisor multi-agent system",
    version="1.0.0"
)

# CORS configuration to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global orchestrator instance
orchestrator = None
model_info = {}

class InitRequest(BaseModel):
    """Request model for initialization"""
    model_provider: str = "groq_oss"
    api_key_name: str = "GROQ_API_KEY"

class ChatMessage(BaseModel):
    """Chat message model"""
    content: str
    files: Optional[List[str]] = None

class ChatResponse(BaseModel):
    """Response model for chat messages"""
    content: str
    sources: List[dict] = []
    model: str
    agent_used: str
    route_info: str
    processing_time: float
    is_regulatory: bool = False

class SystemStatus(BaseModel):
    """System status model"""
    initialized: bool
    models: dict

def get_model_info():
    """Get detailed model information from config"""
    try:
        config = load_config()
        return {
            "groq_oss": {
                "model_name": config["llm"]["groq_oss"]["model_name"],
                "provider": "Groq",
                "api_key": "GROQ_API_KEY"
            },
            "groq_deepseek": {
                "model_name": config["llm"]["groq_deepseek"]["model_name"],
                "provider": "Groq",
                "api_key": "GROQ_API_KEY"
            },
            "groq_oss_20b": {
                "model_name": config["llm"]["groq_oss_20b"]["model_name"],
                "provider": "Groq",
                "api_key": "GROQ_API_KEY"
            },
            "gemini_2.5_pro": {
                "model_name": config["llm"]["gemini_2.5_pro"]["model_name"],
                "provider": "Google",
                "api_key": "GEMINI_API_KEY"
            }
        }
    except Exception as e:
        print(f"Error loading model config: {e}")
        return {}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Financial Advisor API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/api/initialize")
async def initialize_session(request: InitRequest):
    """Initialize the AI Financial Advisor system"""
    global orchestrator, model_info
    
    try:
        # Check API keys
        required_keys = ["GROQ_API_KEY", "TAVILY_API_KEY"]
        missing_keys = [key for key in required_keys if not os.getenv(key)]
        
        if missing_keys:
            raise HTTPException(
                status_code=400,
                detail=f"Missing API keys: {', '.join(missing_keys)}"
            )
        
        # Get model info
        model_info = get_model_info()
        
        # Initialize orchestrator
        orchestrator = OrchestratorAgent(
            model_provider=request.model_provider,
            api_key_name=request.api_key_name
        )
        
        return {
            "status": "success",
            "message": "AI Financial Advisor System initialized successfully",
            "models": model_info
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize system: {str(e)}"
        )

@app.get("/api/status")
async def get_status():
    """Get system status"""
    global orchestrator, model_info
    
    return SystemStatus(
        initialized=orchestrator is not None,
        models=model_info if orchestrator else {}
    )

@app.post("/api/chat")
async def chat(message: ChatMessage):
    """Process a chat message and return response"""
    global orchestrator, model_info
    
    if not orchestrator:
        raise HTTPException(
            status_code=400,
            detail="System not initialized. Please initialize first."
        )
    
    try:
        start_time = time.time()
        
        # Get response from orchestrator
        response = orchestrator.run(message.content)
        processing_time = time.time() - start_time
        
        # Detect agent used and route info
        if "IPO Advisor Response:" in response:
            ipo_model = model_info.get("groq_deepseek", {}).get("model_name", "deepseek-r1")
            agent_used = f"IPO Agent ({ipo_model})"
            route_info = "Specialized IPO Analysis"
            model_used = ipo_model
        elif "Stock Advisor Response:" in response:
            stock_model = model_info.get("gemini_2.5_pro", {}).get("model_name", "gemini-2.5-pro")
            agent_used = f"Stock Agent ({stock_model})"
            route_info = "Comprehensive Stock Analysis"
            model_used = stock_model
        elif any(keyword in response.lower() for keyword in ["search results", "search_web", "tavily"]):
            agent_used = "Web Search Tool (Tavily)"
            route_info = "General Market Research"
            model_used = "tavily-search"
        else:
            orch_model = model_info.get("groq_oss", {}).get("model_name", "gpt-oss-120b")
            agent_used = f"Orchestrator ({orch_model})"
            route_info = "Direct Response"
            model_used = orch_model
        
        # Check for regulatory content
        regulatory_keywords = ['tax', 'trading', 'legal', 'compliance', 'irs', 'sec']
        is_regulatory = any(keyword in message.content.lower() for keyword in regulatory_keywords)
        
        return ChatResponse(
            content=response,
            sources=[],  # TODO: Extract sources from response if available
            model=model_used,
            agent_used=agent_used,
            route_info=route_info,
            processing_time=processing_time,
            is_regulatory=is_regulatory
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing message: {str(e)}"
        )

@app.get("/api/models")
async def get_models():
    """Get information about available models"""
    global model_info
    
    if not model_info:
        model_info = get_model_info()
    
    return {"models": model_info}

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting AI Financial Advisor API Server...")
    print("📱 Frontend should connect to: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
