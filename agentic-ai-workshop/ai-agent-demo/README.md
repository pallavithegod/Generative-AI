# AI Agent Demo

A small Python demo that combines **OpenAI** (chat and tool use), a **FastAPI** service, and **RAG** backed by **MongoDB Atlas Vector Search**. It shows direct LLM calls, a weather “agent” that calls geocoding and forecast APIs, and document upload plus retrieval-augmented Q&A.

## Requirements

- Python 3.10+ (uses `str | None` style hints)
- An [OpenAI API key](https://platform.openai.com/)
- For RAG endpoints: a [MongoDB Atlas](https://www.mongodb.com/atlas) cluster with **Atlas Vector Search** configured on the collection used by this app

## Setup

From the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate with `.venv\Scripts\activate` instead of `source .venv/bin/activate`.

1. **Configure environment variables**. Copy `.env.example` to `.env` and fill in real values:

   | Variable | Purpose |
   |----------|---------|
   | `OPENAI_API_KEY` | Required for all LLM and embedding calls |
   | `MONGODB_URI` | Required for `/rag/*` endpoints |
   | `MONGODB_VECTOR_INDEX` | Name of your Atlas vector index (default: `vector_index`) |

   Optional: `MONGODB_TLS_CA_FILE` — path to a CA bundle; if unset, [certifi](https://pypi.org/project/certifi/) is used for TLS to Atlas.

2. **MongoDB Atlas (RAG only)**  
   The app uses database `rag_demo_db` and collection `rag_docs` (see `shared_utils.py`). Create an **Atlas Vector Search** index whose name matches `MONGODB_VECTOR_INDEX`, with embeddings on the path LangChain expects for `MongoDBAtlasVectorSearch` (typically `embedding`). If queries fail with an index error, confirm the index name and field path in the Atlas UI.

## Running the API server

```bash
uvicorn api_server:app --reload
```

- Health: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Interactive docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### API overview

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/` | Health check |
| `POST` | `/chat/direct` | JSON body: `message`, optional `instruction` — plain LLM reply |
| `POST` | `/chat/weather` | JSON body: `message` — model uses tools to fetch weather via [Open-Meteo](https://open-meteo.com/) |
| `POST` | `/rag/instruction` | Set the system instruction used for RAG answers |
| `POST` | `/rag/upload` | Multipart file upload — chunks text and stores vectors in MongoDB (`.txt`, `.md`, `.json`, `.csv`, `.pdf`, `.docx`; legacy `.doc` may be limited) |
| `POST` | `/rag/query` | JSON body: `query`, optional `k` (1–10) — retrieve chunks and answer from context only |

## Standalone scripts

- **`basic_openai_weather.py`** — Interactive terminal chat using the OpenAI Responses API (`gpt-4.1-mini` by default). Run: `python basic_openai_weather.py`
- **`openai_mcp_weather.py`** — CLI weather agent with function calling. Run: `python openai_mcp_weather.py "What's the weather in Paris?"`

Shared model and client helpers live in **`shared_utils.py`** (`OPENAI_MODEL`, `EMBED_MODEL`, MongoDB collection wiring).

## Project layout

| File | Role |
|------|------|
| `api_server.py` | FastAPI app: chat, weather, RAG upload/query |
| `basic_openai_weather.py` | Direct LLM + interactive chat |
| `openai_mcp_weather.py` | Tool-calling weather flow |
| `shared_utils.py` | Env loading, OpenAI client, embeddings, MongoDB collection |
| `requirements.txt` | Python dependencies |

## Notes

- Weather data comes from public HTTP APIs (Open-Meteo); no API key is required for those calls.
- The filename `openai_mcp_weather.py` reflects an agent-style pattern; the implementation uses inline Python tools rather than a separate MCP server process.
