from app.models.conversationMemory import ConversationMemory


class Memory:

    def __init__(self):
        self._memory: dict[str, ConversationMemory] = {}

    def create(self, session_id: str) -> ConversationMemory:

        conversation_memory = ConversationMemory(
            conversation_id=session_id
        )

        self._memory[session_id] = conversation_memory

        return conversation_memory

    def get(self, session_id: str) -> ConversationMemory | None:

        return self._memory.get(session_id)

    def update(
        self,
        session_id: str,
        memory: ConversationMemory
    ) -> None:

        self._memory[session_id] = memory