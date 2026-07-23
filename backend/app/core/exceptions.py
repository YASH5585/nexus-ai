from fastapi import HTTPException, status


class NexusAIException(Exception):
    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class OpenAIError(NexusAIException):
    def __init__(self, message: str):
        super().__init__(message, code="OPENAI_ERROR")


class SandboxError(NexusAIException):
    def __init__(self, message: str):
        super().__init__(message, code="SANDBOX_ERROR")


class TestFailureError(NexusAIException):
    def __init__(self, message: str):
        super().__init__(message, code="TEST_FAILURE")


class MaxRetriesExceededError(NexusAIException):
    def __init__(self, message: str):
        super().__init__(message, code="MAX_RETRIES_EXCEEDED")


def handle_nexus_exception(exc: NexusAIException) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"code": exc.code, "message": exc.message},
    )
