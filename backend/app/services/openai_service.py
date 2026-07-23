from openai import OpenAI

from app.core.config import settings


class OpenAIService:
    def __init__(self, api_key: str, model: str) -> None:
        self._client = OpenAI(api_key=api_key)
        self._model = model

    async def generate_code(self, prompt: str, language: str = "python") -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert software engineer. "
                        "Return ONLY valid, production-ready code. "
                        "No explanations, no markdown fences."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Language: {language}\n\nProblem:\n{prompt}\n\nSolution:",
                },
            ],
            max_tokens=2048,
        )
        return response.choices[0].message.content or ""
