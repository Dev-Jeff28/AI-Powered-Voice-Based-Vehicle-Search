from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.llm import get_llm
from app.memory.memory import Memory
from app.models.searchQuery import SearchQuery


class UnderstandingService:

    def __init__(self, memory: Memory):
        self._memory = memory

        self.llm = get_llm()

        self.structured_llm = self.llm.with_structured_output(
            SearchQuery,
            method="json_schema"
        )

        prompt_path = (
            Path(__file__).parent.parent
            / "prompts"
            / "understanding_prompt.txt"
        )

        prompt = prompt_path.read_text(
            encoding="utf-8"
        )

        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                prompt
            ),
            MessagesPlaceholder(
                variable_name="history"
            ),
            (
                "human",
                "{query}"
            )
        ])

        self.chain = (
            self.prompt
            | self.structured_llm
        )

    def understand(
        self,
        query: str,
        session_id: str
    ) -> SearchQuery:

        history = self._memory.get_message_history(
            session_id
        )

        response = self.chain.invoke({
            "history": history.messages,
            "query": query
        })

        print(
            "Understanding Response:",
            response
        )

        return response