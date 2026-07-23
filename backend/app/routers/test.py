from fastapi import APIRouter, HTTPException, status
from app.services.tester import TestingEngine
from app.schemas.test import TestRequest, TestResponse
from app.core.config import settings

router = APIRouter(prefix="/test", tags=["test"])


@router.post("", response_model=TestResponse)
async def run_test(request: TestRequest):
    """
    Test the provided Python code against predefined unit tests.

    Args:
        request: The test request containing the code and optional test cases.

    Returns:
        A structured JSON response with the test results.
    """
    if request.language.lower() != "python":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only 'python' language is currently supported",
        )

    try:
        engine = TestingEngine(timeout=settings.sandbox_timeout)
        report = await engine.run_tests(
            code=request.code,
            test_cases=request.test_cases,
            attempt=request.attempt,
        )
        return TestResponse(
            passed=report.passed,
            attempt=report.attempt,
            execution_time=round(report.duration_ms / 1000, 3),
            tests_passed=report.tests_passed,
            tests_failed=report.tests_failed,
            stdout=report.stdout,
            stderr=report.stderr,
            errors=report.errors,
            exit_code=report.exit_code,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while running the test: {str(e)}",
        )