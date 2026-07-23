from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class ErrorCategory(str, Enum):
    COMPILER = "compiler"
    RUNTIME = "runtime"
    TEST = "test"
    UNKNOWN = "unknown"


class ReasoningStep(BaseModel):
    thought: str = Field(description="Structured reasoning about the current state")
    observation: str = Field(description="What was observed from execution")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in the current approach")
    next_action: Literal["retry", "repair", "abort", "succeed"] = Field(description="Recommended next action")


class ErrorReport(BaseModel):
    category: ErrorCategory
    message: str
    file: str | None = None
    line: int | None = None
    stack_trace: str | None = None
    test_name: str | None = None


class RepairAction(BaseModel):
    reason: str = Field(description="Why this modification is needed")
    code_change: str = Field(description="The actual code modification")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence this fix will work")
    expected_outcome: str = Field(description="What should happen after applying this fix")


class AgentOutput(BaseModel):
    explanation: str = Field(description="Human-readable explanation of what happened")
    code: str = Field(description="The final or current code state")
    reason_for_modification: str = Field(description="Why the code was modified")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in the solution")
    next_action: Literal["retry", "repair", "abort", "succeed"] = Field(description="Recommended next action")
    reasoning: list[ReasoningStep] = Field(default_factory=list, description="Structured reasoning trace")
    errors: list[ErrorReport] = Field(default_factory=list, description="Collected errors")
    repair: RepairAction | None = Field(default=None, description="Last repair action taken")
    attempts: int = Field(ge=0, description="Number of attempts made")
    max_attempts: int = Field(ge=1, description="Maximum attempts allowed")
    status: Literal["running", "success", "error"] = Field(description="Current agent status")


class AgentConfig(BaseModel):
    max_retries: int = Field(default=5, ge=1, le=20)
    sandbox_timeout: int = Field(default=30, ge=5, le=300)
    model: str = Field(default="gpt-4o")
    temperature: float = Field(default=0.2, ge=0.0, le=1.0)
    enable_reasoning: bool = Field(default=True)
