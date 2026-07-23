"""
Nexus AI Testing Engine.

A robust service for executing and validating AI-generated Python code
against predefined test suites using pytest.

This module provides:
- Temporary file management for code and test files
- pytest execution in isolated subprocesses
- Structured result parsing and reporting
- Timeout and error handling
- JSON serialization for API responses

Example:
    Basic usage:

        engine = TestingEngine(timeout=30)
        report = await engine.run_tests(
            code="def add(a, b): return a + b",
            attempt=1
        )
        print(f"Passed: {report.passed}")
        print(f"Tests: {report.tests_passed}/{report.tests_passed + report.tests_failed}")

    With custom test cases:

        report = await engine.run_tests(
            code="def factorial(n): ...",
            test_cases=[
                {"name": "test_factorial_5", "call": "factorial(5)", "expected": 120}
            ],
            attempt=1
        )
"""

import asyncio
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import structlog
import sys

from app.core.config import settings

logger = structlog.get_logger(__name__)


@dataclass
class TestResult:
    """Individual test result."""
    name: str
    passed: bool
    error_message: Optional[str] = None
    duration_ms: float = 0.0


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


class TestGenerationError(Exception):
    """Raised when test generation fails."""
    pass


class TestExecutionError(Exception):
    """Raised when test execution fails."""
    pass


