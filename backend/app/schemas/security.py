"""
Schemas for the Security Scanner.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class SecurityIssue(BaseModel):
    """A single security issue found during scanning."""
    category: str = Field(description="Category of the issue (eval, exec, command_injection, sql_injection, path_traversal, unsafe_subprocess, hardcoded_secret, unsafe_pickle)")
    severity: str = Field(description="Severity level (low, medium, high, critical)")
    risk: str = Field(description="Description of the security risk")
    line_number: Optional[int] = Field(default=None, description="Line number where the issue was found")
    code_snippet: Optional[str] = Field(default=None, description="Code snippet containing the issue")
    recommendation: str = Field(description="Recommendation for fixing the issue")


class SecurityScanRequest(BaseModel):
    """Request schema for security scanning."""
    code: str = Field(..., min_length=1, description="Python code to scan for security issues")
    language: str = Field(default="python", description="Programming language (currently only Python supported)")
    strict: bool = Field(default=False, description="Enable strict mode for more thorough checks")


class SecurityScanResponse(BaseModel):
    """Response schema for security scan results."""
    passed: bool = Field(description="Whether the code passed security scan without issues")
    total_issues: int = Field(description="Total number of security issues found")
    issues: List[SecurityIssue] = Field(default_factory=list, description="List of security issues")
    summary: Dict[str, int] = Field(default_factory=dict, description="Summary of issues by category")
    scan_time: float = Field(description="Time taken to scan in seconds")
