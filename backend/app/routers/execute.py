from fastapi import APIRouter, Depends, HTTPException, status

from app.core.di import get_container
from app.models.schemas import ExecuteRequest, ExecuteResponse
from app.services.sandbox_service import SandboxError

router = APIRouter(prefix="/execute", tags=["execute"])


@router.post("", response_model=ExecuteResponse)
async def execute(
    payload: ExecuteRequest,
    container=Depends(get_container),
) -> ExecuteResponse:
    try:
        result = container.sandbox().execute(payload.code, payload.tests)
        return ExecuteResponse(
            stdout=result.stdout,
            stderr=result.stderr,
            return_code=result.return_code,
            duration_ms=result.duration_ms,
        )
    except SandboxError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "SANDBOX_ERROR", "message": str(exc)},
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": "INTERNAL_ERROR", "message": str(exc)},
        ) from exc
