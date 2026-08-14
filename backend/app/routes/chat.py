from fastapi import APIRouter

from app.memory.memory import Memory
from app.services.conversation import ConversationService
from app.session.session import create_session_id


def create_chat_router(
    memory: Memory,
    conversation_service: ConversationService
):
    router = APIRouter()

    @router.put("/app/chat")
    def chat(
        query: str,
        session_id: str | None = None
    ):

        if session_id is None:

            session_id = create_session_id()

            memory.create(
                session_id
            )

        elif memory.get(session_id) is None:

            memory.create(
                session_id
            )

        conversation_response = (
            conversation_service.handle(
                query,
                session_id
            )
        )

        if conversation_response is None:

            return {
                "session_id": session_id,
                "assistant_response": None
            }

        return {
            "session_id": session_id,
            "assistant_response":
                conversation_response.assistant_response
        }

    return router