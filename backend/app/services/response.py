import json
from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate

from app.llm import get_llm
from app.models.searchQuery import SearchQuery
from app.models.searchResponse import SearchResponse
from app.models.vehicle import Vehicle


class ResponseService:

    def __init__(self):

        self._llm = get_llm()

        # Search response prompt
        search_prompt_path = (
            Path(__file__).parent.parent
            / "prompts"
            / "response_prompt.txt"
        )

        search_prompt = search_prompt_path.read_text(
            encoding="utf-8"
        )

        self._search_prompt = (
            ChatPromptTemplate.from_template(
                search_prompt
            )
        )

        self._search_chain = (
            self._search_prompt
            | self._llm
        )

        # Individual vehicle response prompt
        vehicle_prompt_path = (
            Path(__file__).parent.parent
            / "prompts"
            / "vehicle_response_prompt.txt"
        )

        vehicle_prompt = vehicle_prompt_path.read_text(
            encoding="utf-8"
        )

        self._vehicle_prompt = (
            ChatPromptTemplate.from_template(
                vehicle_prompt
            )
        )

        self._vehicle_chain = (
            self._vehicle_prompt
            | self._llm
        )

    def respond(
        self,
        vehicles: list[Vehicle],
        search_query: SearchQuery
    ) -> SearchResponse:

        vehicle_data = []

        for vehicle in vehicles:

            vehicle_data.append({
                "id": vehicle.id,
                "brand": vehicle.brand,
                "model": vehicle.model,
                "year": vehicle.year,
                "km_driven": vehicle.km_driven,
                "usage": vehicle.usage,
                "price": vehicle.price,
                "payload": vehicle.payload,
                "city": vehicle.city,
                "body_type": vehicle.body_type,
                "fuel_type": vehicle.fuel_type,
                "papers_verified": vehicle.papers_verified
            })

        vehicles_json = json.dumps(
            vehicle_data
        )

        response = self._search_chain.invoke({
            "brand": search_query.brand,
            "model": search_query.model,
            "year": search_query.year,
            "usage": search_query.usage,
            "price": search_query.price,
            "city": search_query.city,
            "body_type": search_query.body_type,
            "fuel_type": search_query.fuel_type,
            "vehicles": vehicles_json
        })

        return SearchResponse(
            vehicles=vehicles,
            search_query=search_query,
            assistant_response=response.content
        )

    def respond_about_vehicle(
        self,
        vehicle: Vehicle,
        query: str
    ) -> SearchResponse:

        response = self._vehicle_chain.invoke({
            "query": query,
            "brand": vehicle.brand,
            "model": vehicle.model,
            "year": vehicle.year,
            "km_driven": vehicle.km_driven,
            "price": vehicle.price,
            "usage": vehicle.usage,
            "payload": vehicle.payload,
            "city": vehicle.city,
            "body_type": vehicle.body_type,
            "fuel_type": vehicle.fuel_type,
            "papers_verified": vehicle.papers_verified
        })

        return SearchResponse(
            vehicles=[vehicle],
            search_query=SearchQuery(),
            assistant_response=response.content
        )