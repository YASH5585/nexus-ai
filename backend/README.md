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
└── .env.example
```

## Setup

1. Copy `.env.example` to `.env` and fill in values
2. Install dependencies: `pip install -r requirements.txt`
3. Run server: `uvicorn app.main:app --reload`

## Endpoints

| Method | Path    | Description                    |
|--------|---------|--------------------------------|
| POST   | /generate | Generate code from prompt      |
| POST   | /execute  | Execute code in sandbox        |
| POST   | /repair   | Patch code based on errors     |
| GET    | /status   | Health check                   |

## Design Decisions

- **Dependency Injection**: `Container` class lazily instantiates services. Promotes testability and decouples route handlers from concrete implementations.
- **Modular Routers**: Each domain concern (generate, execute, repair, status) has its own router. Easy to extend or version.
- **Structured Logging**: `structlog` with JSON output in production and console output in development. Includes contextual fields (run_id, step, attempt).
- **Exception Hierarchy**: Custom exceptions map to HTTP responses via a global handler. Keeps route handlers clean.
- **Sandbox Isolation**: Code runs in temp directories via `subprocess.run` with timeouts. Syntax validation happens before execution.
- **Self-Healing Loop**: `HealingService.run()` orchestrates the full pipeline with configurable retry limits and step tracking.
