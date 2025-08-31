from __future__ import annotations

import os
from typing import List, Dict, Any

from openai import OpenAI


class OpenAIChatLLM:
    """OpenAI Chat wrapper."""

    def __init__(self, model: str | None = None):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY env var not set.")
        self.client = OpenAI(api_key=api_key)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def generate(self, prompt_text: str) -> str:
        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": "You are an intent classification model. Return plain text with required fields.",
                },
                {"role": "user", "content": prompt_text},
            ],
        )
        return completion.choices[0].message.content or ""

    def chat(self, messages: List[Dict[str, Any]]) -> str:
        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=0.4,
            messages=messages,
        )
        return completion.choices[0].message.content or ""
