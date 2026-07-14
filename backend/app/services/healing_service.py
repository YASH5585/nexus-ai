import re

from app.agent.engine import AutonomousAgent
from app.agent.models import AgentConfig, AgentOutput
from app.core.exceptions import MaxRetriesExceededError
from app.models.entities import ExecutionContext, ExecutionStep, StepStatus
from app.services.openai_service import OpenAIService
from app.services.sandbox_service import SandboxService, SandboxError


class HealingService:
    def __init__(
        self,
        openai_service: OpenAIService,
        sandbox_service: SandboxService,
        max_retries: int = 5,
    ) -> None:
        self._openai = openai_service
        self._sandbox = sandbox_service
        self._max_retries = max_retries
        self._agent = AutonomousAgent(
            openai_service=openai_service,
            sandbox_service=sandbox_service,
            config=AgentConfig(max_retries=max_retries),
        )

    async def run(self, context: ExecutionContext) -> ExecutionContext:
        context.status = "running"
        context.add_step(ExecutionStep(id="analyze", label="Analyze Prompt"))
        context.add_step(ExecutionStep(id="generate", label="Generate Code"))
        context.add_step(ExecutionStep(id="execute", label="Execute Code"))
        context.add_step(ExecutionStep(id="heal", label="Heal Failures"))

        self._set_step_status(context, "analyze", StepStatus.running, "Launching autonomous agent")
        output = await self._agent.run(prompt=context.prompt)
        self._set_step_status(context, "analyze", StepStatus.completed)

        context.code = output.code
        context.attempts = output.attempts
        context.errors = [e.message for e in output.errors]
        context.status = output.status

        if output.status == "success":
            self._set_step_status(context, "generate", StepStatus.completed, "Code generated successfully")
            self._set_step_status(context, "execute", StepStatus.completed, "All tests passed")
            context.patched_code = output.code
        else:
            self._set_step_status(context, "execute", StepStatus.error, f"Failed after {output.attempts} attempts")
            raise MaxRetriesExceededError(output.explanation)

        return context

    def _set_step_status(
        self,
        context: ExecutionContext,
        step_id: str,
        status: StepStatus,
        detail: str | None = None,
    ) -> None:
        for step in context.steps:
            if step.id == step_id:
                step.status = status
                if detail:
                    step.detail = detail
                break

    @staticmethod
    def _parse_pytest_output(stdout: str, stderr: str) -> list[dict]:
        results: list[dict] = []
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

    @staticmethod
    async def _sleep(ms: int) -> None:
        import asyncio
        await asyncio.sleep(ms / 1000)
