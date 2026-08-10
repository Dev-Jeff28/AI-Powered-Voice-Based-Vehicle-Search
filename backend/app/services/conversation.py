from app.memory.memory import Memory
from app.models.searchQuery import SearchQuery
from app.models.searchResponse import SearchResponse
from app.repositories.interface_repository import interfaceRepository
from app.services.response import ResponseService
from app.services.understanding import UnderstandingService


class ConversationService:

    def __init__(
        self,
        memory: Memory,
        repository: interfaceRepository,
        response_service: ResponseService,
        understanding_service: UnderstandingService
    ):
        self._memory = memory
        self._repository = repository
        self._response_service = response_service
        self._understanding_service = understanding_service

    def handle(
        self,
        query: str,
        session_id: str
    ) -> SearchResponse | None:

        memory = self._memory.get(session_id)

        if memory is None:
            return None

        # Check for first, second or third vehicle
        vehicle_position = self._find_vehicle_position(
            query
        )

        if vehicle_position is not None:

            if vehicle_position >= len(
                memory.vehicle_ids
            ):
                return None

            vehicle_id = memory.vehicle_ids[
                vehicle_position
            ]

            vehicle = self._repository.get_by_id(
                vehicle_id
            )

            if vehicle is None:
                return None

            return self._response_service.respond_about_vehicle(
                vehicle
            )

        # Otherwise treat this as a new/refined search
        new_search_query = (
            self._understanding_service.understand_query(
                query
            )
        )
        print("New SearchQuery:")
        print(new_search_query)

        merged_search_query = self._merge_search_query(
            memory.search_query,
            new_search_query
        )
        print("Merged SearchQuery:")
        print(merged_search_query)
        return self._understanding_service.search(
            merged_search_query,
            session_id
        )

    def _merge_search_query(
        self,
        old_query: SearchQuery | None,
        new_query: SearchQuery
    ) -> SearchQuery:

        if old_query is None:
            return new_query

        return SearchQuery(
            brand=(
                new_query.brand
                if new_query.brand is not None
                else old_query.brand
            ),
            model=(
                new_query.model
                if new_query.model is not None
                else old_query.model
            ),
            year=(
                new_query.year
                if new_query.year is not None
                else old_query.year
            ),
            usage=(
                new_query.usage
                if new_query.usage is not None
                else old_query.usage
            ),
            price=(
                new_query.price
                if new_query.price is not None
                else old_query.price
            ),
            city=(
                new_query.city
                if new_query.city is not None
                else old_query.city
            ),
            body_type=(
                new_query.body_type
                if new_query.body_type is not None
                else old_query.body_type
            ),
            fuel_type=(
                new_query.fuel_type
                if new_query.fuel_type is not None
                else old_query.fuel_type
            )
        )

    def _find_vehicle_position(
        self,
        query: str
    ) -> int | None:

        query = query.lower()

        if "first" in query:
            return 0

        if "second" in query:
            return 1

        if "third" in query:
            return 2

        return None