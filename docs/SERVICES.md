# Services Documentation

Detailed documentation for each service in the Nexus AI backend.

## 📋 Table of Contents

- [Overview](#overview)
- [OpenAI Service](#openai-service)
- [Sandbox Service](#sandbox-service)
- [Testing Engine](#testing-engine)
- [Decision Engine](#decision-engine)
- [Code Reviewer](#code-reviewer)
- [Security Scanner](#security-scanner)
- [Performance Analyzer](#performance-analyzer)
- [Confidence Engine](#confidence-engine)
- [Healing Service](#healing-service)

---

## Overview

Nexus AI's backend is organized into specialized services, each responsible for a specific domain concern. Services are stateless, async-aware, and designed for testability.

### Service Architecture

```
services/
├── openai_service.py        # OpenAI API integration
├── sandbox_service.py       # Secure code execution
├── tester.py                # Test generation and execution
├── decision_engine.py       # Failure classification
├── code_reviewer.py         # Static code analysis
├── security_scanner.py      # Security vulnerability scanning
├── performance_analyzer.py  # Performance analysis
├── confidence_engine.py     # Confidence scoring
└── healing_service.py       # Self-healing orchestration
```

---

## OpenAI Service

### Purpose

Handles all communication with the OpenAI API for code generation, repair, and test generation.

### Location

`backend/app/services/openai_service.py`

### Interface

```python
class OpenAIService:
    def __init__(self, api_key: str, model: str) -> None:
        """
        Initialize OpenAI service.

        Args:
            api_key: OpenAI API key
            model: Model name (e.g., "gpt-4o")
        """

    async def generate_code(self, prompt: str, language: str = "python") -> str:
        """
        Generate code from a natural language prompt.

        Args:
            prompt: Natural language description of desired code
            language: Programming language (default: python)

        Returns:
            Generated code as string
        """

    async def repair_code(
        self,
        code: str,
        errors: list[str],
        prompt: str,
        language: str = "python"
    ) -> tuple[str, str]:
        """
        Repair code based on error messages.

        Args:
            code: Original code that failed
            errors: List of error messages
            prompt: Original prompt that generated the code
            language: Programming language

        Returns:
            Tuple of (repaired_code, explanation)
        """

    async def generate_tests(self, code: str, language: str = "python") -> str:
        """
        Generate pytest tests for provided code.

        Args:
            code: Code to generate tests for
            language: Programming language

        Returns:
            Generated test code as string
        """
```

### Usage Example

```python
from app.services.openai_service import OpenAIService

service = OpenAIService(
    api_key="sk-...",
    model="gpt-4o"
)

# Generate code
code = await service.generate_code(
    prompt="Write a factorial function",
    language="python"
)

# Repair code
repaired, explanation = await service.repair_code(
    code=code,
    errors=["TypeError: unsupported operand type(s)"],
    prompt="Write a factorial function"
)

# Generate tests
tests = await service.generate_tests(code=code)
```

### Configuration

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `OPENAI_MODEL` | Model name | `gpt-4o` |
| `OPENAI_ORG_ID` | Organization ID | Optional |
| `OPENAI_BASE_URL` | Custom API endpoint | `https://api.openai.com/v1` |

---

## Sandbox Service

### Purpose

Provides secure, isolated execution environments for running generated code with resource limits.

### Location

`backend/app/services/sandbox_service.py`

### Interface

```python
class SandboxService:
    def __init__(self, timeout: int = 30, memory_limit: int = 512) -> None:
        """
        Initialize sandbox service.

        Args:
            timeout: Maximum execution time in seconds
            memory_limit: Memory limit in MB
        """

    async def execute(self, code: str, language: str = "python") -> SandboxResult:
        """
        Execute code in isolated sandbox.

        Args:
            code: Code to execute
            language: Programming language

        Returns:
            SandboxResult with stdout, stderr, exit_code
        """

    def validate_code(self, code: str) -> ValidationResult:
        """
        Validate code before execution.

        Args:
            code: Code to validate

        Returns:
            ValidationResult with is_valid and errors
        """
```

### Usage Example

```python
from app.services.sandbox_service import SandboxService

sandbox = SandboxService(timeout=30, memory_limit=512)

# Execute code
result = await sandbox.execute(
    code="print('Hello, World!')",
    language="python"
)

print(result.stdout)   # "Hello, World!\n"
print(result.exit_code)  # 0
print(result.timed_out)  # False
```

### Security Features

- **Process Isolation**: Code runs in separate subprocess
- **Resource Limits**: CPU, memory, and time limits
- **File System Isolation**: Temporary directories only
- **Network Isolation**: No outbound network access

---

## Testing Engine

### Purpose

Generates and executes pytest tests for AI-generated Python code.

### Location

`backend/app/services/tester.py`

### Interface

```python
class TestingEngine:
    def __init__(self, timeout: int = 30) -> None:
        """
        Initialize testing engine.

        Args:
            timeout: Maximum test execution time in seconds
        """

    async def run_tests(
        self,
        code: str,
        test_cases: Optional[List[Dict[str, Any]]] = None,
        attempt: int = 1
    ) -> TestReport:
        """
        Execute tests for provided code.

        Args:
            code: Python code to test
            test_cases: Optional predefined test cases
            attempt: Current attempt number for tracking

        Returns:
            TestReport with complete results
        """

    def _save_code(self, code: str, temp_dir: Path) -> Path:
        """Save code to temporary file."""

    def _create_test_file(
        self,
        code: str,
        test_cases: Optional[List[Dict[str, Any]]],
        temp_dir: Path
    ) -> Path:
        """Create pytest test file."""

    def _build_test_content(self, code: str, test_cases: List[Dict[str, Any]]) -> str:
        """Build pytest test file content."""

    def to_dict(self, report: TestReport) -> Dict[str, Any]:
        """Convert TestReport to dictionary for JSON serialization."""
```

### Usage Example

```python
from app.services.tester import TestingEngine

engine = TestingEngine(timeout=30)

report = await engine.run_tests(
    code="def add(a, b): return a + b",
    test_cases=[
        {"name": "test_add", "call": "add(2, 3)", "expected": 5}
    ],
    attempt=1
)

print(f"Passed: {report.passed}")
print(f"Tests passed: {report.tests_passed}")
print(f"Tests failed: {report.tests_failed}")
print(f"Errors: {report.errors}")
```

### Test Case Format

```json
[
  {
    "name": "test_add_positive",
    "call": "add(2, 3)",
    "expected": 5
  },
  {
    "name": "test_add_negative",
    "call": "add(-1, 1)",
    "expected": 0
  }
]
```

---

## Decision Engine

### Purpose

Classifies failures and determines repair strategies using pattern matching instead of always calling OpenAI.

### Location

`backend/app/services/decision_engine.py`

### Interface

```python
class DecisionEngine:
    def __init__(self) -> None:
        """Initialize decision engine with classification rules."""

    def classify(
        self,
        error: str,
        context: Optional[Dict[str, Any]] = None
    ) -> FailureClassification:
        """
        Classify a failure based on error message and context.

        Args:
            error: The error message or output
            context: Additional context (code, execution_time, etc.)

        Returns:
            FailureClassification with type, severity, and repair strategy
        """

    def get_repair_prompt(
        self,
        error: str,
        code: str,
        failure_type: Optional[FailureType] = None
    ) -> str:
        """Get the appropriate repair prompt for a failure."""

    def get_repair_strategy(
        self,
        error: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Get the repair strategy for a failure."""

    def register_failure_type(
        self,
        failure_type: FailureType,
        patterns: List[str],
        severity: Severity,
        repair_strategy: str,
        base_prompt: str
    ) -> None:
        """Register a new failure type (extensibility)."""

    def analyze_execution_result(
        self,
        stdout: str,
        stderr: str,
        exit_code: int,
        execution_time: float,
        timeout: int = 30
    ) -> DecisionEngineResult:
        """Analyze execution results and classify any failures."""
```

### Failure Types

| Type | Severity | Patterns |
|------|----------|----------|
| `syntax` | HIGH | SyntaxError, IndentationError, TabError |
| `runtime` | MEDIUM | TypeError, ValueError, AttributeError, KeyError |
| `assertion` | MEDIUM | AssertionError, FAILED, test failed |
| `import` | HIGH | ImportError, ModuleNotFoundError |
| `timeout` | CRITICAL | timeout, timed out, TimeoutExpired |
| `security` | CRITICAL | PermissionError, AccessDenied |
| `performance` | MEDIUM | MemoryError, RecursionError |
| `unknown` | MEDIUM | Default fallback |

### Usage Example

```python
from app.services.decision_engine import DecisionEngine, FailureType, Severity

engine = DecisionEngine()

# Classify a failure
classification = engine.classify(
    error="TypeError: unsupported operand type(s) for +: 'int' and 'str'",
    context={"code": "def add(a, b): return a + b"}
)

print(classification.failure_type)  # FailureType.RUNTIME
print(classification.severity)       # Severity.MEDIUM
print(classification.repair_strategy)  # "Fix runtime errors..."
print(classification.suggested_prompt)  # "Fix the following Python runtime error..."
```

---

## Code Reviewer

### Purpose

Static analysis tool that detects code quality issues including unused variables, duplicate code, magic numbers, poor naming, missing comments, and missing type hints.

### Location

`backend/app/services/code_reviewer.py`

### Interface

```python
class CodeReviewer:
    def __init__(self, strict: bool = False) -> None:
        """
        Initialize code reviewer.

        Args:
            strict: Enable strict mode for more thorough checks
        """

    def review(self, code: str) -> CodeReviewReport:
        """
        Review Python code and return a report.

        Args:
            code: Python source code to review

        Returns:
            CodeReviewReport with all findings
        """

    def to_dict(self, report: CodeReviewReport) -> Dict[str, Any]:
        """Convert CodeReviewReport to dictionary for JSON serialization."""
```

### Check Categories

| Category | Severity | Description |
|----------|----------|-------------|
| `unused_variable` | MEDIUM | Variables assigned but never used |
| `duplicate_code` | HIGH | Duplicate code blocks |
| `magic_number` | MEDIUM | Hardcoded numbers without explanation |
| `poor_naming` | LOW | Naming convention violations |
| `missing_comments` | MEDIUM | Missing docstrings |
| `missing_type_hints` | MEDIUM | Missing type annotations |
| `syntax_error` | CRITICAL | Code has syntax errors |

### Usage Example

```python
from app.services.code_reviewer import CodeReviewer

reviewer = CodeReviewer(strict=True)
report = reviewer.review("""
def add(a, b):
    return a + b

x = 10
""")

for suggestion in report.suggestions:
    print(f"{suggestion.category}: {suggestion.message}")
    print(f"  Suggestion: {suggestion.suggestion}")
```

---

## Security Scanner

### Purpose

Scans Python code for security vulnerabilities including eval/exec usage, command injection, SQL injection, path traversal, unsafe subprocess, hardcoded secrets, and unsafe pickle.

### Location

`backend/app/services/security_scanner.py`

### Interface

```python
class SecurityScanner:
    def __init__(self, strict: bool = False) -> None:
        """
        Initialize security scanner.

        Args:
            strict: Enable strict mode for more thorough checks
        """

    def scan(self, code: str) -> SecurityScanReport:
        """
        Scan Python code for security vulnerabilities.

        Args:
            code: Python source code to scan

        Returns:
            SecurityScanReport with all findings
        """

    def to_dict(self, report: SecurityScanReport) -> Dict[str, Any]:
        """Convert SecurityScanReport to dictionary for JSON serialization."""
```

### Vulnerability Categories

| Category | Severity | Description |
|----------|----------|-------------|
| `eval` | CRITICAL | Use of eval() function |
| `exec` | CRITICAL | Use of exec() function |
| `command_injection` | CRITICAL | Shell command injection |
| `sql_injection` | CRITICAL | SQL injection vulnerabilities |
| `path_traversal` | HIGH | Directory traversal attacks |
| `unsafe_subprocess` | CRITICAL | Unsafe subprocess usage |
| `hardcoded_secret` | HIGH | Hardcoded passwords/keys |
| `unsafe_pickle` | CRITICAL | Unsafe pickle deserialization |
| `unsafe_yaml` | HIGH | yaml.load without SafeLoader |
| `ssl_verify_disabled` | HIGH | SSL verification disabled |
| `weak_cryptography` | HIGH | MD5 usage |
| `insecure_random` | MEDIUM | random module usage (strict mode) |

### Usage Example

```python
from app.services.security_scanner import SecurityScanner

scanner = SecurityScanner(strict=False)
report = scanner.scan("""
import os
user_input = input("Enter command: ")
os.system(user_input)
""")

for issue in report.issues:
    print(f"{issue.category} ({issue.severity}): {issue.risk}")
    print(f"  Recommendation: {issue.recommendation}")
```

---

## Performance Analyzer

### Purpose

Analyzes Python code to estimate time/space complexity, memory usage, and provide optimization suggestions with alternative algorithm recommendations.

### Location

`backend/app/services/performance_analyzer.py`

### Interface

```python
class PerformanceAnalyzer:
    def __init__(self, strict: bool = False) -> None:
        """
        Initialize performance analyzer.

        Args:
            strict: Enable strict mode for more thorough checks
        """

    def analyze(
        self,
        code: str,
        input_size: int = 1000
    ) -> PerformanceAnalysisReport:
        """
        Analyze Python code for performance characteristics.

        Args:
            code: Python source code to analyze
            input_size: Expected input size for estimation

        Returns:
            PerformanceAnalysisReport with all findings
        """

    def to_dict(self, report: PerformanceAnalysisReport) -> Dict[str, Any]:
        """Convert PerformanceAnalysisReport to dictionary."""
```

### Optimization Categories

| Category | Severity | Description |
|----------|----------|-------------|
| `nested_loops` | HIGH | Nested loops suggesting O(n²) |
| `list_in_loop` | MEDIUM | List append in loop |
| `string_concatenation` | MEDIUM | String concatenation in loop |
| `repeated_calculation` | LOW | Repeated function calls |
| `recursion` | MEDIUM | Recursive functions |
| `multiple_passes` | MEDIUM | Multiple passes over data |
| `inefficient_data_structure` | HIGH | List vs set/dict for lookups |
| `algorithm_efficiency` | HIGH | O(n²) or worse algorithms |
| `memory_usage` | MEDIUM | Memory inefficiencies |
| `loop_efficiency` | LOW | Loop condition inefficiencies |

### Usage Example

```python
from app.services.performance_analyzer import PerformanceAnalyzer

analyzer = PerformanceAnalyzer()
report = analyzer.analyze("""
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
""", input_size=1000)

print(f"Time Complexity: {report.complexity.time_complexity}")
print(f"Space Complexity: {report.complexity.space_complexity}")

for suggestion in report.suggestions:
    print(f"{suggestion.category}: {suggestion.message}")
    print(f"  Suggestion: {suggestion.suggestion}")
    print(f"  Improvement: {suggestion.estimated_improvement}")
```

---

## Confidence Engine

### Purpose

Calculates confidence scores for generated code based on multiple dimensions: tests, security, performance, repair attempts, documentation, and complexity.

### Location

`backend/app/services/confidence_engine.py`

### Interface

```python
class ConfidenceEngine:
    def __init__(self) -> None:
        """Initialize confidence engine with default weights."""

    def calculate(
        self,
        code: str,
        test_results: Optional[Any] = None,
        security_scan: Optional[Any] = None,
        performance_analysis: Optional[Any] = None,
        code_review: Optional[Any] = None,
        repair_attempts: int = 0,
        max_attempts: int = 5,
        has_documentation: bool = False,
        complexity_score: Optional[float] = None,
        language: str = "python"
    ) -> Dict[str, Any]:
        """
        Calculate confidence score for generated code.

        Args:
            code: Python source code
            test_results: Test results (optional)
            security_scan: Security scan results (optional)
            performance_analysis: Performance analysis results (optional)
            code_review: Code review results (optional)
            repair_attempts: Number of repair attempts needed
            max_attempts: Maximum allowed repair attempts
            has_documentation: Whether code has documentation
            complexity_score: Optional complexity score (0-1)
            language: Programming language

        Returns:
            Dictionary with score, grade, production_ready, explanation, etc.
        """
```

### Scoring Model

| Factor | Weight | Description |
|--------|--------|-------------|
| Tests | 30% | Based on pass rate and errors |
| Security | 20% | Deducts per issue severity |
| Performance | 15% | Deducts for suggestions and complexity |
| Repair | 10% | Exponential decay based on attempts |
| Documentation | 10% | Docstring coverage |
| Complexity | 15% | Cyclomatic complexity |

### Letter Grades

| Grade | Score Range | Production Ready |
|-------|-------------|------------------|
| A | 90-100 | Yes (if tests pass, no critical security issues) |
| B | 80-89 | Conditional |
| C | 70-79 | No |
| D | 60-69 | No |
| F | 0-59 | No |

### Usage Example

```python
from app.services.confidence_engine import ConfidenceEngine

engine = ConfidenceEngine()
result = engine.calculate(
    code="def add(a, b): return a + b",
    test_results=type('obj', (object,), {
        'passed': True,
        'tests_passed': 3,
        'tests_failed': 0,
        'errors': []
    })(),
    security_scan=type('obj', (object,), {
        'passed': True,
        'total_issues': 0,
        'critical_issues': 0
    })(),
    repair_attempts=1,
    max_attempts=5,
    has_documentation=True
)

print(f"Score: {result['score']}")
print(f"Grade: {result['letter_grade']}")
print(f"Production Ready: {result['production_ready']}")
print(f"Explanation: {result['explanation']}")
```

---

## Healing Service

### Purpose

Orchestrates the complete self-healing loop: generate → test → classify → repair → retest.

### Location

`backend/app/services/healing_service.py`

### Interface

```python
class HealingService:
    def __init__(
        self,
        openai_service: OpenAIService,
        sandbox_service: SandboxService,
        max_retries: int = 5,
    ) -> None:
        """
        Initialize healing service.

        Args:
            openai_service: OpenAI service for code generation
            sandbox_service: Sandbox service for code execution
            max_retries: Maximum number of repair attempts
        """

    async def run(self, context: ExecutionContext) -> ExecutionContext:
        """
        Run the self-healing loop.

        Args:
            context: Execution context with prompt and results

        Returns:
            Updated execution context with final results
        """
```

### Workflow

1. **Generate**: Create initial code from prompt
2. **Review**: Analyze code quality
3. **Security Scan**: Check for vulnerabilities
4. **Performance Analysis**: Analyze complexity
5. **Test**: Run test suite
6. **Classify**: Identify failure type
7. **Repair**: Fix identified issues
8. **Retest**: Verify fix
9. **Repeat**: Until success or max attempts

### Usage Example

```python
from app.services.healing_service import HealingService
from app.services.openai_service import OpenAIService
from app.services.sandbox_service import SandboxService
from app.models.entities import ExecutionContext

# Initialize services
openai_service = OpenAIService(api_key="sk-...", model="gpt-4o")
sandbox_service = SandboxService(timeout=30)
healing_service = HealingService(
    openai_service=openai_service,
    sandbox_service=sandbox_service,
    max_retries=5
)

# Create execution context
context = ExecutionContext(
    prompt="Write a factorial function",
    status="pending"
)

# Run self-healing loop
result = await healing_service.run(context)

print(f"Status: {result.status}")
print(f"Attempts: {result.attempts}")
print(f"Final Code: {result.code}")
```

---

## Next Steps

- [Architecture](./ARCHITECTURE.md) - System design overview
- [API Documentation](./API.md) - Complete API reference
- [Schemas Reference](./SCHEMAS.md) - Data models and schemas
