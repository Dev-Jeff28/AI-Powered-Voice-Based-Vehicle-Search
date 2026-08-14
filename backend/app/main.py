from fastapi import FastAPI

from app.memory.memory import Memory
from app.repositories.repository import Repository
from app.routes.chat import create_chat_router
from app.services.conversation import ConversationService
from app.services.response import ResponseService
from app.services.search import SearchService
from app.services.understanding import UnderstandingService


app = FastAPI()


memory = Memory()

repository = Repository()

response_service = ResponseService()

understanding_service = UnderstandingService(
    memory
)

search_service = SearchService(
    vehicle_repository=repository,
    response_service=response_service,
    memory=memory
)

conversation_service = ConversationService(
    memory=memory,
    repository=repository,
    response_service=response_service,
    understanding_service=understanding_service,
    search_service=search_service
)


app.include_router(
    create_chat_router(
        memory=memory,
        conversation_service=conversation_service
    )
)