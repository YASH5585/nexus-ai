from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import configure_logging, logger
from app.core.exceptions import NexusAIException, handle_nexus_exception
from app.models.schemas import ErrorResponse
from app.routers.generate import router as generate_router
from app.routers.execute import router as execute_router
from app.routers.repair import router as repair_router
from app.routers.status import router as status_router
from app.routers.agent import router as agent_router

configure_logging()

app = FastAPI(
    title="Nexus AI Backend",
    description="Autonomous self-healing software engineer backend",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(NexusAIException)
async def nexus_exception_handler(request: Request, exc: NexusAIException) -> JSONResponse:
    logger.error("Nexus AI exception", code=exc.code, message=exc.message)
    http_exc = handle_nexus_exception(exc)
    return JSONResponse(
        status_code=http_exc.status_code,
        content=ErrorResponse(code=exc.code, message=exc.message).model_dump(),
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Unhandled exception", error=str(exc))
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(code="INTERNAL_ERROR", message="An unexpected error occurred").model_dump(),
    )


app.include_router(status_router)
app.include_router(generate_router)
app.include_router(execute_router)
app.include_router(repair_router)
app.include_router(agent_router)


@app.on_event("startup")
async def startup() -> None:
    logger.info("Nexus AI backend starting", environment=settings.environment)


@app.on_event("shutdown")
async def shutdown() -> None:
    logger.info("Nexus AI backend shutting down")
