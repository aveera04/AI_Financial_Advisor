# AI Financial Advisor

Multi-agent AI system to help with investing in IPOs and stocks. Features a modern React frontend with FastAPI backend.

## Features

- **Multi-Agent System**: Specialized agents for IPO analysis, stock analysis, and general orchestration
- **Web Search Integration**: Real-time market data using Tavily API
- **Modern UI**: React-based chat interface with shadcn/ui components
- **Regulatory Compliance**: Built-in warnings for regulatory-sensitive queries
- **Model Transparency**: Clear disclosure of AI models used for each response

## Quick Start

### Prerequisites

- Python 3.8+ with pip
- Node.js 16+ with npm
- API Keys:
  - GROQ_API_KEY (for AI models)
  - TAVILY_API_KEY (for web search)
  - GEMINI_API_KEY (optional, for Gemini models)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/aveera04/AI_Financial_Advisor.git
cd AI_Financial_Advisor
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Install frontend dependencies (optional, will auto-install on first run):
```bash
cd frontend
npm install
cd ..
```

### Running the Application

Launch the complete application (backend + frontend):

```bash
python main.py
```

This will start:
- FastAPI backend on http://localhost:8000
- React frontend on http://localhost:8080

Then open http://localhost:8080 in your browser.

### Alternative: Legacy Streamlit Interface

The original Streamlit interface is still available:

```bash
python -m streamlit run app.py
```

## Architecture

### Backend (FastAPI)
- **api_server.py**: REST API server
- **agent/**: Multi-agent workflow system
  - Orchestrator agent for routing queries
  - IPO specialist agent (DeepSeek R1)
  - Stock specialist agent (Gemini 2.5 Pro)
- **tools/**: Web search and data retrieval tools
- **utils/**: Configuration and utility functions

### Frontend (React + TypeScript)
- **Vite**: Fast build tool and dev server
- **React 18**: UI framework
- **shadcn/ui**: Component library
- **Tailwind CSS**: Styling
- **Zustand**: State management

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

### Key Endpoints

- `POST /api/initialize` - Initialize the AI system
- `POST /api/chat` - Send a message and get AI response
- `GET /api/status` - Check system status
- `GET /api/models` - Get information about available models

## Development

### Backend Development

```bash
# Run backend only
python api_server.py

# Run tests
pytest tests/
```

### Frontend Development

```bash
cd frontend

# Start dev server
npm run dev

# Build for production
npm run build

# Lint code
npm run lint
```

## Configuration

Edit `config/config.yaml` to customize:
- LLM model providers and settings
- Agent behaviors
- Search parameters

## License

See LICENSE file for details.

## Disclaimer

⚠️ This is not investment advice. Please consult a financial advisor before making investment decisions.
