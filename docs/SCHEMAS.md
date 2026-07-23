# Schemas Reference

Complete reference for all data models, schemas, and entities in Nexus AI.

## 📋 Table of Contents

- [Overview](#overview)
- [Pydantic Schemas](#pydantic-schemas)
  - [Test Schemas](#test-schemas)
  - [Decision Schemas](#decision-schemas)
  - [Reviewer Schemas](#reviewer-schemas)
  - [Security Schemas](#security-schemas)
  - [Performance Schemas](#performance-schemas)
  - [Confidence Schemas](#confidence-schemas)
- [Domain Entities](#domain-entities)
- [Enums](#enums)

---

## Overview

Nexus AI uses **Pydantic** for data validation and serialization. Schemas are organized by domain concern and are used for:

- **Request validation**: Ensure incoming data is valid
- **Response serialization**: Format outgoing data consistently
- **Documentation**: Auto-generate OpenAPI specs

### Schema Organization

```
backend/app/
├── schemas/
│   ├── test.py           # Testing schemas
│   ├── decision.py       # Decision engine schemas
│   ├── reviewer.py       # Code review schemas
│   ├── security.py       # Security scan schemas
│   ├── performance.py    # Performance analysis schemas
│   └── confidence.py     # Confidence scoring schemas
└── models/
    ├── schemas.py        # Core API schemas
    └── entities.py       # Domain entities
```

---

## Pydantic Schemas

### Test Schemas

**File**: `backend/app/schemas/test.py`

#### TestRequest

Request schema for running tests.

```python
class TestRequest(BaseModel):
    """Request schema for running tests."""
    code: str = Field(
        ...,
        min_length=1,
        description="Python code to test"
    )
    language: str = Field(
        default="python",
        description="Programming language (currently only Python supported)"
    )
    test_cases: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Optional predefined test cases"
    )
    attempt: int = Field(
        default=1,
        ge=1,
        description="Attempt number for tracking"
    )
```

**Example**:
```json
{
  "code": "def add(a, b): return a + b",
  "language": "python",
  "test_cases": [
    {
      "name": "test_add",
      "call": "add(2, 3)",
      "expected": 5
    }
  ],
  "attempt": 1
}
```

#### TestResponse

Response schema for test results.

```python
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
```

**Example**:
```json
{
  "passed": true,
  "attempt": 1,
  "execution_time": 0.12,
  "tests_passed": 3,
  "tests_failed": 0,
  "stdout": "test_add PASSED\n",
  "stderr": "",
  "errors": [],
  "exit_code": 0
}
```

---

### Decision Schemas

**File**: `backend/app/schemas/decision.py`

#### DecisionRequest

Request schema for decision engine.

```python
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
```

**Example**:
```json
{
  "error": "TypeError: unsupported operand type(s) for +: 'int' and 'str'",
  "stdout": "",
  "stderr": "TypeError: unsupported operand type(s) for +: 'int' and 'str'",
  "exit_code": 1,
  "execution_time": 0.05,
  "timeout": 30,
  "code": "def add(a, b): return a + b"
}
```

#### DecisionResponse

Response schema for decision engine.

```python
class DecisionResponse(BaseModel):
    """Response schema for decision engine."""
    failure_type: str
    severity: str
    repair_strategy: str
    confidence: float = Field(ge=0.0, le=1.0)
    suggested_prompt: str
    original_error: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
```

**Example**:
```json
{
  "failure_type": "runtime",
  "severity": "medium",
  "repair_strategy": "Fix runtime errors by handling edge cases and type mismatches",
  "confidence": 0.9,
  "suggested_prompt": "Fix the following Python runtime error:\nTypeError: ...",
  "original_error": "TypeError: unsupported operand type(s) for +: 'int' and 'str'",
  "metadata": {
    "matched_pattern": "TypeError",
    "context": {}
  }
}
```

#### RegisterFailureTypeRequest

Request schema for registering a new failure type.

```python
class RegisterFailureTypeRequest(BaseModel):
    """Request schema for registering a new failure type."""
    failure_type: str = Field(..., min_length=1, description="Name of the failure type")
    patterns: List[str] = Field(..., min_length=1, description="Patterns to match in error messages")
    severity: str = Field(..., description="Severity level (low, medium, high, critical)")
    repair_strategy: str = Field(..., min_length=1, description="Repair strategy description")
    base_prompt: str = Field(..., min_length=1, description="Base prompt template for repair")
```

---

### Reviewer Schemas

**File**: `backend/app/schemas/reviewer.py`

#### CodeReviewRequest

Request schema for code review.

```python
class CodeReviewRequest(BaseModel):
    """Request schema for code review."""
    code: str = Field(..., min_length=1, description="Python code to review")
    language: str = Field(default="python", description="Programming language")
    strict: bool = Field(default=False, description="Enable strict mode")
```

**Example**:
```json
{
  "code": "def add(a, b): return a + b",
  "language": "python",
  "strict": true
}
```

#### ReviewSuggestion

A single code review suggestion.

```python
class ReviewSuggestion(BaseModel):
    """A single code review suggestion."""
    category: str = Field(description="Category of the issue")
    severity: str = Field(description="Severity level")
    line_number: Optional[int] = Field(default=None, description="Line number")
    message: str = Field(description="Description of the issue")
    suggestion: str = Field(description="Suggested fix")
```

**Example**:
```json
{
  "category": "missing_comments",
  "severity": "medium",
  "line_number": 1,
  "message": "Function 'add' is missing a docstring",
  "suggestion": "Add a docstring explaining the purpose, parameters, and return value"
}
```

#### CodeReviewResponse

Response schema for code review results.

```python
class CodeReviewResponse(BaseModel):
    """Response schema for code review results."""
    passed: bool = Field(description="Whether code passed review")
    total_issues: int = Field(description="Total number of issues")
    suggestions: List[ReviewSuggestion] = Field(default_factory=list)
    summary: Dict[str, int] = Field(default_factory=dict)
    review_time: float = Field(description="Time taken to review")
```

---

### Security Schemas

**File**: `backend/app/schemas/security.py`

#### SecurityScanRequest

Request schema for security scanning.

```python
class SecurityScanRequest(BaseModel):
    """Request schema for security scanning."""
    code: str = Field(..., min_length=1, description="Python code to scan")
    language: str = Field(default="python", description="Programming language")
    strict: bool = Field(default=False, description="Enable strict mode")
```

#### SecurityIssue

A single security issue found during scanning.

```python
class SecurityIssue(BaseModel):
    """A single security issue found during scanning."""
    category: str = Field(description="Category of the issue")
    severity: str = Field(description="Severity level")
    risk: str = Field(description="Description of the security risk")
    line_number: Optional[int] = Field(default=None, description="Line number")
    code_snippet: Optional[str] = Field(default=None, description="Code snippet")
    recommendation: str = Field(description="Recommendation for fixing")
```

**Example**:
```json
{
  "category": "command_injection",
  "severity": "critical",
  "risk": "Command injection vulnerability: shell=True allows arbitrary command execution",
  "line_number": 2,
  "code_snippet": "os.system(user_input)",
  "recommendation": "Avoid using shell=True. Use array-style arguments instead"
}
```

#### SecurityScanResponse

Response schema for security scan results.

```python
class SecurityScanResponse(BaseModel):
    """Response schema for security scan results."""
    passed: bool = Field(description="Whether code passed security scan")
    total_issues: int = Field(description="Total number of issues")
    issues: List[SecurityIssue] = Field(default_factory=list)
    summary: Dict[str, int] = Field(default_factory=dict)
    scan_time: float = Field(description="Time taken to scan")
```

---

### Performance Schemas

**File**: `backend/app/schemas/performance.py`

#### PerformanceAnalysisRequest

Request schema for performance analysis.

```python
class PerformanceAnalysisRequest(BaseModel):
    """Request schema for performance analysis."""
    code: str = Field(..., min_length=1, description="Python code to analyze")
    language: str = Field(default="python", description="Programming language")
    input_size: Optional[int] = Field(default=1000, description="Expected input size")
    strict: bool = Field(default=False, description="Enable strict mode")
```

#### OptimizationSuggestion

A single optimization suggestion.

```python
class OptimizationSuggestion(BaseModel):
    """A single optimization suggestion."""
    category: str = Field(description="Category of the suggestion")
    severity: str = Field(description="Severity level")
    line_number: Optional[int] = Field(default=None, description="Line number")
    message: str = Field(description="Description of the optimization")
    suggestion: str = Field(description="Specific recommendation")
    estimated_improvement: str = Field(description="Estimated performance improvement")
```

#### ComplexityEstimate

Complexity estimation for a function or code block.

```python
class ComplexityEstimate(BaseModel):
    """Complexity estimation for a function or code block."""
    time_complexity: str = Field(description="Big O time complexity")
    space_complexity: str = Field(description="Big O space complexity")
    estimated_memory_mb: Optional[float] = Field(default=None, description="Estimated memory usage")
```

#### AlternativeAlgorithm

Suggested alternative algorithm.

```python
class AlternativeAlgorithm(BaseModel):
    """Suggested alternative algorithm."""
    name: str = Field(description="Name of the alternative algorithm")
    time_complexity: str = Field(description="Time complexity of the alternative")
    space_complexity: str = Field(description="Space complexity of the alternative")
    description: str = Field(description="Description of the algorithm")
    use_case: str = Field(description="When to use this algorithm")
```

#### PerformanceAnalysisResponse

Response schema for performance analysis results.

```python
class PerformanceAnalysisResponse(BaseModel):
    """Response schema for performance analysis results."""
    passed: bool = Field(description="Whether code passes performance checks")
    total_suggestions: int = Field(description="Total optimization suggestions")
    complexity: ComplexityEstimate = Field(description="Complexity estimates")
    suggestions: List[OptimizationSuggestion] = Field(default_factory=list)
    alternative_algorithms: List[AlternativeAlgorithm] = Field(default_factory=list)
    summary: Dict[str, int] = Field(default_factory=dict)
    analysis_time: float = Field(description="Time taken to analyze")
```

---

### Confidence Schemas

**File**: `backend/app/schemas/confidence.py`

#### ConfidenceRequest

Request schema for confidence calculation.

```python
class ConfidenceRequest(BaseModel):
    """Request schema for confidence calculation."""
    code: str = Field(..., min_length=1, description="Python code to evaluate")
    test_results: Optional[TestResultsInput] = Field(default=None)
    security_scan: Optional[SecurityScanInput] = Field(default=None)
    performance_analysis: Optional[PerformanceAnalysisInput] = Field(default=None)
    code_review: Optional[CodeReviewInput] = Field(default=None)
    repair_attempts: int = Field(default=0, ge=0, description="Number of repair attempts")
    max_attempts: int = Field(default=5, ge=1, description="Maximum allowed attempts")
    has_documentation: bool = Field(default=False, description="Whether code has docstrings")
    complexity_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    language: str = Field(default="python", description="Programming language")
```

#### ConfidenceResponse

Response schema for confidence calculation.

```python
class ConfidenceResponse(BaseModel):
    """Response schema for confidence calculation."""
    score: float = Field(ge=0.0, le=100.0, description="Confidence score (0-100)")
    letter_grade: str = Field(description="Letter grade (A, B, C, D, F)")
    production_ready: bool = Field(description="Whether code is production ready")
    explanation: str = Field(description="Human-readable confidence explanation")
    breakdown: Dict[str, Any] = Field(default_factory=dict, description="Score breakdown")
    recommendations: List[str] = Field(default_factory=list, description="Improvement recommendations")
```

**Example**:
```json
{
  "score": 96.4,
  "letter_grade": "A",
  "production_ready": true,
  "explanation": "Code is production-ready with a confidence score of 96.4/100...",
  "breakdown": {
    "test_score": 100.0,
    "security_score": 100.0,
    "performance_score": 100.0,
    "repair_score": 64.0,
    "documentation_score": 100.0,
    "complexity_score": 100.0,
    "weights": {
      "test": 0.30,
      "security": 0.20,
      "performance": 0.15,
      "repair": 0.10,
      "documentation": 0.10,
      "complexity": 0.15
    }
  },
  "recommendations": []
}
```

---

## Domain Entities

**File**: `backend/app/models/entities.py`

### ExecutionContext

Context for agent execution.

```python
@dataclass
class ExecutionContext:
    """Context for agent execution."""
    prompt: str
    status: str = "pending"
    code: Optional[str] = None
    attempts: int = 0
    errors: List[str] = field(default_factory=list)
    steps: List[ExecutionStep] = field(default_factory=list)

    def add_step(self, step: ExecutionStep) -> None:
        """Add an execution step."""
```

### ExecutionStep

Individual step in execution flow.

```python
@dataclass
class ExecutionStep:
    """Individual step in execution flow."""
    id: str
    label: str
    status: StepStatus = StepStatus.pending
    detail: Optional[str] = None
    timestamp: float = field(default_factory=time.time)
```

### StepStatus

Enum for step status.

```python
class StepStatus(str, Enum):
    """Status of an execution step."""
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"
```

### TestResult

Individual test result.

```python
@dataclass
class TestResult:
    """Individual test result."""
    name: str
    passed: bool
    error_message: Optional[str] = None
    duration_ms: float = 0.0
```

### TestReport

Complete test execution report.

```python
@dataclass
class TestReport:
    """Complete test execution report."""
    passed: bool
    tests_passed: int
    tests_failed: int
    errors: List[str]
    stdout: str
    stderr: str
    exit_code: int
    duration_ms: float
    attempt: int = 1
```

---

## Enums

### FailureType

**File**: `backend/app/services/decision_engine.py`

```python
class FailureType(str, Enum):
    """Types of failures that can occur during code execution."""
    SYNTAX = "syntax"
    RUNTIME = "runtime"
    ASSERTION = "assertion"
    IMPORT = "import"
    TIMEOUT = "timeout"
    SECURITY = "security"
    PERFORMANCE = "performance"
    UNKNOWN = "unknown"
```

### Severity

**File**: `backend/app/services/decision_engine.py`

```python
class Severity(str, Enum):
    """Severity levels for failures."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
```

---

## Next Steps

- [Architecture](./ARCHITECTURE.md) - System design overview
- [Services Documentation](./SERVICES.md) - Detailed service documentation
- [API Documentation](./API.md) - Complete API reference
