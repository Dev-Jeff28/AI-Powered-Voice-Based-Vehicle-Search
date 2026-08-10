from openai import OpenAI
from dotenv import load_dotenv
import os

from app.clients.llm_client import LLMClient


load_dotenv()


class OpenRouterClient(LLMClient):

    def __init__(self):

        api_key = os.getenv("OPENROUTER_API_KEY")
        model = os.getenv("OPENROUTER_MODEL")

        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY is not configured"
            )

        if not model:
            raise ValueError(
                "OPENROUTER_MODEL is not configured"
            )

        try:

            self._client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key
            )

            self._model = model

            print("OpenRouter successfully connected")

        except Exception as e:

            raise ConnectionError(
                f"Failed to connect to OpenRouter: {e}"
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
                f"OpenRouter returned no choices: {response}"
            )

        message = response.choices[0].message

        if message is None:
            raise RuntimeError(
                f"OpenRouter returned no message: {response}"
            )

        if message.content is None:
            raise RuntimeError(
                f"OpenRouter returned no content: {response}"
            )

        return message.content