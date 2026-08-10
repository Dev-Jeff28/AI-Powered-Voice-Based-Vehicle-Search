from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = (
    BASE_DIR
    / "database"
    / "vehicle_catalog.db"
)

PROMPTS_DIR = BASE_DIR / "prompts"

OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "llama3.2"