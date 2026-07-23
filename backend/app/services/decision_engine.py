"""
AI Decision Engine for Nexus AI.

Classifies failures and determines repair strategies.
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import structlog

logger = structlog.get_logger(__name__)


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


class Severity(str, Enum):
    """Severity levels for failures."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class FailureClassification:
    """Result of failure classification."""
    failure_type: FailureType
    severity: Severity
    repair_strategy: str
    confidence: float
    suggested_prompt: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DecisionEngineResult:
    """Complete decision engine result."""
    classification: FailureClassification
    original_error: str
    context: Dict[str, Any]
    timestamp: float


class DecisionEngine:
    """
    AI-powered decision engine for classifying failures and determining repair strategies.
    
    Instead of sending every error to OpenAI, this engine classifies failures
    and uses targeted repair prompts for each category.
    """

    def __init__(self):
        """Initialize the decision engine with classification rules."""
        self.logger = logger.bind(component="DecisionEngine")
        
        # Define classification patterns
        self._patterns = {
            FailureType.SYNTAX: {
                "patterns": [
                    "SyntaxError", "IndentationError", "TabError",
                    "unexpected indent", "unexpected EOF", "invalid syntax"
                ],
                "severity": Severity.HIGH,
                "repair_strategy": "Fix syntax errors by correcting indentation, parentheses, or colons",
                "base_prompt": (
                    "Fix the following Python syntax error:\n{error}\n\n"
                    "Code:\n{code}\n\n"
                    "Return ONLY the corrected code. No explanations."
                )
            },
            FailureType.RUNTIME: {
                "patterns": [
                    "TypeError", "ValueError", "AttributeError", "KeyError",
                    "IndexError", "ZeroDivisionError", "NameError", "TypeError",
                    "RuntimeError", "NotImplementedError", "StopIteration",
                    "OSError", "IOError", "BlockingIOError", "ChildProcessError"
                ],
                "severity": Severity.MEDIUM,
                "repair_strategy": "Fix runtime errors by handling edge cases and type mismatches",
                "base_prompt": (
                    "Fix the following Python runtime error:\n{error}\n\n"
                    "Code:\n{code}\n\n"
                    "Return ONLY the corrected code. No explanations."
                )
            },
            FailureType.ASSERTION: {
                "patterns": [
                    "AssertionError", "assert ", "FAILED", "test failed"
                ],
                "severity": Severity.MEDIUM,
                "repair_strategy": "Fix assertion failures by correcting logic or expected values",
                "base_prompt": (
                    "Fix the following test assertion failure:\n{error}\n\n"
                    "Code:\n{code}\n\n"
                    "Return ONLY the corrected code. No explanations."
                )
            },
            FailureType.IMPORT: {
                "patterns": [
                    "ImportError", "ModuleNotFoundError", "No module named",
                    "cannot import name"
                ],
                "severity": Severity.HIGH,
                "repair_strategy": "Fix import errors by adding missing imports or correcting module paths",
                "base_prompt": (
                    "Fix the following Python import error:\n{error}\n\n"
                    "Code:\n{code}\n\n"
                    "Return ONLY the corrected code with proper imports. No explanations."
                )
            },
            FailureType.TIMEOUT: {
                "patterns": [
                    "timeout", "timed out", "TimeoutExpired", "Took too long"
                ],
                "severity": Severity.CRITICAL,
                "repair_strategy": "Optimize code to reduce execution time or increase timeout",
                "base_prompt": (
                    "Optimize the following code to reduce execution time:\n{error}\n\n"
                    "Code:\n{code}\n\n"
                    "Return ONLY the optimized code. No explanations."
                )
            },
            FailureType.SECURITY: {
                "patterns": [
                    "PermissionError", "AccessDenied", "Forbidden", "Unauthorized",
                    "security", "injection", "unsafe"
                ],
                "severity": Severity.CRITICAL,
                "repair_strategy": "Fix security issues by sanitizing inputs and using safe APIs",
                "base_prompt": (
                    "Fix the following security issue:\n{error}\n\n"
                    "Code:\n{code}\n\n"
                    "Return ONLY the secured code. No explanations."
                )
            },
            FailureType.PERFORMANCE: {
                "patterns": [
                    "MemoryError", "RecursionError", "too many open files",
                    "out of memory", "slow", "performance"
                ],
                "severity": Severity.MEDIUM,
                "repair_strategy": "Optimize code for better performance and memory usage",
                "base_prompt": (
                    "Optimize the following code for better performance:\n{error}\n\n"
                    "Code:\n{code}\n\n"
                    "Return ONLY the optimized code. No explanations."
                )
            }
        }

    def classify(self, error: str, context: Optional[Dict[str, Any]] = None) -> FailureClassification:
        """
        Classify a failure based on error message and context.
        
        Args:
            error: The error message or output
            context: Additional context (code, execution_time, etc.)
            
        Returns:
            FailureClassification with type, severity, and repair strategy
        """
        context = context or {}
        error_lower = error.lower()
        
        # Check each failure type pattern
        for failure_type, config in self._patterns.items():
            for pattern in config["patterns"]:
                if pattern.lower() in error_lower:
                    self.logger.info(
                        "Failure classified",
                        failure_type=failure_type.value,
                        severity=config["severity"].value,
                        pattern=pattern
                    )
                    
                    return FailureClassification(
                        failure_type=failure_type,
                        severity=config["severity"],
                        repair_strategy=config["repair_strategy"],
                        confidence=0.9,
                        suggested_prompt=config["base_prompt"].format(
                            error=error,
                            code=context.get("code", "")
                        ),
                        metadata={
                            "matched_pattern": pattern,
                            "context": context
                        }
                    )
        
        # Default to unknown
        self.logger.warning("Unknown failure type", error=error[:200])
        return FailureClassification(
            failure_type=FailureType.UNKNOWN,
            severity=Severity.MEDIUM,
            repair_strategy="General error fixing",
            confidence=0.5,
            suggested_prompt=(
                "Fix the following error:\n{error}\n\n"
                "Code:\n{code}\n\n"
                "Return ONLY the corrected code. No explanations."
            ).format(error=error, code=context.get("code", "")),
            metadata={"context": context}
        )

    def get_repair_prompt(self, error: str, code: str, failure_type: Optional[FailureType] = None) -> str:
        """
        Get the appropriate repair prompt for a failure.
        
        Args:
            error: The error message
            code: The code that failed
            failure_type: Optional pre-classified failure type
            
        Returns:
            Repair prompt string
        """
        if failure_type:
            config = self._patterns.get(failure_type)
            if config:
                return config["base_prompt"].format(error=error, code=code)
        
        # Classify first
        classification = self.classify(error, {"code": code})
        return classification.suggested_prompt

    def get_repair_strategy(self, error: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get the repair strategy for a failure.
        
        Args:
            error: The error message
            context: Additional context
            
        Returns:
            Dictionary with repair strategy information
        """
        classification = self.classify(error, context)
        
        return {
            "failure_type": classification.failure_type.value,
            "severity": classification.severity.value,
            "repair_strategy": classification.repair_strategy,
            "confidence": classification.confidence,
            "suggested_prompt": classification.suggested_prompt
        }

    def register_failure_type(
        self,
        failure_type: FailureType,
        patterns: List[str],
        severity: Severity,
        repair_strategy: str,
        base_prompt: str
    ) -> None:
        """
        Register a new failure type (extensibility).
        
        Args:
            failure_type: The failure type enum value
            patterns: List of patterns to match in error messages
            severity: Severity level for this failure type
            repair_strategy: Description of the repair strategy
            base_prompt: Base prompt template for repair
        """
        self._patterns[failure_type] = {
            "patterns": patterns,
            "severity": severity,
            "repair_strategy": repair_strategy,
            "base_prompt": base_prompt
        }
        
        self.logger.info(
            "New failure type registered",
            failure_type=failure_type.value,
            patterns_count=len(patterns)
        )

    def analyze_execution_result(
        self,
        stdout: str,
        stderr: str,
        exit_code: int,
        execution_time: float,
        timeout: int = 30
    ) -> DecisionEngineResult:
        """
        Analyze execution results and classify any failures.
        
        Args:
            stdout: Standard output from execution
            stderr: Standard error from execution
            exit_code: Process exit code
            execution_time: Execution time in seconds
            timeout: Timeout threshold in seconds
            
        Returns:
            DecisionEngineResult with classification
        """
        context = {
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": exit_code,
            "execution_time": execution_time,
            "timeout": timeout
        }
        
        # Check for timeout
        if execution_time >= timeout:
            return DecisionEngineResult(
                classification=FailureClassification(
                    failure_type=FailureType.TIMEOUT,
                    severity=Severity.CRITICAL,
                    repair_strategy="Optimize code to reduce execution time or increase timeout",
                    confidence=0.95,
                    suggested_prompt=self._patterns[FailureType.TIMEOUT]["base_prompt"].format(
                        error=f"Execution timed out after {execution_time}s",
                        code=""
                    ),
                    metadata={"execution_time": execution_time, "timeout": timeout}
                ),
                original_error=f"Execution timed out after {execution_time}s",
                context=context,
                timestamp=time.time()
            )
        
        # Check for failures
        if exit_code != 0:
            error_message = stderr or stdout or "Unknown error"
            classification = self.classify(error_message, context)
            
            return DecisionEngineResult(
                classification=classification,
                original_error=error_message,
                context=context,
                timestamp=time.time()
            )
        
        # Success
        return DecisionEngineResult(
            classification=FailureClassification(
                failure_type=FailureType.UNKNOWN,
                severity=Severity.LOW,
                repair_strategy="No repair needed",
                confidence=1.0,
                suggested_prompt="",
                metadata={"status": "success"}
            ),
            original_error="",
            context=context,
            timestamp=time.time()
        )
