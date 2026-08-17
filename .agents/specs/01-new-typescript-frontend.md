# Spec: New TypeScript Frontend

## Overview

This feature introduces a full-featured **React + TypeScript + Vite + Tailwind CSS** frontend located at `frontend/` in the project root. The UI layer replaces the Streamlit chatbot (`app.py`) as the primary user-facing interface for Indian retail investors querying the AI Financial Advisor multi-agent system. The frontend communicates with the agent backend via a **FastAPI REST API** layer that bridges the React app with the `OrchestratorAgent`. The frontend exposes a rich chat interface with streaming-style message rendering, agent-routing transparency (which sub-agent responded), and a dark OLED financial aesthetic powered by the design system below.

**Layer:** UI layer (`frontend/`) + API layer (FastAPI backend)

---

## Design System

Sourced from `ui-ux-pro-max` skill (design system query: *"fintech AI financial advisor chat dark modern"*).

### Pattern: Enterprise Gateway
- Path-selection layout, trust signals prominent, clear AI labelling
- SEBI disclaimer always visible in the UI footer

### Style: Dark Mode (OLED)
- Deep black backgrounds, high contrast, eye-friendly for low-light use
- Minimal green glow effects, low white emission, visible keyboard focus rings

### Color Palette — Financial Dashboard Dark
| Role | Hex | CSS Variable |
|------|-----|--------------|
| Background | `#020617` | `--color-background` |
| Primary (surface) | `#0F172A` | `--color-primary` |
| Secondary (card bg) | `#1E293B` | `--color-secondary` |
| Accent / CTA | `#22C55E` | `--color-accent` |
| On Accent | `#0F172A` | `--color-on-accent` |
| Foreground (text) | `#F8FAFC` | `--color-foreground` |
| Card | `#0E1223` | `--color-card` |
| Muted | `#1A1E2F` | `--color-muted` |
| Muted Foreground | `#94A3B8` | `--color-muted-foreground` |
| Border | `#334155` | `--color-border` |
| Destructive | `#EF4444` | `--color-destructive` |

### Typography
- **Font:** IBM Plex Sans (weights: 300, 400, 500, 600, 700)
- **Import:** https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap
- **Mood:** Financial, trustworthy, professional, corporate

### Key UX Rules (from ui-ux-pro-max)
- Stream AI responses token-by-token (typewriter effect) — do NOT show a full-page spinner for >2s
- Label all AI-generated content clearly (`AI Advisor` badge) — never present AI as human
- Use `role="alert"` or `aria-live` for errors — not visual-only
- Hover states: 150–300ms transitions, `cursor-pointer` on all clickable elements
- Responsive: 375px / 768px / 1024px / 1440px breakpoints
- Use Phosphor Icons (`@phosphor-icons/react`) — no emoji as structural icons
- Respect `prefers-reduced-motion`

---

## Depends on

- **`OrchestratorAgent`** in `agent/agentic_workflow.py` — the chat backend
- **FastAPI + uvicorn** already in `requirements.txt` — needed to expose HTTP endpoints
- **Environment variables:** `GROQ_API_KEY`, `TAVILY_API_KEY` (already in `.env`)
- **`bun`** package manager for frontend (per GEMINI.md)
- **`app.py`** `get_response()` routing-detection logic — the API server will replicate this

---

## Agent / Routing Changes

No routing changes. The `OrchestratorAgent` is consumed as-is. The FastAPI backend wraps `orchestrator.run(query)` and returns the routing metadata already produced by `app.py`'s `get_response()`.

---

## New Tools

No new LangChain `@tool` functions. The frontend integrates via HTTP — no changes to the agent tool layer.

---

## API Endpoints (FastAPI)

New file: `api/main.py` — FastAPI application bridging the React frontend with the `OrchestratorAgent`.

All endpoints include CORS headers permitting http://localhost:5173 (Vite dev server).

### POST /api/chat
Send a user query to the orchestrator and receive a structured response.

**Request body:**
`json
{
  "query": "string"
}
`

**Response body:**
`json
{
  "response": "string",
  "agent_used": "string",
  "route_info": "string",
  "processing_time": 0.0
}
`

**Error response (rate limit / API error):**
`json
{
  "error": "string",
  "error_type": "rate_limit | api_error | system_error",
  "retry_after": "string | null"
}
`
HTTP status: 429 for rate limit, 500 for system errors.

### GET /api/health
Liveness probe — confirms FastAPI + OrchestratorAgent are ready.

