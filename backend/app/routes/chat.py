from fastapi import APIRouter

from app.services.conversation import ConversationService
from app.services.understanding import UnderstandingService
from app.memory.memory import Memory
from app.session.session import create_session_id


router = APIRouter()


def create_chat_router(
    memory: Memory,
    understanding_service: UnderstandingService,
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

        conversation_response = conversation_service.handle(
            query,
            session_id
        )

        if conversation_response is not None:

            return {
                "session_id": session_id,
                "assistant_response":
                    conversation_response.assistant_response
            }

        response = understanding_service.understand(
            query,
            session_id
        )

        return {
            "session_id": session_id,
            "assistant_response":
                response.assistant_response
        }

    return router