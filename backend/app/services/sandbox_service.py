import ast
import os
import subprocess
import tempfile
from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionResult:
    stdout: str
    stderr: str
    return_code: int
    duration_ms: float


class SandboxError(Exception):
    pass


class SandboxService:
    def __init__(self, timeout: int = 30) -> None:
        self._timeout = timeout

    def execute(self, code: str, tests: str | None = None) -> ExecutionResult:
        with tempfile.TemporaryDirectory() as tmpdir:
            solution_path = os.path.join(tmpdir, "solution.py")
            with open(solution_path, "w", encoding="utf-8") as f:
                f.write(code)

            test_path = None
            if tests:
                test_path = os.path.join(tmpdir, "test_solution.py")
                with open(test_path, "w", encoding="utf-8") as f:
                    f.write(tests)

            cmd = ["python", "-m", "pytest", solution_path, "-v", "--tb=short", "--disable-warnings"]
            if test_path:
                cmd = ["python", "-m", "pytest", test_path, "-v", "--tb=short", "--disable-warnings"]

            import time
            start = time.perf_counter()
            try:
                proc = subprocess.run(
                    cmd,
                    cwd=tmpdir,
                    capture_output=True,
                    text=True,
                    timeout=self._timeout,
                )
                duration_ms = (time.perf_counter() - start) * 1000
                return ExecutionResult(
                    stdout=proc.stdout,
                    stderr=proc.stderr,
                    return_code=proc.returncode,
                    duration_ms=duration_ms,
                )
            except subprocess.TimeoutExpired as exc:
                duration_ms = (time.perf_counter() - start) * 1000
                return ExecutionResult(
                    stdout=exc.stdout or "",
                    stderr=exc.stderr or "Execution timed out",
                    return_code=-1,
                    duration_ms=duration_ms,
                )
            except Exception as exc:
                raise SandboxError(f"Sandbox execution failed: {exc}") from exc

    def validate_syntax(self, code: str, language: str = "python") -> None:
        if language != "python":
            return
        try:
            ast.parse(code)
        except SyntaxError as exc:
            raise SandboxError(f"Syntax error: {exc.msg} at line {exc.lineno}") from exc
