"""
Nexus AI Backend Application.

This module initializes the FastAPI application, configures middleware,
registers routers, and defines global exception handlers.

Example:
    To run the application:

        uvicorn app.main:app --reload

    Or programmatically:

        import uvicorn
        from app.main import app
        uvicorn.run(app, host="0.0.0.0", port=8000)
"""

from typing import Dict

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.core.exceptions import NexusAIException, handle_nexus_exception
from app.models.schemas import ErrorResponse
from app.routers.generate import router as generate_router
from app.routers.execute import router as execute_router
from app.routers.repair import router as repair_router
from app.routers.status import router as status_router
from app.routers.agent import router as agent_router
from app.routers.test import router as test_router
from app.api.routers.decision import router as decision_router
from app.api.routers.reviewer import router as reviewer_router
from app.api.routers.performance import router as performance_router
from app.api.routers.confidence import router as confidence_router

logger = get_logger(__name__)

# Configure structured logging on application startup
setup_logging()

# Initialize FastAPI application with metadata
app = FastAPI(
    title="Nexus AI Backend",
    description=(
        "Autonomous self-healing software engineer backend. "
        "Generates code from natural language, executes it in secure sandboxes, "
        "and iteratively patches failures through intelligent self-healing loops."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Exception Handlers
# ---------------------------------------------------------------------------


@app.exception_handler(NexusAIException)
async def nexus_exception_handler(
    request: Request, exc: NexusAIException
) -> JSONResponse:
    """
    Global exception handler for NexusAIException.

    Logs the error and returns a structured JSON error response.

    Args:
        request: The incoming HTTP request
        exc: The NexusAIException that was raised

    Returns:
        JSONResponse with error details and appropriate status code
    """
    logger.error(
        "Nexus AI exception",
        code=exc.code,
        message=exc.message,
        path=request.url.path,
    )
    http_exc = handle_nexus_exception(exc)
    return JSONResponse(
        status_code=http_exc.status_code,
        content=ErrorResponse(code=exc.code, message=exc.message).model_dump(),
    )


@app.exception_handler(Exception)
async def generic_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """
    Global exception handler for unhandled exceptions.

    Args:
        request: The incoming HTTP request
        exc: The unhandled exception

    Returns:
        JSONResponse with generic error message
    """
    logger.error(
        "Unhandled exception",
        error=str(exc),
        path=request.url.path,
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            code="INTERNAL_ERROR",
            message="An unexpected error occurred. Please try again later.",
        ).model_dump(),
    )


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(status_router)
app.include_router(generate_router)
app.include_router(execute_router)
app.include_router(repair_router)
app.include_router(agent_router)
app.include_router(test_router)
app.include_router(decision_router)
app.include_router(reviewer_router)
app.include_router(performance_router)
app.include_router(confidence_router)


# ---------------------------------------------------------------------------
# Root Endpoints
# ---------------------------------------------------------------------------


@app.get("/", tags=["root"])
async def root() -> Dict[str, str]:
    """
    Root endpoint providing basic service information.

    Returns:
        Dictionary with service name and version
    """
    return {
        "message": "Nexus AI Backend is running",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["root"])
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint for load balancers and monitoring.

    Returns:
        Dictionary with service health status
    """
    return {"status": "healthy", "service": "nexus-ai"}


# ---------------------------------------------------------------------------
# Lifecycle Events
# ---------------------------------------------------------------------------


@app.on_event("startup")
async def startup() -> None:
    """
    Application startup event handler.

    Initializes services and logs startup information.
    """
    logger.info(
        "Nexus AI backend starting",
        environment=settings.environment,
        version="0.1.0",
    )


@app.on_event("shutdown")
async def shutdown() -> None:
    """
    Application shutdown event handler.

    Cleans up resources and logs shutdown information.
    """
    logger.info("Nexus AI backend shutting down")
