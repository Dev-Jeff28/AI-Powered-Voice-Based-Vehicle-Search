from fastapi import FastAPI

from app.clients.openrouter_client import OpenRouterClient
#from app.clients.gemini_client import GeminiClient
from app.repositories.repository import Repository
from app.services.response import ResponseService
from app.services.search import SearchService
from app.services.understanding import UnderstandingService
from app.services.conversation import ConversationService
from app.memory.memory import Memory
from app.session.session import create_session_id

from app.routes.chat import create_chat_router


app = FastAPI()


llm_client = OpenRouterClient()

repository = Repository()

memory = Memory()

response_service = ResponseService(
    llm_client
)

search_service = SearchService(
    repository,
    response_service,
    memory
)

understanding_service = UnderstandingService(
    llm_client,
    search_service
)

conversation_service = ConversationService(
    memory,
    repository,
    response_service,
    understanding_service
)


app.include_router(
    create_chat_router(
        memory,
        understanding_service,
        conversation_service
    )
)