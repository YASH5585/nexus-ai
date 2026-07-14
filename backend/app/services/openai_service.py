from openai import OpenAI

from app.core.config import settings


class OpenAIService:
    def __init__(self, api_key: str, model: str) -> None:
        self._client = OpenAI(api_key=api_key)
        self._model = model

    async def generate_code(self, prompt: str, language: str = "python") -> str:
        response = self._client.responses.create(
            model=self._model,
            input=[
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
            max_output_tokens=2048,
        )
        return response.output_text

    async def repair_code(
        self,
        code: str,
        errors: list[str],
        prompt: str,
        language: str = "python",
    ) -> tuple[str, str]:
        error_report = "\n".join(f"- {e}" for e in errors)
        response = self._client.responses.create(
            model=self._model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert debugger. "
                        "Return ONLY the fixed code and a brief explanation of what changed. "
                        "Format: EXPLANATION: ... followed by CODE: ... followed by the code."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Language: {language}\n"
                        f"Original prompt: {prompt}\n\n"
                        f"Current code:\n{code}\n\n"
                        f"Errors to fix:\n{error_report}\n\n"
                        "Please provide the repaired code and explanation."
                    ),
                },
            ],
            max_output_tokens=2048,
        )
        text = response.output_text
        explanation = ""
        patched_code = code
        if "EXPLANATION:" in text and "CODE:" in text:
            parts = text.split("CODE:", 1)
            explanation = parts[0].replace("EXPLANATION:", "").strip()
            patched_code = parts[1].strip()
        return patched_code, explanation

    async def generate_tests(self, code: str, language: str = "python") -> str:
        response = self._client.responses.create(
            model=self._model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are a QA engineer. Generate comprehensive pytest unit tests for the given code. "
                        "Return ONLY valid Python pytest code. No explanations, no markdown fences."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Language: {language}\n\nCode to test:\n{code}\n\npytest tests:",
                },
            ],
            max_output_tokens=2048,
        )
        return response.output_text
