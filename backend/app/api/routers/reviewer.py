"""
Code Reviewer API router.
"""

from fastapi import APIRouter, HTTPException, status
from app.schemas.reviewer import CodeReviewRequest
from app.services.code_reviewer import CodeReviewer
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/review", tags=["reviewer"])


@router.post("")
async def review_code(request: CodeReviewRequest) -> dict:
    """
    Review generated code for common issues.
    
    Args:
        request: Review request containing code to analyze
        
    Returns:
        Dictionary with review results
    """
    try:
        reviewer = CodeReviewer(strict=request.strict)
        report = reviewer.review(request.code)
        return reviewer.to_dict(report)
    except Exception as e:
        logger.error("Code review failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Code review failed: {str(e)}"
        )


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint for the code reviewer service."""
    return {"status": "healthy", "service": "code_reviewer"}
