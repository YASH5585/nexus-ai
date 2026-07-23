from __future__ import annotations

import os
from typing import List, Optional, Tuple

import httpx

from app.core.config import Settings, get_settings


class HuggingFaceService:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        timeout: float = 60.0,
    ) -> None:
        self._api_key = api_key or os.getenv("HUGGINGFACE_API_KEY") or os.getenv("HF_API_KEY") or ""
        self._model = model or os.getenv("HUGGINGFACE_MODEL", "google/flan-t5-large")
        self._timeout = timeout
        self._base_url = "https://api-inference.huggingface.co/models"

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"
        return headers

    async def _post(self, payload: dict) -> dict:
        url = f"{self._base_url}/{self._model}"
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.post(url, json=payload, headers=self._headers())
        response.raise_for_status()
        return response.json()

    async def generate_code(self, prompt: str, language: str = "python") -> str:
        system_prompt = (
            "You are an expert software engineer. "
            "Return ONLY valid, production-ready code. "
            "No explanations, no markdown fences."
        )
        user_prompt = f"Language: {language}\n\nProblem:\n{prompt}\n\nSolution:"

        payload = {
            "inputs": f"{system_prompt}\n\n{user_prompt}",
            "parameters": {
                "max_new_tokens": 1024,
                "temperature": 0.2,
                "return_full_text": False,
            },
        }

        data = await self._post(payload)
        if isinstance(data, list) and data:
            return data[0].get("generated_text", "") or ""
        if isinstance(data, dict):
            return data.get("generated_text", "") or ""
        return ""

    async def repair_code(
        self,
        code: str,
        errors: List[str],
        prompt: str,
        language: str = "python",
    ) -> Tuple[str, str]:
        error_report = "\n".join(f"- {e}" for e in errors)
        user_prompt = (
            f"Language: {language}\n"
            f"Original prompt: {prompt}\n\n"
            f"Current code:\n{code}\n\n"
            f"Errors to fix:\n{error_report}\n\n"
            "Please provide the repaired code and a brief explanation. "
            "Format: EXPLANATION: explanation\nCODE:```python\ncode```"
        )
        payload = {
            "inputs": user_prompt,
            "parameters": {
                "max_new_tokens": 1024,
                "temperature": 0.2,
                "return_full_text": False,
            },
        }

        text = ""
        data = await self._post(payload)
        if isinstance(data, list) and data:
            text = data[0].get("generated_text", "") or ""
        elif isinstance(data, dict):
            text = data.get("generated_text", "") or ""

        explanation = ""
        patched_code = code
        if "EXPLANATION:" in text and "CODE:" in text:
            parts = text.split("CODE:", 1)
            explanation = parts[0].replace("EXPLANATION:", "").strip()
            patched_code = parts[1].strip()
        return patched_code, explanation

    async def generate_tests(self, code: str, language: str = "python") -> str:
        user_prompt = (
            f"Language: {language}\n\nCode to test:\n{code}\n\n"
            "Generate comprehensive pytest unit tests for the given code. "
            "Return ONLY valid Python pytest code. No explanations, no markdown fences."
        )
        payload = {
            "inputs": user_prompt,
            "parameters": {
                "max_new_tokens": 1024,
                "temperature": 0.2,
                "return_full_text": False,
            },
        }

        data = await self._post(payload)
        if isinstance(data, list) and data:
            return data[0].get("generated_text", "") or ""
        if isinstance(data, dict):
            return data.get("generated_text", "") or ""
        return ""
