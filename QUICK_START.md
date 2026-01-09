# Quick Start Guide - AI Financial Advisor

## Overview

The AI Financial Advisor now features a modern React-based web interface with a FastAPI backend. This guide will help you get started quickly.

## Prerequisites

Before you begin, ensure you have:

1. **Python 3.8+** installed
2. **Node.js 16+** and npm installed
3. API keys for:
   - **GROQ_API_KEY** - Required for AI models
   - **TAVILY_API_KEY** - Required for web search
   - **GEMINI_API_KEY** - Optional, for Gemini models

## Setup

### 1. Environment Variables

Create a `.env` file in the project root:

```bash
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here  # Optional
```

### 2. Install Dependencies

Install Python dependencies:
```bash
pip install -r requirements.txt
```

Frontend dependencies will be automatically installed on first run, or you can install them manually:
```bash
cd frontend
npm install
cd ..
```

## Running the Application

### Option 1: Complete Application (Recommended)

Run both backend and frontend together:

```bash
python main.py
```

This will:
- Start the FastAPI backend on `http://localhost:8000`
- Start the React frontend on `http://localhost:8080`
- Open automatically in your browser

**Access the app at:** http://localhost:8080

### Option 2: Backend Only

If you only want to run the API backend:

```bash
python api_server.py
```

**API Documentation:** http://localhost:8000/docs

### Option 3: Legacy Streamlit Interface

The original Streamlit interface is still available:

```bash
python -m streamlit run app.py
```

**Access at:** http://localhost:8501

## Using the Application

### Initialize the System

1. Open http://localhost:8080
2. Click the "Initialize" button in the sidebar
3. Wait for the system to initialize (this connects to the AI models)

### Ask Questions

Once initialized, you can:
- Type questions in the chat input at the bottom
- Ask about IPOs, stocks, market trends, investment advice
- Upload documents for analysis (coming soon)

### Sample Queries

Try these example questions:
- "What are the current IPO opportunities in India?"
- "Should I invest in upcoming IPOs this week?"
- "What are today's stock market trends?"
- "Compare IPO vs mutual fund returns"
- "Tell me about recent tech company IPOs"

### Features

- **Multi-Agent Routing**: Questions are automatically routed to specialized agents
- **Source Citations**: Responses include sources and references
- **Model Transparency**: See which AI model answered your question
- **Regulatory Warnings**: Automatic warnings for sensitive topics
- **Chat History**: Your conversations are saved locally

## Architecture

### Backend (Port 8000)
- FastAPI REST API
- Multi-agent orchestration system
- Web search integration
- Model management

### Frontend (Port 8080)
- React 18 with TypeScript
- Modern UI with shadcn/ui components
- Real-time chat interface
- Session management

## Troubleshooting

### Backend won't start
- Check that all Python dependencies are installed: `pip install -r requirements.txt`
- Verify your API keys are set in `.env`
- Check if port 8000 is available

### Frontend won't start
- Ensure Node.js is installed: `node --version`
- Install dependencies: `cd frontend && npm install`
- Check if port 8080 is available

### API Connection Error
- Verify backend is running on http://localhost:8000
- Check browser console for errors
- Ensure CORS is properly configured (should be automatic)

## Development

### Backend Development
```bash
# Run with auto-reload
uvicorn api_server:app --reload --port 8000
```

### Frontend Development
```bash
cd frontend
npm run dev  # Starts with hot reload
```

### Run Tests
```bash
# Backend tests
pytest tests/

# Integration test
python test_integration.py
```

## API Endpoints

Key endpoints (visit http://localhost:8000/docs for full documentation):

- `POST /api/initialize` - Initialize the AI system
- `POST /api/chat` - Send a message and get response
- `GET /api/status` - Check if system is initialized
- `GET /api/models` - Get available AI models info
- `GET /health` - Health check

## Need Help?

- Check the main README.md for detailed information
- Review the API documentation at http://localhost:8000/docs
- Check the frontend README at `frontend/README.md`

## Disclaimer

⚠️ **This is not investment advice.** The AI Financial Advisor provides information and analysis but should not be used as the sole basis for investment decisions. Always consult with a qualified financial advisor before making investment decisions.
