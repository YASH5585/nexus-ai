"""
Pydantic schemas for the testing API.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class TestRequest(BaseModel):
    """Request schema for running tests."""
    code: str = Field(..., min_length=1, description="Python code to test")
    language: str = Field(default="python", description="Programming language (currently only Python supported)")
    test_cases: Optional[List[Dict[str, Any]]] = Field(default=None, description="Optional predefined test cases")
    attempt: int = Field(default=1, ge=1, description="Attempt number for tracking")


class TestResponse(BaseModel):
    """Response schema for test results."""
    passed: bool = Field(description="Whether all tests passed")
    attempt: int = Field(description="Attempt number")
    execution_time: float = Field(description="Execution time in seconds")
    tests_passed: int = Field(description="Number of tests that passed")
    tests_failed: int = Field(description="Number of tests that failed")
    stdout: str = Field(description="Standard output from pytest")
    stderr: str = Field(description="Standard error from pytest")
    errors: List[str] = Field(default_factory=list, description="List of error messages")
    exit_code: int = Field(description="Process exit code")
