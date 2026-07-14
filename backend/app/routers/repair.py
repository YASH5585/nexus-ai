from fastapi import APIRouter, Depends, HTTPException, status

from app.core.di import get_container
from app.models.schemas import RepairRequest, RepairResponse

router = APIRouter(prefix="/repair", tags=["repair"])


@router.post("", response_model=RepairResponse)
async def repair(
    payload: RepairRequest,
    container=Depends(get_container),
) -> RepairResponse:
    try:
        patched_code, explanation = await container.openai().repair_code(
            code=payload.code,
            errors=payload.errors,
            prompt=payload.prompt,
            language=payload.language,
        )
        return RepairResponse(patched_code=patched_code, explanation=explanation, confidence=0.9)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={"code": "OPENAI_ERROR", "message": str(exc)},
        ) from exc
