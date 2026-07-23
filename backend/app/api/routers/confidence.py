"""
Confidence Engine API router.
"""

from fastapi import APIRouter, HTTPException, status
from app.schemas.confidence import ConfidenceRequest
from app.services.confidence_engine import ConfidenceEngine
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/confidence", tags=["confidence"])


@router.post("")
async def calculate_confidence(request: ConfidenceRequest) -> dict:
    """
    Calculate confidence score for generated code.
    
    Args:
        request: Confidence request containing code and analysis results
        
    Returns:
        Dictionary with confidence score, grade, and explanation
    """
    try:
        engine = ConfidenceEngine()
        result = engine.calculate(
            code=request.code,
            test_results=request.test_results,
            security_scan=request.security_scan,
            performance_analysis=request.performance_analysis,
            code_review=request.code_review,
            repair_attempts=request.repair_attempts,
            max_attempts=request.max_attempts,
            has_documentation=request.has_documentation,
            complexity_score=request.complexity_score,
            language=request.language
        )
        return result
    except Exception as e:
        logger.error("Confidence calculation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Confidence calculation failed: {str(e)}"
        )


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint for the confidence engine service."""
    return {"status": "healthy", "service": "confidence_engine"}
