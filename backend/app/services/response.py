import json
from pathlib import Path

from app.clients.llm_client import LLMClient
from app.models.searchQuery import SearchQuery
from app.models.searchResponse import SearchResponse
from app.models.vehicle import Vehicle


class ResponseService:

    def __init__(self, llm_client: LLMClient):
        self._llm_client = llm_client

    def respond(
        self,
        vehicles: list[Vehicle],
        search_query: SearchQuery
    ) -> SearchResponse:

        prompt_path = (
            Path(__file__).parent.parent
            / "prompts"
            / "response_prompt.txt"
        )

        prompt = prompt_path.read_text(
            encoding="utf-8"
        )

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

        prompt = prompt.replace(
            "{brand}",
            str(search_query.brand)
        )

        prompt = prompt.replace(
            "{model}",
            str(search_query.model)
        )

        prompt = prompt.replace(
            "{year}",
            str(search_query.year)
        )

        prompt = prompt.replace(
            "{usage}",
            str(search_query.usage)
        )

        prompt = prompt.replace(
            "{price}",
            str(search_query.price)
        )

        prompt = prompt.replace(
            "{city}",
            str(search_query.city)
        )

        prompt = prompt.replace(
            "{body_type}",
            str(search_query.body_type)
        )

        prompt = prompt.replace(
            "{fuel_type}",
            str(search_query.fuel_type)
        )

        prompt = prompt.replace(
            "{vehicles}",
            vehicles_json
        )

        assistant_response = self._llm_client.generate(
            prompt
        )

        return SearchResponse(
            vehicles=vehicles,
            search_query=search_query,
            assistant_response=assistant_response
        )

    def respond_about_vehicle(
        self,
        vehicle: Vehicle
    ) -> SearchResponse:

        prompt = f"""
Give the user a natural, conversational description of this
commercial vehicle.

Vehicle:
brand: {vehicle.brand}
model: {vehicle.model}
year: {vehicle.year}
km_driven: {vehicle.km_driven}
price: {vehicle.price}
usage: {vehicle.usage}
payload: {vehicle.payload}
city: {vehicle.city}
body_type: {vehicle.body_type}
fuel_type: {vehicle.fuel_type}
papers_verified: {vehicle.papers_verified}

Explain the vehicle naturally.
Mention the important details.
Do not invent information.
Do not mention vehicles other than this vehicle.
Do not ask another question unless necessary.

Return only the natural language response.
"""

        response = self._llm_client.generate(
            prompt
        )

        return SearchResponse(
            vehicles=[vehicle],
            assistant_response=response
        )