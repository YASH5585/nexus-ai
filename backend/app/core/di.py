from app.services.openai_service import OpenAIService
from app.services.huggingface_service import HuggingFaceService
from app.services.sandbox_service import SandboxService
from app.services.healing_service import HealingService
from app.core.config import Settings, settings


class Container:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._openai_service: OpenAIService | None = None
        self._huggingface_service: HuggingFaceService | None = None
        self._sandbox_service: SandboxService | None = None
        self._healing_service: HealingService | None = None

    def openai(self) -> OpenAIService:
        if self._openai_service is None:
            self._openai_service = OpenAIService(
                api_key=self._settings.openai_api_key,
                model=self._settings.openai_model,
            )
        return self._openai_service

    def huggingface(self) -> HuggingFaceService:
        if self._huggingface_service is None:
            self._huggingface_service = HuggingFaceService(
                api_key=self._settings.huggingface_api_key,
                model=self._settings.huggingface_model,
            )
        return self._huggingface_service

    def sandbox(self) -> SandboxService:
        if self._sandbox_service is None:
            self._sandbox_service = SandboxService(timeout=self._settings.sandbox_timeout)
        return self._sandbox_service

    def healing(self) -> HealingService:
        if self._healing_service is None:
            provider = (self._settings.llm_provider or "openai").lower()
            if provider == "huggingface":
                llm_service = self.huggingface()
            else:
                llm_service = self.openai()
            self._healing_service = HealingService(
                openai_service=llm_service,
                sandbox_service=self.sandbox(),
                max_retries=self._settings.max_retries,
            )
        return self._healing_service


container = Container(settings=settings)


def get_container() -> Container:
    return container
