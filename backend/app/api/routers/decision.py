"""
Decision Engine API router.
"""

from fastapi import APIRouter, HTTPException, status
from app.schemas.decision import (
    DecisionRequest,
    DecisionResponse,
    RegisterFailureTypeRequest
)
from app.services.decision_engine import (
    DecisionEngine,
    FailureType,
    Severity
)
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/decision", tags=["decision"])

# Initialize decision engine
decision_engine = DecisionEngine()


@router.post("/classify", response_model=DecisionResponse)
async def classify_failure(request: DecisionRequest) -> DecisionResponse:
    """
    Classify a failure and determine repair strategy.
    
    Args:
        request: Decision request containing error details and context
        
    Returns:
        DecisionResponse with classification and repair strategy
    """
    try:
        context = request.context or {}
        if request.code:
            context["code"] = request.code
        context.update({
            "stdout": request.stdout,
            "stderr": request.stderr,
            "exit_code": request.exit_code,
            "execution_time": request.execution_time,
            "timeout": request.timeout
        })
        
        result = decision_engine.analyze_execution_result(
            stdout=request.stdout or "",
            stderr=request.stderr or "",
            exit_code=request.exit_code or 1,
            execution_time=request.execution_time or 0.0,
            timeout=request.timeout or 30
        )
        
        return DecisionResponse(
            failure_type=result.classification.failure_type.value,
            severity=result.classification.severity.value,
            repair_strategy=result.classification.repair_strategy,
            confidence=result.classification.confidence,
            suggested_prompt=result.classification.suggested_prompt,
            original_error=result.original_error,
            metadata=result.classification.metadata
        )
    except Exception as e:
        logger.error("Decision engine classification failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Classification failed: {str(e)}"
        )


@router.post("/repair-prompt")
async def get_repair_prompt(request: DecisionRequest) -> Dict[str, str]:
    """
    Get the appropriate repair prompt for a failure.
    
    Args:
        request: Decision request containing error and code
        
    Returns:
        Dictionary with repair prompt
    """
    try:
        prompt = decision_engine.get_repair_prompt(
            error=request.error,
            code=request.code or ""
        )
        return {"repair_prompt": prompt}
    except Exception as e:
        logger.error("Failed to generate repair prompt", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate repair prompt: {str(e)}"
        )


@router.post("/register-failure-type")
async def register_failure_type(request: RegisterFailureTypeRequest) -> Dict[str, str]:
    """
    Register a new failure type (extensibility).
    
    Args:
        request: Failure type registration request
        
    Returns:
        Success message
    """
    try:
        failure_type = FailureType(request.failure_type)
        decision_engine.register_failure_type(
            failure_type=failure_type,
            patterns=request.patterns,
            severity=Severity(request.severity),
            repair_strategy=request.repair_strategy,
            base_prompt=request.base_prompt
        )
        return {"message": f"Failure type '{request.failure_type}' registered successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid failure type or severity: {str(e)}"
        )
    except Exception as e:
        logger.error("Failed to register failure type", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.get("/failure-types")
async def list_failure_types() -> Dict[str, List[str]]:
    """List all registered failure types."""
    return {
        "failure_types": [ft.value for ft in FailureType]
    }
