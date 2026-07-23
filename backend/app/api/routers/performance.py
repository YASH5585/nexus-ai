"""
Performance Analyzer API router.
"""

from fastapi import APIRouter, HTTPException, status
from app.schemas.performance import PerformanceAnalysisRequest
from app.services.performance_analyzer import PerformanceAnalyzer
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/performance", tags=["performance"])


@router.post("")
async def analyze_performance(request: PerformanceAnalysisRequest) -> dict:
    """
    Analyze code for performance characteristics and optimization opportunities.
    
    Args:
        request: Performance analysis request containing code to analyze
        
    Returns:
        Dictionary with performance analysis results
    """
    try:
        analyzer = PerformanceAnalyzer(strict=request.strict)
        report = analyzer.analyze(request.code, input_size=request.input_size or 1000)
        return analyzer.to_dict(report)
    except Exception as e:
        logger.error("Performance analysis failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Performance analysis failed: {str(e)}"
        )


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint for the performance analyzer service."""
    return {"status": "healthy", "service": "performance_analyzer"}
