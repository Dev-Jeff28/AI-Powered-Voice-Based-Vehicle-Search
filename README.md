# AI Vehicle Search

## Prerequisites

Before running the application, create accounts and obtain API keys for:

* **OpenRouter** — required for the LLM
* **Deepgram** — required for speech-to-text

At the time of development:

* OpenRouter provided free models with a daily limit of **50 requests**
* Deepgram provided **$200 in free credits**

> These limits and offers may change.

---

## Backend Setup

### 1. Navigate to the Backend

```bash
cd backend
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

**Windows:**

```powershell
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file inside `backend/`:

```text
backend/.env
```

Add:

```env
OPENROUTER_API_KEY=
OPENROUTER_MODEL=google/gemma-4-31b-it:free
```

Add your OpenRouter API key after `OPENROUTER_API_KEY=`.

### Prompt Files

The application uses prompt files located in:

```text
backend/app/prompts/
```

Make sure the required prompt files are present before running the application.

---

## Using Local Ollama

The application can also use a locally installed Ollama model instead of OpenRouter.

The Ollama configuration is defined in:

```text
backend/app/config.py
```

### Switch the LLM Client

Open:

```text
backend/app/main.py
```

Change:

```python
from app.clients.openrouter_client import OpenRouterClient
```

to:

```python
from app.clients.ollama_client import OllamaClient
```

Then change:

```python
llm_client = OpenRouterClient()
```

to:

```python
llm_client = OllamaClient()
```

Make sure Ollama is installed and the configured model is available locally.

---

## CLI Setup

The CLI uses a separate virtual environment because it has its own dependencies.

### 1. Navigate to the CLI

```bash
cd cli
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

**Windows:**

```powershell
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file inside `cli/`:

```text
cli/.env
```

Add:

```env
DEEPGRAM_API_KEY=
BACKEND_URL=http://127.0.0.1:8000
```

Add your Deepgram API key after `DEEPGRAM_API_KEY=`.

If the backend is running on a different host or port, update `BACKEND_URL` accordingly.

---

## Running the Application

The backend and CLI must be run in **separate terminals**, each using its respective virtual environment.

### Terminal 1 — Backend

```bash
cd backend
.venv\Scripts\activate
```

Start the FastAPI backend:

```bash
uvicorn app.main:app --reload
```

The backend will start on the configured local host and port, for example:

```text
http://127.0.0.1:8000
```

### Terminal 2 — CLI

Open a second terminal:

```bash
cd cli
.venv\Scripts\activate
```

Run the CLI:

```bash
python main.py
```

The CLI will connect to the running backend using the `BACKEND_URL` configured in `cli/.env`.
