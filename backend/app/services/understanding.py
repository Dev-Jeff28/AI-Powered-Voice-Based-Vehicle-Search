from pathlib import Path

from app.clients.llm_client import LLMClient
from app.models.searchQuery import SearchQuery
from app.models.searchResponse import SearchResponse
from app.services.search import SearchService


class UnderstandingService:

    def __init__(
        self,
        llm_client: LLMClient,
        search_service: SearchService
    ):
        self._llm_client = llm_client
        self._search_service = search_service

    def understand_query(
        self,
        query: str
    ) -> SearchQuery:

        prompt_path = (
            Path(__file__).parent.parent
            / "prompts"
            / "understanding_prompt.txt"
        )

        prompt = prompt_path.read_text(
            encoding="utf-8"
        )

        prompt = prompt.replace(
            "{query}",
            query
        )

        response = self._llm_client.generate(
            prompt
        )

        response = response.strip()

        # Remove markdown code fences if the LLM adds them
        if response.startswith("```json"):
            response = response[7:]

        elif response.startswith("```"):
            response = response[3:]

        if response.endswith("```"):
            response = response[:-3]

        response = response.strip()

        search_query = SearchQuery.model_validate_json(
            response
        )

        return search_query

    def search(
        self,
        search_query: SearchQuery,
        session_id: str
    ) -> SearchResponse:

        return self._search_service.search(
            search_query,
            session_id
        )

    def understand(
        self,
        query: str,
        session_id: str
    ) -> SearchResponse:

        search_query = self.understand_query(
            query
        )

        print("Object Created")
        print(search_query)

        return self.search(
            search_query,
            session_id
        )