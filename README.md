# Portfolio RAG API

A FastAPI backend that answers questions about Ankit Wadhwa's portfolio using retrieval-augmented generation. It searches a local Chroma vector store and generates grounded responses with Groq.

## Requirements

- Python 3.10 or newer
- A Groq API key

## Setup

```bash
cd "/Users/ankitwadhwa/development/Gen AI Projects/Portfolio_RAG"
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

Add your key and frontend URL to `.env`:

```dotenv
GROQ_API_KEY=your_groq_api_key
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## Index the portfolio

The knowledge base lives in `ankit_wadhwa_portfolio_knowledge_base.md`. Rebuild the vector store after changing it:

```bash
venv/bin/python lib/ingest.py
```

The generated `chroma_db` directory is local-only and is not committed to Git.

## Run the API

```bash
venv/bin/python -m uvicorn lib.main:app --reload --host 127.0.0.1 --port 8000
```

Open the interactive API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Checks whether the API and RAG services are ready. |
| `POST` | `/chat` | Answers a portfolio question using retrieved context. |
| `GET` | `/docs` | Opens Swagger UI. |
| `GET` | `/redoc` | Opens ReDoc API documentation. |

## Chat request

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What experience does Ankit have with RAG systems?",
    "history": []
  }'
```

Example response:

```json
{
  "answer": "...",
  "sources": ["Professional Summary", "Technical Skills"]
}
```

`question` accepts up to 2,000 characters. `history` is optional, allows up to six messages, and supports only `user` and `assistant` roles.

## Project structure

```text
.
├── ankit_wadhwa_portfolio_knowledge_base.md
├── lib
│   ├── ingest.py
│   ├── main.py
│   └── app.py
├── .env.example
├── requirements.txt
└── README.md
```
