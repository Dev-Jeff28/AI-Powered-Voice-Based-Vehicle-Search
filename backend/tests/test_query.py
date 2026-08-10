from app.clients.ollama_client import OllamaClient
from app.models.searchQuery import SearchQuery
from app.repositories.repository import Repository
from app.services.response import ResponseService
from app.services.search import SearchService


search_query = SearchQuery(
    brand="Tata"
)

llm_client = OllamaClient()

repository = Repository()

response_service = ResponseService(llm_client)

search_service = SearchService(
    repository,
    response_service
)

response = search_service.search(search_query)

print("\nFinal Search Response:")
print(response)