from langchain_core.chat_history import InMemoryChatMessageHistory

from app.models.conversationMemory import ConversationMemory


class Memory:

    def __init__(self):
        self._memory: dict[str, ConversationMemory] = {}
        self._message_history: dict[
            str,
            InMemoryChatMessageHistory
        ] = {}

    def create(
        self,
        session_id: str
    ) -> ConversationMemory:

        conversation_memory = ConversationMemory(
            conversation_id=session_id
        )

        self._memory[session_id] = conversation_memory

        self._message_history[session_id] = (
            InMemoryChatMessageHistory()
        )

        return conversation_memory

    def get(
        self,
        session_id: str
    ) -> ConversationMemory | None:

        return self._memory.get(session_id)

    def update(
        self,
        session_id: str,
        memory: ConversationMemory
    ) -> None:

        self._memory[session_id] = memory

    def get_message_history(
        self,
        session_id: str
    ) -> InMemoryChatMessageHistory:

        if session_id not in self._message_history:
            self._message_history[session_id] = (
                InMemoryChatMessageHistory()
            )

        return self._message_history[session_id]