**Response:**
`json
{
  "status": "ok | not_initialized",
  "agent": "OrchestratorAgent",
  "timestamp": "ISO8601"
}
`

### POST /api/initialize
Initialize (or re-initialize) the `OrchestratorAgent` singleton.

**Request body:** `{}` (empty)

**Response:**
`json
{
  "status": "initialized",
  "model_provider": "groq_oss"
}
`

### GET /api/sample-queries
Return the curated list of sample queries shown in the sidebar.

**Response:**
`json
{
  "queries": ["string"]
}
`

---

## Model / Config Changes

No changes to `config/config.yaml`. The FastAPI backend uses `model_provider="groq_oss"` (already defined). If a different model provider is required, add an entry under `llm:` in config and update `ModelLoader` — do not hardcode.

---

## Prompt Changes

No prompt changes. All routing prompts remain in `prompt_library/prompt.py`. The SEBI disclaimer will be surfaced in the React UI footer (static text) independent of prompt changes.

---

## Frontend Changes

### Directory: `frontend/` (create fresh at project root)

The `frontend/` directory does NOT exist in the current repo. It must be scaffolded with Vite + React + TypeScript + Tailwind CSS using `bun`.

### Create: New components and pages

`
frontend/
├── index.html
├── vite.config.ts
├── tsconfig.json
├── tsconfig.app.json
├── package.json
├── tailwind.config.ts
├── postcss.config.js
├── components.json                    # shadcn/ui config
└── src/
    ├── main.tsx                       # React entry point
    ├── App.tsx                        # Root app, routing
    ├── index.css                      # Global styles + CSS variables (design system tokens)
    ├── pages/
    │   └── Index.tsx                  # Main chat page
    ├── components/
    │   ├── layout/
    │   │   ├── Sidebar.tsx            # System info, sample queries, clear chat
    │   │   └── Header.tsx             # App title + status badge
    │   ├── chat/
    │   │   ├── ChatWindow.tsx         # Scrollable message list
    │   │   ├── MessageBubble.tsx      # User / AI message rendering (with markdown)
    │   │   ├── ChatInput.tsx          # Input bar + send button
    │   │   ├── AgentBadge.tsx         # Which agent handled the query
    │   │   └── TypingIndicator.tsx    # Animated dots while waiting
    │   ├── ui/
    │   │   ├── Button.tsx             # Design-system button variants
    │   │   ├── Badge.tsx              # Agent / status badges
    │   │   ├── Spinner.tsx            # Loading states
    │   │   └── Tooltip.tsx            # Hover tooltips (shadcn/ui)
    │   └── dialogs/
    │       └── DisclaimerModal.tsx    # SEBI disclaimer on first load
    ├── services/
    │   └── api.ts                     # All HTTP calls to FastAPI backend
    ├── stores/
    │   └── chatStore.ts               # Zustand store: messages, system state
    ├── hooks/
    │   ├── useChat.ts                 # Chat logic: send message, receive response
    │   └── useSystemInit.ts           # Initialize agent via /api/initialize
    └── types/
        ├── chat.ts                    # Message, ChatResponse, AgentRoute types
        └── api.ts                     # API request/response shape interfaces
`

### Modify: None

No existing files are modified. The Streamlit `app.py` remains functional in parallel.

---

## Files to Change

| File | Change |
|------|--------|
| `GEMINI.md` | Update `frontend/` directory listing to reflect new structure (post-implementation) |

---

## Files to Create

### Python / API

| File | Purpose |
|------|---------|
| `api/__init__.py` | Package marker |
| `api/main.py` | FastAPI application: CORS, /api/chat, /api/health, /api/initialize, /api/sample-queries |
| `api/models.py` | Pydantic v2 request/response models for all endpoints |
| `api/orchestrator_singleton.py` | Module-level singleton for OrchestratorAgent (mirrors app.py pattern) |

### Frontend (full scaffold)

All files listed in the Frontend Changes section above.

---

## New Dependencies

### Python (uv)
`ash
uv add fastapi uvicorn[standard]
`
fastapi and uvicorn are already in requirements.txt; add via uv to keep uv.lock consistent.

### Frontend (bun)

`ash
cd frontend
bun add react react-dom react-router-dom
bun add -D @types/react @types/react-dom typescript vite @vitejs/plugin-react-swc
bun add tailwindcss @tailwindcss/vite autoprefixer postcss
bun add zustand
bun add react-markdown remark-gfm
bun add @phosphor-icons/react
bun add class-variance-authority clsx tailwind-merge
# shadcn/ui (run after scaffold):
bunx --bun shadcn@latest init
bunx --bun shadcn@latest add tooltip dialog button badge
`

