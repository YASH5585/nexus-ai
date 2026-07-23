"""
Testing API router.
"""

from fastapi import APIRouter, HTTPException, status
from app.schemas.test import TestRequest, TestResponse
from app.services.tester import TestingEngine, TestGenerationError, TestExecutionError
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/test", tags=["testing"])


@router.post("/run", response_model=TestResponse)
async def run_tests(request: TestRequest) -> TestResponse:
    """
    Execute pytest tests for the provided code.
    
    Args:
        request: Test request containing code and optional test cases
        
    Returns:
        TestResponse with complete test results
    """
    try:
        engine = TestingEngine(timeout=30)
        report = await engine.run_tests(
            code=request.code,
            test_cases=request.test_cases,
            attempt=request.attempt
        )
        return engine.to_dict(report)
    except TestGenerationError as e:
        logger.error("Test generation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Test generation failed: {str(e)}"
        )
    except TestExecutionError as e:
        logger.error("Test execution failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Test execution failed: {str(e)}"
        )
    except Exception as e:
        logger.error("Unexpected error in test endpoint", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint for the testing service."""
    return {"status": "healthy", "service": "testing"}
