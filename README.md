# Financial Advisor - AI-Powered Multi-Agent System

An intelligent financial advisor powered by a multi-agent orchestration system. Get personalized advice on IPOs, stocks, and financial planning.

## 🚀 Features

- **Multi-Agent Orchestration**: Specialized agents for IPOs, stocks, and general financial queries
- **Real-time Web Search**: Up-to-date information using Tavily search integration
- **Modern React Frontend**: Beautiful UI built with React, Tailwind CSS, and Shadcn/UI
- **FastAPI Backend**: High-performance API server with async support

## 📋 Prerequisites

- Python 3.10+
- Node.js 18+
- npm or bun

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Financial_Advisor.git
cd Financial_Advisor
```

### 2. Set up the Python backend

```bash
# Create a virtual environment
python -m venv .venv

# Activate it (Windows)
.venv\Scripts\activate

# Activate it (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root directory with your API keys:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here  # Optional
```

### 4. Set up the frontend

```bash
cd frontend
npm install
```

## 🏃 Running the Application

### Option 1: Run both servers manually

**Terminal 1 - Backend API (port 8000):**
```bash
cd Financial_Advisor
python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend (port 8080):**
```bash
cd Financial_Advisor/frontend
npm run dev
```

Open http://localhost:8080 in your browser.

### Option 2: Run Streamlit UI (Legacy)

```bash
python main.py
```

Or directly:
```bash
streamlit run app.py
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/models` | GET | Get model information |
| `/chat` | POST | Send a message to the financial advisor |

### Chat Request Example

```json
{
  "message": "What are the best stocks to invest in for 2026?",
  "tone": "detailed"
}
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    React Frontend (8080)                     │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend (8000)                     │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  Orchestrator Agent                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  IPO Agent   │  │ Stock Agent  │  │  Web Search Tool │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
Financial_Advisor/
├── api.py                 # FastAPI backend server
├── app.py                 # Streamlit UI (legacy)
├── main.py               # Streamlit launcher
├── agent/
│   ├── agentic_workflow.py    # Multi-agent orchestration
│   └── simple_orchestrator.py
├── frontend/             # React frontend
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API service
│   │   ├── stores/       # State management
│   │   └── types/        # TypeScript types
│   └── package.json
├── tools/                # Agent tools
├── utils/                # Utility modules
├── config/               # Configuration files
└── requirements.txt
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