---

## Rules for Implementation

1. **Python >= 3.13** — no deprecated syntax or APIs
2. **Pydantic v2** — use `model_post_init` in any custom models; use `model_config = ConfigDict(...)` for settings
3. **`get_logger(__name__)`** from `logger.logger` — no `print()` in `api/` library code
4. **Model names from `config/config.yaml`** — `api/orchestrator_singleton.py` must read via `ModelLoader`, never hardcode `"groq_oss"`
5. **Singleton pattern** — `OrchestratorAgent` must be initialized once per server process in `api/orchestrator_singleton.py` using module-level `_orchestrator_instance = None`
6. **FastAPI CORS** — allow http://localhost:5173 and http://127.0.0.1:5173 in `CORSMiddleware`; also allow the production domain if deployed
7. **TypeScript strict mode** — `"strict": true` in `tsconfig.app.json`; all props typed via interfaces (no PropTypes, no implicit any)
8. **React event types** — `React.ChangeEvent<HTMLInputElement>`, `React.FormEvent<HTMLFormElement>` etc. — never use generic `Event`
9. **useState types** — always provide explicit generic: `useState<Message[]>([])`, `useState<boolean>(false)`
10. **Streaming UX** — while awaiting /api/chat, show TypingIndicator; display AI response text progressively if using SSE, or show full response on completion
11. **SEBI disclaimer** — must appear in DisclaimerModal on first visit (persisted to localStorage) AND in the page footer at all times
12. **Phosphor Icons only** — no emoji as structural icons; import from `@phosphor-icons/react`
13. **prefers-reduced-motion** — all CSS animations must have a `@media (prefers-reduced-motion: reduce)` override disabling or reducing motion
14. **No hardcoded API base URL** — use `import.meta.env.VITE_API_BASE_URL` (defaults to http://localhost:8000)
15. **Backend start command** — `uvicorn api.main:app --reload --port 8000` from project root
16. **Frontend start command** — `cd frontend && bun run dev` (Vite on port 5173)
17. **Never truncate** sub-agent responses — forward the full string from `orchestrator.run()` to the API response
18. **Backward-compat** — `app.py` must remain fully functional alongside the new API; do not modify the Streamlit app

---

## Definition of Done

- [ ] `api/main.py` starts with `uvicorn api.main:app --reload --port 8000` without errors
- [ ] `GET http://localhost:8000/api/health` returns `{"status": "not_initialized"}` before init and `{"status": "ok"}` after
- [ ] `POST http://localhost:8000/api/initialize` returns `{"status": "initialized", "model_provider": "groq_oss"}`
- [ ] `POST http://localhost:8000/api/chat` with `{"query": "What are upcoming IPOs?"}` returns a non-empty `response` string and `agent_used` contains "IPO"
- [ ] `GET http://localhost:8000/api/sample-queries` returns a JSON array of >= 5 strings
- [ ] `cd frontend && bun install && bun run dev` starts the Vite dev server on port 5173 with no TypeScript errors
- [ ] The chat page renders in a browser at http://localhost:5173 with a dark OLED background (`#020617`)
- [ ] IBM Plex Sans font is loaded and applied to all text
- [ ] Sending a query via the chat input calls /api/chat and renders the AI response in a MessageBubble
- [ ] AgentBadge correctly displays which sub-agent handled the query (IPO / Stock / Orchestrator)
- [ ] TypingIndicator is shown while a request is in flight and hidden on completion
- [ ] SEBI disclaimer modal appears on first visit and can be dismissed; does not reappear on refresh (localStorage persisted)
- [ ] SEBI disclaimer text is also visible in the page footer at all times
- [ ] "Clear Chat" action empties the chat window without a page reload
- [ ] "Sample Queries" in the sidebar pre-fill the chat input on click
- [ ] `streamlit run app.py` still works independently with no regressions
- [ ] TypeScript compilation passes with 0 errors: `cd frontend && bunx tsc --noEmit`
- [ ] Page is responsive at 375px, 768px, 1024px, and 1440px viewports
- [ ] No emojis used as structural icons — Phosphor Icons used throughout
- [ ] Rate-limit error from the API renders a user-friendly message (not a raw error object)
- [ ] `curl -X POST http://localhost:8000/api/chat -H "Origin: http://localhost:5173" -I` returns `Access-Control-Allow-Origin: http://localhost:5173`
