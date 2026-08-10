from app.models.searchQuery import SearchQuery
from app.models.searchResponse import SearchResponse
from app.repositories.interface_repository import interfaceRepository
from app.services.response import ResponseService
from app.memory.memory import Memory


TRUCK_TYPES = [
    "mini truck",
    "light truck",
    "medium truck",
    "heavy truck"
]


class SearchService:

    def __init__(
        self,
        vehicle_repository: interfaceRepository,
        response_service: ResponseService,
        memory: Memory
    ):
        self._vehicle_repository = vehicle_repository
        self._response_service = response_service
        self._memory = memory

    def search(
        self,
        search_query: SearchQuery,
        session_id: str
    ) -> SearchResponse:

        print("Search method called")

        # Resolve broad body-type categories.
        body_types = None

        if search_query.body_type is not None:

            if search_query.body_type.lower() == "truck":
                body_types = TRUCK_TYPES

            else:
                body_types = [
                    search_query.body_type
                ]

        vehicles = self._vehicle_repository.search(
            search_query,
            body_types
        )

        ranked_vehicles = []

        for vehicle in vehicles:

            exact_match_score = 0
            distance = 0

            # Brand
            if search_query.brand is not None:

                if (
                    vehicle.brand.lower()
                    == search_query.brand.lower()
                ):
                    exact_match_score += 1

            # Model
            if search_query.model is not None:

                if (
                    vehicle.model.lower()
                    == search_query.model.lower()
                ):
                    exact_match_score += 1

            # Year
            if search_query.year is not None:

                if vehicle.year == search_query.year:
                    exact_match_score += 1

                distance += abs(
                    vehicle.year
                    - search_query.year
                )

            # Usage
            if search_query.usage is not None:

                if (
                    vehicle.usage.lower()
                    == search_query.usage.lower()
                ):
                    exact_match_score += 1

            # Price
            if search_query.price is not None:

                distance += abs(
                    vehicle.price
                    - search_query.price
                )

            # City
            if search_query.city is not None:

                if (
                    vehicle.city.lower()
                    == search_query.city.lower()
                ):
                    exact_match_score += 1

            # Body type
            if search_query.body_type is not None:

                if (
                    search_query.body_type.lower()
                    == "truck"
                ):

                    if (
                        vehicle.body_type.lower()
                        in TRUCK_TYPES
                    ):
                        exact_match_score += 1

                elif (
                    vehicle.body_type.lower()
                    == search_query.body_type.lower()
                ):
                    exact_match_score += 1

            # Fuel type
            if search_query.fuel_type is not None:

                if (
                    vehicle.fuel_type.lower()
                    == search_query.fuel_type.lower()
                ):
                    exact_match_score += 1

            ranked_vehicles.append(
                (
                    vehicle,
                    exact_match_score,
                    distance
                )
            )

        # Higher exact-match score first.
        # For equal scores, smaller distance first.
        ranked_vehicles.sort(
            key=lambda item: (
                -item[1],
                item[2]
            )
        )

        # Only top 3 are sent forward.
        top_vehicles = [
            item[0]
            for item in ranked_vehicles[:3]
        ]

        print(
            "\nTop 3 vehicles from database:"
        )

        for vehicle in top_vehicles:

            print(
                f"ID: {vehicle.id} | "
                f"{vehicle.brand} "
                f"{vehicle.model} | "
                f"Year: {vehicle.year} | "
                f"Price: ₹{vehicle.price} | "
                f"City: {vehicle.city}"
            )

        # Store current conversation state.
        conversation_memory = (
            self._memory.get(session_id)
        )

        conversation_memory.search_query = (
            search_query
        )

        conversation_memory.vehicle_ids = [
            vehicle.id
            for vehicle in top_vehicles
        ]

        self._memory.update(
            session_id,
            conversation_memory
        )

        return self._response_service.respond(
            top_vehicles,
            search_query
        )