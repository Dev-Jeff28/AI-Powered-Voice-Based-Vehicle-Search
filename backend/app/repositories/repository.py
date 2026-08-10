from sqlalchemy import select

from app.database.connection import SessionLocal
from app.models.searchQuery import SearchQuery
from app.models.vehicle import Vehicle
from app.repositories.interface_repository import interfaceRepository


class Repository(interfaceRepository):

    def search(
        self,
        search_query: SearchQuery,
        body_types: list[str] | None = None
    ) -> list[Vehicle]:

        query = select(Vehicle)

        if search_query.brand is not None:
            query = query.where(
                Vehicle.brand.ilike(
                    search_query.brand
                )
            )

        if search_query.model is not None:
            query = query.where(
                Vehicle.model.ilike(
                    search_query.model
                )
            )

        if search_query.year is not None:
            query = query.where(
                Vehicle.year == search_query.year
            )

        if search_query.usage is not None:
            query = query.where(
                Vehicle.usage.ilike(
                    search_query.usage
                )
            )

        if search_query.price is not None:
            query = query.where(
                Vehicle.price <= search_query.price
            )

        if search_query.city is not None:
            query = query.where(
                Vehicle.city.ilike(
                    search_query.city
                )
            )

        # Body type
        #
        # SearchService resolves broad categories
        # such as "truck" into specific database
        # body types.
        if body_types is not None:
            query = query.where(
                Vehicle.body_type.in_(
                    body_types
                )
            )

        if search_query.fuel_type is not None:
            query = query.where(
                Vehicle.fuel_type.ilike(
                    search_query.fuel_type
                )
            )

        session = SessionLocal()

        try:

            result = session.execute(query)

            vehicles = result.scalars().all()

            print(
                "Matched vehicles:",
                len(vehicles)
            )

            return vehicles

        finally:

            session.close()

    def get_by_id(
        self,
        vehicle_id: int
    ) -> Vehicle | None:

        session = SessionLocal()

        try:

            return session.get(
                Vehicle,
                vehicle_id
            )

        finally:

            session.close()