class TestingEngine:
    """
    Production-ready testing engine for AI-generated Python code.

    This engine provides a complete testing pipeline:
    1. Saves generated code to temporary files
    2. Generates pytest test cases (or uses provided ones)
    3. Executes tests in an isolated subprocess sandbox
    4. Captures stdout, stderr, and exit codes
    5. Parses pytest output into structured results
    6. Handles timeouts and errors gracefully

    Attributes:
        timeout: Maximum execution time in seconds for pytest
        logger: Structured logger instance

    Example:
        engine = TestingEngine(timeout=30)
        report = await engine.run_tests(code=code, attempt=1)
        if report.passed:
            print("All tests passed!")
        else:
            print(f"Tests failed: {report.errors}")
    """

    def __init__(self, timeout: int = 30):
        """
        Initialize the testing engine.

        Args:
            timeout: Maximum execution time in seconds for pytest.
                     Defaults to 30 seconds.

        Raises:
            ValueError: If timeout is not a positive integer
        """
        if timeout <= 0:
            raise ValueError(f"timeout must be positive, got {timeout}")
        self.timeout = timeout
        self.logger = logger.bind(component="TestingEngine")

    async def run_tests(
        self,
        code: str,
        test_cases: Optional[List[Dict[str, Any]]] = None,
        attempt: int = 1
    ) -> TestReport:
        """
        Execute tests for the provided code.

        This is the main entry point for the testing engine. It:
        1. Creates a temporary directory
        2. Saves the generated code to a file
        3. Creates a pytest test file
        4. Executes pytest in a subprocess
        5. Parses the results into a TestReport

        Args:
            code: Python code to test
            test_cases: Optional list of test case definitions.
                        Each test case should have:
                        - name: Test function name
                        - call: Function call to test (e.g., "add(2, 3)")
                        - expected: Expected return value
            attempt: Current attempt number for tracking (default: 1)

        Returns:
            TestReport with complete results including:
            - passed: Whether all tests passed
            - tests_passed: Number of passing tests
            - tests_failed: Number of failing tests
            - errors: List of error messages
            - stdout/stderr: Pytest output
            - exit_code: Process exit code
            - duration_ms: Execution time in milliseconds

        Raises:
            TestGenerationError: If test file generation fails
            TestExecutionError: If test execution fails

        Example:
            engine = TestingEngine(timeout=30)
            report = await engine.run_tests(
                code="def add(a, b): return a + b",
                test_cases=[
                    {"name": "test_add", "call": "add(2, 3)", "expected": 5}
                ],
                attempt=1
            )
        """
        self.logger.info(
            "Starting test execution",
            code_length=len(code),
            attempt=attempt,
            has_test_cases=test_cases is not None
        )

        start_time = time.perf_counter()
        
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Save the generated code
                code_file = self._save_code(code, temp_path)
                self.logger.debug("Code saved", file=str(code_file))
                
                # Create test file
                test_file = self._create_test_file(code, test_cases, temp_path)
                self.logger.debug("Test file created", file=str(test_file))
                
                # Execute pytest
                result = await self._execute_pytest(test_file, temp_path)
                
                # Parse results
                report = self._parse_results(result, attempt)
                report.duration_ms = (time.perf_counter() - start_time) * 1000
                
                self.logger.info(
                    "Test execution completed",
                    passed=report.passed,
                    tests_passed=report.tests_passed,
                    tests_failed=report.tests_failed,
                    duration_ms=report.duration_ms
                )
                
                return report
                
        except subprocess.TimeoutExpired:
            self.logger.error("Test execution timed out", timeout=self.timeout)
            return TestReport(
                passed=False,
                tests_passed=0,
                tests_failed=0,
                errors=[f"Execution timed out after {self.timeout} seconds"],
                stdout="",
                stderr="Timeout",
                exit_code=-1,
                duration_ms=(time.perf_counter() - start_time) * 1000,
                attempt=attempt
            )
        except Exception as e:
            self.logger.error("Unexpected error during test execution", error=str(e))
            return TestReport(
                passed=False,
                tests_passed=0,
                tests_failed=0,
                errors=[f"Unexpected error: {str(e)}"],
                stdout="",
                stderr=str(e),
                exit_code=-2,
                duration_ms=(time.perf_counter() - start_time) * 1000,
                attempt=attempt
            )

    def _save_code(self, code: str, temp_dir: Path) -> Path:
        """
        Save generated code to a temporary file.
        
        Args:
            code: Python code string
            temp_dir: Temporary directory path
            
        Returns:
            Path to the saved code file
        """
        code_file = temp_dir / "solution.py"
        code_file.write_text(code, encoding="utf-8")
        return code_file

    def _create_test_file(
        self,
        code: str,
        test_cases: Optional[List[Dict[str, Any]]],
        temp_dir: Path
    ) -> Path:
        """
        Create a pytest test file with generated test cases.
        
        Args:
            code: The source code being tested (for introspection)
            test_cases: Optional predefined test cases
            temp_dir: Temporary directory path
            
        Returns:
            Path to the created test file
        """
        test_file = temp_dir / "test_solution.py"
        
        # Generate test cases if not provided
        if not test_cases:
            test_cases = self._generate_test_cases(code)
        
        # Build test file content
        test_content = self._build_test_content(code, test_cases)
        test_file.write_text(test_content, encoding="utf-8")
        
        return test_file

    def _generate_test_cases(self, code: str) -> List[Dict[str, Any]]:
        """
        Generate test cases based on the code structure.
        
        Args:
            code: Python source code
            
        Returns:
            List of test case definitions
        """
        test_cases = []
        
        # Simple heuristic-based test generation
        # In production, this would use AI to generate comprehensive tests
        if "def add(" in code or "def sum(" in code:
            test_cases.extend([
                {"name": "test_add_positive", "call": "add(2, 3)", "expected": 5},
                {"name": "test_add_negative", "call": "add(-1, 1)", "expected": 0},
                {"name": "test_add_zero", "call": "add(0, 0)", "expected": 0},
            ])
        
        if "def factorial(" in code:
            test_cases.extend([
                {"name": "test_factorial_zero", "call": "factorial(0)", "expected": 1},
                {"name": "test_factorial_one", "call": "factorial(1)", "expected": 1},
                {"name": "test_factorial_five", "call": "factorial(5)", "expected": 120},
            ])
        
        if "def palindrome(" in code or "def is_palindrome(" in code:
            test_cases.extend([
                {"name": "test_palindrome_empty", "call": 'palindrome("")', "expected": True},
                {"name": "test_palindrome_single", "call": 'palindrome("a")', "expected": True},
                {"name": "test_palindrome_even", "call": 'palindrome("abba")', "expected": True},
                {"name": "test_palindrome_odd", "call": 'palindrome("racecar")', "expected": True},
                {"name": "test_palindrome_false", "call": 'palindrome("hello")', "expected": False},
            ])
        
        # Default test if no patterns matched
        if not test_cases:
            test_cases.append({
                "name": "test_basic_execution",
                "call": "None",
                "expected": "pass"
            })
        
        return test_cases

    def _build_test_content(self, code: str, test_cases: List[Dict[str, Any]]) -> str:
        """
        Build the pytest test file content.
        
        Args:
            code: Source code being tested
            test_cases: List of test cases
            
        Returns:
            Complete test file content as string
        """
        lines = [
            "import sys",
            "import os",
            "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))",
            "from solution import *",
            "",
            ""
        ]
        
        for tc in test_cases:
            test_name = tc.get("name", "test_unknown")
            call = tc.get("call", "")
            expected = tc.get("expected", "pass")
            
            if expected == "pass":
                lines.append(f"def {test_name}():")
                lines.append(f"    {call}")
                lines.append(f"    assert True")
            else:
                lines.append(f"def {test_name}():")
                lines.append(f"    result = {call}")
                lines.append(f"    assert result == {repr(expected)}")
            lines.append("")
        
        return "\n".join(lines)

    async def _execute_pytest(self, test_file: Path, cwd: Path) -> subprocess.CompletedProcess:
        """
        Execute pytest asynchronously.
        
        Args:
            test_file: Path to the test file
            cwd: Working directory for execution
            
        Returns:
            CompletedProcess result
        """
        cmd = [
            sys.executable, "-m", "pytest",
            str(test_file),
            "-v",
            "--tb=short",
            "--disable-warnings",
            "-q"
        ]
        
        self.logger.debug("Executing pytest", cmd=" ".join(cmd))
        
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
        )
        
        return result

    def _parse_results(self, result: subprocess.CompletedProcess, attempt: int) -> TestReport:
        """
        Parse pytest output into structured results.
        
        Args:
            result: CompletedProcess from pytest execution
            attempt: Attempt number
            
        Returns:
            TestReport with parsed results
        """
        stdout = result.stdout
        stderr = result.stderr
        exit_code = result.returncode
        
        # Count passed and failed tests
        passed = stdout.count(" PASSED")
        failed = stdout.count(" FAILED")
        errors = stdout.count(" ERROR")
        
        # Extract error messages
        error_messages = []
        if stderr:
            error_messages.append(stderr.strip())
        
        # Extract specific failure messages from stdout
        if failed > 0 or errors > 0:
            for line in stdout.splitlines():
                if "FAILED" in line or "ERROR" in line:
                    error_messages.append(line.strip())
        
        # Determine if all tests passed
        all_passed = exit_code == 0 and failed == 0 and errors == 0
        
        return TestReport(
            passed=all_passed,
            tests_passed=passed,
            tests_failed=failed + errors,
            errors=error_messages[:10],  # Limit to 10 errors
            stdout=stdout,
            stderr=stderr,
            exit_code=exit_code,
            duration_ms=0.0,
            attempt=attempt
        )

    def to_dict(self, report: TestReport) -> Dict[str, Any]:
        """
        Convert TestReport to dictionary for JSON serialization.
        
        Args:
            report: TestReport instance
            
        Returns:
            Dictionary representation
        """
        return {
            "passed": report.passed,
            "attempt": report.attempt,
            "execution_time": round(report.duration_ms / 1000, 3),
            "tests_passed": report.tests_passed,
            "tests_failed": report.tests_failed,
            "stdout": report.stdout,
            "stderr": report.stderr,
            "errors": report.errors,
            "exit_code": report.exit_code
        }
