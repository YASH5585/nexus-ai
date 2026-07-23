"""
Schemas for the AI Code Reviewer.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ReviewSuggestion(BaseModel):
    """A single code review suggestion."""
    category: str = Field(description="Category of the issue (unused_variable, duplicate_code, magic_number, poor_naming, missing_comments, missing_type_hints)")
    severity: str = Field(description="Severity level (low, medium, high, critical)")
    line_number: Optional[int] = Field(default=None, description="Line number where the issue was found")
    message: str = Field(description="Description of the issue")
    suggestion: str = Field(description="Suggested fix")


class CodeReviewRequest(BaseModel):
    """Request schema for code review."""
    code: str = Field(..., min_length=1, description="Python code to review")
    language: str = Field(default="python", description="Programming language (currently only Python supported)")
    strict: bool = Field(default=False, description="Enable strict mode for more thorough checks")


class CodeReviewResponse(BaseModel):
    """Response schema for code review results."""
    passed: bool = Field(description="Whether the code passed review without issues")
    total_issues: int = Field(description="Total number of issues found")
    suggestions: List[ReviewSuggestion] = Field(default_factory=list, description="List of review suggestions")
    summary: Dict[str, int] = Field(default_factory=dict, description="Summary of issues by category")
    review_time: float = Field(description="Time taken to review in seconds")
