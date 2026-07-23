"""
Schemas for the Confidence Engine.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class TestResultsInput(BaseModel):
    """Test results for confidence calculation."""
    passed: bool
    tests_passed: int
    tests_failed: int
    execution_time: float
    errors: List[str] = Field(default_factory=list)


class SecurityScanInput(BaseModel):
    """Security scan results for confidence calculation."""
    passed: bool
    total_issues: int
    critical_issues: int = 0
    high_issues: int = 0
    medium_issues: int = 0
    low_issues: int = 0


class PerformanceAnalysisInput(BaseModel):
    """Performance analysis results for confidence calculation."""
    passed: bool
    time_complexity: str
    space_complexity: str
    total_suggestions: int
    high_suggestions: int = 0
    medium_suggestions: int = 0
    low_suggestions: int = 0


class CodeReviewInput(BaseModel):
    """Code review results for confidence calculation."""
    passed: bool
    total_issues: int
    high_issues: int = 0
    medium_issues: int = 0
    low_issues: int = 0


class ConfidenceRequest(BaseModel):
    """Request schema for confidence calculation."""
    code: str = Field(..., min_length=1, description="Python code to evaluate")
    test_results: Optional[TestResultsInput] = Field(default=None, description="Test execution results")
    security_scan: Optional[SecurityScanInput] = Field(default=None, description="Security scan results")
    performance_analysis: Optional[PerformanceAnalysisInput] = Field(default=None, description="Performance analysis results")
    code_review: Optional[CodeReviewInput] = Field(default=None, description="Code review results")
    repair_attempts: int = Field(default=0, ge=0, description="Number of repair attempts needed")
    max_attempts: int = Field(default=5, ge=1, description="Maximum allowed repair attempts")
    has_documentation: bool = Field(default=False, description="Whether code has documentation/docstrings")
    complexity_score: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Complexity score (0-1, lower is better)")
    language: str = Field(default="python", description="Programming language")


class ConfidenceResponse(BaseModel):
    """Response schema for confidence calculation."""
    score: float = Field(ge=0.0, le=100.0, description="Confidence score (0-100)")
    letter_grade: str = Field(description="Letter grade (A, B, C, D, F)")
    production_ready: bool = Field(description="Whether code is production ready")
    explanation: str = Field(description="Human-readable confidence explanation")
    breakdown: Dict[str, Any] = Field(default_factory=dict, description="Detailed score breakdown")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations for improvement")
