from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("API KEY EXISTS:", bool(api_key))
print("API KEY PREFIX:", api_key[:8] if api_key else None)

client = genai.Client(
    api_key=api_key
)

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents="Say hello"
)

print(response.text)