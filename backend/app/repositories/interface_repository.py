from abc import ABC, abstractmethod

from app.models.searchQuery import SearchQuery
from app.models.vehicle import Vehicle


class interfaceRepository(ABC):

    @abstractmethod
    def search(
    self,
    search_query: SearchQuery,
    body_types: list[str] | None = None
    ) -> list[Vehicle]: 
        pass


    @abstractmethod
    def get_by_id(self,vehicle_id: int) -> Vehicle | None:
        pass