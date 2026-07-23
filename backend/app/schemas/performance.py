"""
Schemas for the Performance Analyzer.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class OptimizationSuggestion(BaseModel):
    """A single optimization suggestion."""
    category: str = Field(description="Category of the suggestion (algorithm, data_structure, loop, memory, caching)")
    severity: str = Field(description="Severity level (low, medium, high, critical)")
    line_number: Optional[int] = Field(default=None, description="Line number where the optimization applies")
    message: str = Field(description="Description of the optimization")
    suggestion: str = Field(description="Specific optimization recommendation")
    estimated_improvement: str = Field(description="Estimated performance improvement")


class ComplexityEstimate(BaseModel):
    """Complexity estimation for a function or code block."""
    time_complexity: str = Field(description="Big O time complexity (e.g., O(n), O(n^2), O(log n))")
    space_complexity: str = Field(description="Big O space complexity")
    estimated_memory_mb: Optional[float] = Field(default=None, description="Estimated memory usage in MB")


class AlternativeAlgorithm(BaseModel):
    """Suggested alternative algorithm."""
    name: str = Field(description="Name of the alternative algorithm")
    time_complexity: str = Field(description="Time complexity of the alternative")
    space_complexity: str = Field(description="Space complexity of the alternative")
    description: str = Field(description="Description of the algorithm")
    use_case: str = Field(description="When to use this algorithm")


class PerformanceAnalysisRequest(BaseModel):
    """Request schema for performance analysis."""
    code: str = Field(..., min_length=1, description="Python code to analyze")
    language: str = Field(default="python", description="Programming language (currently only Python supported)")
    input_size: Optional[int] = Field(default=1000, description="Expected input size for estimation")
    strict: bool = Field(default=False, description="Enable strict mode for more thorough checks")


class PerformanceAnalysisResponse(BaseModel):
    """Response schema for performance analysis results."""
    passed: bool = Field(description="Whether the code passes performance checks")
    total_suggestions: int = Field(description="Total number of optimization suggestions")
    complexity: ComplexityEstimate = Field(description="Complexity estimates")
    suggestions: List[OptimizationSuggestion] = Field(default_factory=list, description="List of optimization suggestions")
    alternative_algorithms: List[AlternativeAlgorithm] = Field(default_factory=list, description="Suggested alternative algorithms")
    summary: Dict[str, int] = Field(default_factory=dict, description="Summary of suggestions by category")
    analysis_time: float = Field(description="Time taken to analyze in seconds")
