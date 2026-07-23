# Nexus AI Backend

FastAPI backend for the Nexus AI autonomous self-healing software engineer.

## Architecture

```
backend/
├── app/
│   ├── core/
│   │   ├── config.py       # Pydantic Settings (env vars)
│   │   ├── logging.py      # Structured logging (structlog)
│   │   ├── exceptions.py   # Custom exception hierarchy
│   │   └── di.py           # Dependency injection container
│   ├── models/
│   │   ├── schemas.py      # Pydantic request/response models
│   │   └── entities.py     # Domain models (dataclasses)
│   ├── services/
│   │   ├── openai_service.py   # OpenAI Responses API client
│   │   ├── sandbox_service.py  # Secure code execution
│   │   └── healing_service.py  # Self-healing loop orchestrator
│   ├── routers/
│   │   ├── generate.py     # POST /generate
│   │   ├── execute.py      # POST /execute
│   │   ├── repair.py       # POST /repair
│   │   └── status.py       # GET /status
│   └── main.py             # FastAPI app entry point
├── tests/
│   └── test_api.py         # Basic API tests
├── requirements.txt
├── pyproject.toml
├── Procfile               # Render deployment
└── .env.example
```

## Local Development

1. Copy `.env.example` to `.env` and fill in values
2. Create virtual environment: `python -m venv .venv`
3. Activate: `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run server: `uvicorn app.main:app --reload`

## Production Deployment (Render)

### Prerequisites
- GitHub account
- Render account (free tier available)
- OpenAI API key

### Step 1: Connect GitHub
1. Push your code to a GitHub repository
2. Log into [Render](https://render.com)

### Step 2: Create Web Service
1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Select the backend directory as the root directory
4. Set the following:

| Setting | Value |
|---------|-------|
| Name | `nexus-ai-backend` |
| Region | Auto |
| Branch | `main` |
| Root Directory | `backend` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Environment | Python 3.11 |

### Step 3: Configure Environment Variables
Add these environment variables in Render:

| Variable | Value |
|----------|-------|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o` (or your preferred model) |
| `DEBUG` | `false` |
| `LOG_LEVEL` | `INFO` |
| `FRONTEND_URL` | `https://your-frontend.vercel.app` |
| `BACKEND_URL` | Render auto-generated URL |

### Step 4: Deploy
1. Click "Create Web Service"
2. Render will automatically build and deploy your backend
3. Your API will be available at the Render-provided URL

## Endpoints

| Method | Path    | Description                    |
|--------|---------|--------------------------------|
| POST   | /generate | Generate code from prompt      |
| POST   | /execute  | Execute code in sandbox        |
| POST   | /repair   | Patch code based on errors     |
| GET    | /status   | Health check                   |
| GET    | /health   | Health check (alias)           |
| GET    | /         | Root endpoint with service info|

## Design Decisions

- **Dependency Injection**: `Container` class lazily instantiates services. Promotes testability and decouples route handlers from concrete implementations.
- **Modular Routers**: Each domain concern (generate, execute, repair, status) has its own router. Easy to extend or version.
- **Structured Logging**: `structlog` with JSON output in production and console output in development. Includes contextual fields (run_id, step, attempt).
- **Exception Hierarchy**: Custom exceptions map to HTTP responses via a global handler. Keeps route handlers clean.
- **Sandbox Isolation**: Code runs in temp directories via `subprocess.run` with timeouts. Syntax validation happens before execution.
- **Self-Healing Loop**: `HealingService.run()` orchestrates the full pipeline with configurable retry limits and step tracking.

## CORS Configuration

The backend automatically configures CORS for:
- Local development: `http://localhost:3000`
- Production: Configured via `FRONTEND_URL` environment variable

## Monitoring & Logging

- Health endpoint: `GET /health`
- API docs: `GET /docs`
- ReDoc: `GET /redoc`
- OpenAPI spec: `GET /openapi.json`