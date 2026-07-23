from typing import Literal, List, Optional

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
    tests: List[TestResult] = []
    duration_ms: float


class RepairRequest(BaseModel):
    code: str
    errors: List[str] = Field(..., min_length=1)
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


# New models for the testing endpoint
class TestRequest(BaseModel):
    language: str = Field(..., description="The programming language of the code (currently only 'python' is supported)")
    code: str = Field(..., min_length=1, description="The Python code to be tested")


class TestResponse(BaseModel):
    passed: bool
    attempt: int = 1  # For compatibility with the self-healing loop; in this service, it's always 1
    execution_time: float  # In seconds
    tests_passed: int
    tests_failed: int
    stdout: str
    stderr: str
    errors: List[str] = Field(default_factory=list, description="List of error messages from failed tests")