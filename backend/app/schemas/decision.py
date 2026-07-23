"""
Schemas for the AI Decision Engine.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class FailureClassificationResponse(BaseModel):
    """Response schema for failure classification."""
    failure_type: str = Field(description="Type of failure (syntax, runtime, assertion, etc.)")
    severity: str = Field(description="Severity level (low, medium, high, critical)")
    repair_strategy: str = Field(description="Recommended repair strategy")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in classification")
    suggested_prompt: str = Field(description="AI prompt for repair")


class DecisionRequest(BaseModel):
    """Request schema for decision engine."""
    error: str = Field(..., min_length=1, description="Error message or output")
    stdout: Optional[str] = Field(default="", description="Standard output")
    stderr: Optional[str] = Field(default="", description="Standard error")
    exit_code: Optional[int] = Field(default=1, description="Process exit code")
    execution_time: Optional[float] = Field(default=0.0, description="Execution time in seconds")
    timeout: Optional[int] = Field(default=30, description="Timeout threshold in seconds")
    code: Optional[str] = Field(default="", description="Code that was executed")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context")


class DecisionResponse(BaseModel):
    """Response schema for decision engine."""
    failure_type: str
    severity: str
    repair_strategy: str
    confidence: float
    suggested_prompt: str
    original_error: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RegisterFailureTypeRequest(BaseModel):
    """Request schema for registering a new failure type."""
    failure_type: str = Field(..., min_length=1, description="Name of the failure type")
    patterns: List[str] = Field(..., min_length=1, description="Patterns to match in error messages")
    severity: str = Field(..., description="Severity level (low, medium, high, critical)")
    repair_strategy: str = Field(..., min_length=1, description="Repair strategy description")
    base_prompt: str = Field(..., min_length=1, description="Base prompt template for repair")
