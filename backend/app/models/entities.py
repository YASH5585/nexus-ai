import asyncio
import subprocess
import tempfile
import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Literal


class StepStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    error = "error"


@dataclass
class ExecutionStep:
    id: str
    label: str
    status: StepStatus = StepStatus.pending
    detail: str | None = None


@dataclass
class ExecutionContext:
    run_id: str
    prompt: str
    code: str = ""
    patched_code: str = ""
    errors: list[str] = field(default_factory=list)
    test_results: list[dict] = field(default_factory=list)
    attempts: int = 0
    max_retries: int = 5
    status: Literal["idle", "running", "success", "error"] = "idle"
    steps: list[ExecutionStep] = field(default_factory=list)

    def add_step(self, step: ExecutionStep) -> None:
        self.steps.append(step)

    def current_step(self) -> ExecutionStep | None:
        for step in self.steps:
            if step.status == StepStatus.running:
                return step
        return None
