from fastapi import APIRouter, Depends, HTTPException, status

from app.agent.engine import AutonomousAgent
from app.agent.models import AgentConfig, AgentOutput
from app.core.config import settings
from app.core.di import get_container
from app.models.schemas import GenerateRequest
from app.services.huggingface_service import HuggingFaceService
from app.services.openai_service import OpenAIService

router = APIRouter(prefix="/agent", tags=["agent"])


def _get_llm_service():
    provider = (settings.llm_provider or "openai").lower()
    if provider == "huggingface":
        return HuggingFaceService(
            api_key=settings.huggingface_api_key,
            model=settings.huggingface_model,
        )
    return OpenAIService(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )


@router.post("/run", response_model=AgentOutput)
async def run_agent(
    payload: GenerateRequest,
    container=Depends(get_container),
) -> AgentOutput:
    try:
        llm_service = _get_llm_service()
        agent = AutonomousAgent(
            openai_service=llm_service,
            sandbox_service=container.sandbox(),
        )
        result = await agent.run(prompt=payload.prompt)
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": "AGENT_ERROR", "message": str(exc)},
        ) from exc


@router.post("/run-with-tests", response_model=AgentOutput)
async def run_agent_with_tests(
    payload: GenerateRequest,
    container=Depends(get_container),
) -> AgentOutput:
    try:
        agent = AutonomousAgent(
            openai_service=container.openai(),
            sandbox_service=container.sandbox(),
        )
        tests = await container.openai().generate_tests("")
        result = await agent.run(prompt=payload.prompt, tests=tests)
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": "AGENT_ERROR", "message": str(exc)},
        ) from exc
