import os

import requests
from dotenv import load_dotenv


load_dotenv()


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000",
)


def send_message(
    query: str,
    session_id: str | None = None,
) -> dict:

    params = {
        "query": query,
    }


    if session_id is not None:

        params["session_id"] = session_id


    response = requests.put(
        f"{BACKEND_URL}/app/chat",
        params=params,
        timeout=120,
    )


    response.raise_for_status()


    return response.json()