import re
import time
from typing import Literal

from app.agent.models import (
    AgentConfig,
    AgentOutput,
    ErrorCategory,
    ErrorReport,
    ReasoningStep,
    RepairAction,
)
from app.core.config import settings
from app.services.openai_service import OpenAIService
from app.services.sandbox_service import SandboxService, SandboxError


class AutonomousAgent:
    def __init__(
        self,
        openai_service: OpenAIService,
        sandbox_service: SandboxService,
        config: AgentConfig | None = None,
    ) -> None:
        self._openai = openai_service
        self._sandbox = sandbox_service
        self._config = config or AgentConfig(
            max_retries=settings.max_retries,
            sandbox_timeout=settings.sandbox_timeout,
            model=settings.openai_model,
        )

    async def run(self, prompt: str, tests: str | None = None) -> AgentOutput:
        reasoning: list[ReasoningStep] = []
        errors: list[ErrorReport] = []
        code = ""
        repair: RepairAction | None = None

        reasoning.append(
            ReasoningStep(
                thought=f"Received prompt: {prompt[:100]}...",
                observation="Starting autonomous workflow",
                confidence=1.0,
                next_action="retry",
            )
        )

        for attempt in range(1, self._config.max_retries + 1):
            reasoning.append(
                ReasoningStep(
                    thought=f"Attempt {attempt}/{self._config.max_retries}: Generating code",
                    observation=f"Attempt {attempt} started",
                    confidence=0.9,
                    next_action="retry",
                )
            )

            if attempt == 1:
                code = await self._openai.generate_code(prompt)
            else:
                reasoning.append(
                    ReasoningStep(
                        thought=f"Attempt {attempt}: Repairing code based on previous errors",
                        observation=f"Errors from previous attempt: {len(errors)}",
                        confidence=0.7,
                        next_action="repair",
                    )
                )
                repair_result = await self._openai.repair_code(
                    code=code,
                    errors=[e.message for e in errors],
                    prompt=prompt,
                )
                code = repair_result[0]
                repair = RepairAction(
                    reason=repair_result[1],
                    code_change=repair_result[0],
                    confidence=0.8,
                    expected_outcome="Fixed errors and passed tests",
                )

            try:
                self._sandbox.validate_syntax(code)
            except SandboxError as exc:
                errors.append(
                    ErrorReport(
                        category=ErrorCategory.COMPILER,
                        message=str(exc),
                    )
                )
                reasoning.append(
                    ReasoningStep(
                        thought="Syntax error detected during compilation",
                        observation=str(exc),
                        confidence=0.5,
                        next_action="repair",
                    )
                )
                continue

            start = time.perf_counter()
            result = self._sandbox.execute(code, tests)
            duration_ms = (time.perf_counter() - start) * 1000

            if result.stderr and "SyntaxError" in result.stderr:
                for line in result.stderr.splitlines():
                    if "SyntaxError" in line:
                        errors.append(
                            ErrorReport(
                                category=ErrorCategory.COMPILER,
                                message=line.strip(),
                            )
                        )
                        break

            if result.return_code != 0:
                runtime_errors = self._extract_runtime_errors(result.stderr)
                errors.extend(runtime_errors)

            test_results = self._parse_pytest_output(result.stdout, result.stderr)
            failed_tests = [t for t in test_results if not t["passed"]]
            for test in failed_tests:
                errors.append(
                    ErrorReport(
                        category=ErrorCategory.TEST,
                        message=test["error"] or "Test failed",
                        test_name=test["name"],
                    )
                )

            if not errors:
                return AgentOutput(
                    explanation=f"Success on attempt {attempt}. All tests passed.",
                    code=code,
                    reason_for_modification="No modifications needed",
                    confidence=1.0,
                    next_action="succeed",
                    reasoning=reasoning,
                    errors=[],
                    repair=repair,
                    attempts=attempt,
                    max_attempts=self._config.max_retries,
                    status="success",
                )

            reasoning.append(
                ReasoningStep(
                    thought=f"Attempt {attempt} failed. Analyzing {len(errors)} errors.",
                    observation=f"Errors: {[e.message for e in errors]}",
                    confidence=0.3,
                    next_action="repair",
                )
            )

        return AgentOutput(
            explanation=f"Failed after {self._config.max_retries} attempts. Manual intervention required.",
            code=code,
            reason_for_modification=repair.reason if repair else "Multiple repair attempts failed",
            confidence=0.0,
            next_action="abort",
            reasoning=reasoning,
            errors=errors,
            repair=repair,
            attempts=self._config.max_retries,
            max_attempts=self._config.max_retries,
            status="error",
        )

    def _extract_runtime_errors(self, stderr: str) -> list[ErrorReport]:
        errors = []
        pattern = re.compile(r"^Traceback.*?^(?:\w+Error|Exception): (.+)$", re.MULTILINE | re.DOTALL)
        for match in pattern.finditer(stderr):
            message = match.group(1).strip()
            line_match = re.search(r"line (\d+)", stderr[: match.start() + 200])
            errors.append(
                ErrorReport(
                    category=ErrorCategory.RUNTIME,
                    message=message,
                    line=int(line_match.group(1)) if line_match else None,
                    stack_trace=stderr[:500],
                )
            )
        return errors

    def _parse_pytest_output(self, stdout: str, stderr: str) -> list[dict]:
        results = []
        pattern = re.compile(r"^(PASSED|FAILED|ERROR)\s+(test_.+)$", re.MULTILINE)
        for match in pattern.finditer(stdout):
            status, name = match.groups()
            results.append(
                {
                    "name": name,
                    "passed": status == "PASSED",
                    "error": None if status == "PASSED" else f"{status}: {name}",
                }
            )
        return results
