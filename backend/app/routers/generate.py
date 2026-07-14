from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import settings
from app.core.di import get_container
from app.models.schemas import GenerateRequest, GeneratedCodeResponse

router = APIRouter(prefix="/generate", tags=["generate"])


@router.post("", response_model=GeneratedCodeResponse)
async def generate(
    payload: GenerateRequest,
    container=Depends(get_container),
) -> GeneratedCodeResponse:
    try:
        code = await container.openai().generate_code(payload.prompt)
        return GeneratedCodeResponse(code=code, language="python")
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={"code": "OPENAI_ERROR", "message": str(exc)},
        ) from exc
