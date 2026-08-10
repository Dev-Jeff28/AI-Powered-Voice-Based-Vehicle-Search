from pydantic import BaseModel, ConfigDict

from app.models.searchQuery import SearchQuery
from app.models.vehicle import Vehicle


class SearchResponse(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

    vehicles: list[Vehicle]
    search_query: SearchQuery
    assistant_response: str