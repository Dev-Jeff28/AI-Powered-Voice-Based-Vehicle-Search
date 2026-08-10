from openai import OpenAI
from dotenv import load_dotenv
import os

from app.clients.llm_client import LLMClient

load_dotenv()


class GeminiClient(LLMClient):

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")
        model = os.getenv("GEMINI_MODEL")
        print("GEMINI KEY EXISTS:", bool(api_key))
        print("GEMINI KEY PREFIX:", api_key[:8] if api_key else None)
        print("GEMINI MODEL:", model)

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured"
            )

        if not model:
            raise ValueError(
                "GEMINI_MODEL is not configured"
            )

        try:

            self._client = OpenAI(
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
                api_key=api_key
            )

            self._model = model

            print("Gemini successfully connected")

        except Exception as e:

            raise ConnectionError(
                f"Failed to connect to Gemini: {e}"
            )

    def generate(
        self,
        prompt: str
    ) -> str:

        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        if not response.choices:
            raise RuntimeError(
                f"Gemini returned no choices: {response}"
            )

        message = response.choices[0].message

        if message is None:
            raise RuntimeError(
                f"Gemini returned no message: {response}"
            )

        if message.content is None:
            raise RuntimeError(
                f"Gemini returned no content: {response}"
            )

        return message.content