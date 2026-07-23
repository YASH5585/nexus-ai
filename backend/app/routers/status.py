from fastapi import APIRouter, Depends

from app.core.config import settings
from app.core.di import get_container

router = APIRouter(tags=["status"])


@router.get("/status")
async def status() -> dict:
    return {
        "status": "ok",
        "environment": settings.environment,
        "model": settings.openai_model,
        "max_retries": settings.max_retries,
    }
