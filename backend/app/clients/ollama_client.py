import ollama

from app.config import OLLAMA_HOST, OLLAMA_MODEL
from app.clients.llm_client import LLMClient


class OllamaClient(LLMClient):

    def __init__(self):
        self.client = ollama.Client(host=OLLAMA_HOST)
        self.model = OLLAMA_MODEL

        try:
            self.client.list()
            print("Ollama successfully connected")
        except Exception as e:
            raise ConnectionError(
                f"Failed to connect to Ollama at {OLLAMA_HOST}"
            ) from e

    def generate(self, prompt: str) -> str:
        response = self.client.generate(
            model=self.model,
            prompt=prompt
        )

        return response["response"]