from pydantic import BaseModel, Field

from app.models.searchQuery import SearchQuery


class ConversationMemory(BaseModel):
    conversation_id: str
    search_query: SearchQuery | None = None
    vehicle_ids: list[int] = Field(default_factory=list)