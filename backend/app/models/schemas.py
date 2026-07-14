from typing import Literal

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=10000, description="Coding problem description")


class GeneratedCodeResponse(BaseModel):
    code: str
    language: str = "python"
    explanation: str | None = None


class ExecuteRequest(BaseModel):
    code: str = Field(..., min_length=1)
    tests: str | None = Field(default=None, description="Optional pytest test code")
    language: str = Field(default="python")


class TestResult(BaseModel):
    name: str
    passed: bool
    error: str | None = None
    duration_ms: float


class ExecuteResponse(BaseModel):
    stdout: str
    stderr: str
    return_code: int
    tests: list[TestResult] = []
    duration_ms: float


class RepairRequest(BaseModel):
    code: str
    errors: list[str] = Field(..., min_length=1)
    prompt: str
    language: str = "python"


class RepairResponse(BaseModel):
    patched_code: str
    explanation: str
    confidence: float = Field(ge=0.0, le=1.0)


class RunStatusResponse(BaseModel):
    status: Literal["idle", "running", "success", "error"]
    current_step: str | None = None
    attempts: int = 0
    max_retries: int = 5
    message: str | None = None


class ErrorResponse(BaseModel):
    code: str
    message: str
