# Portfolio RAG API

A FastAPI backend that answers questions about Ankit Wadhwa's portfolio using retrieval-augmented generation. It searches a local Chroma vector store and generates grounded responses with Groq.

The API uses the quantized ONNX version of `BAAI/bge-small-en-v1.5` through FastEmbed at runtime. This preserves local query embeddings and the existing Chroma RAG architecture without loading PyTorch and Sentence Transformers into the web process.

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
venv/bin/python -m lib.ingest
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
| `GET` | `/live` | Checks whether the process is running. |
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

## Docker deployment

The Docker image installs dependencies, downloads the embedding model, and creates the Chroma index while building. The running container does not need Hugging Face network access.

```bash
docker build -t portfolio-rag-api .
docker run --rm -p 8000:8000 \
  -e GROQ_API_KEY=your_groq_api_key \
  -e ALLOWED_ORIGINS=https://your-portfolio-domain.com \
  -e ENVIRONMENT=production \
  portfolio-rag-api
```

Set `GROQ_API_KEY`, `ALLOWED_ORIGINS`, and `ENVIRONMENT=production` in your deployment provider's secret or environment-variable settings. The provider must route traffic to the `PORT` environment variable, which defaults to `8000`.

Use `/live` for container liveness checks and `/health` for readiness checks. The API refuses to start in production unless `GROQ_API_KEY` and `ALLOWED_ORIGINS` are configured.

## Deploy on Render

1. Push this project to a GitHub repository. Do not commit `.env`.
2. In Render, select **New** → **Blueprint** and connect the repository. Render reads `render.yaml` and creates the Docker web service.
3. Set the required secret environment variables when Render prompts for them:

| Key | Value |
| --- | --- |
| `GROQ_API_KEY` | Your Groq API key. |
| `ALLOWED_ORIGINS` | Your deployed frontend URL, such as `https://your-portfolio.web.app`. Use commas for multiple origins. |

4. Create the service and wait for the Docker build and initial deployment to complete.
5. Copy the generated Render service URL, verify `https://your-service.onrender.com/health`, and use `https://your-service.onrender.com/docs` for API documentation.
6. Update your portfolio frontend to send requests to `https://your-service.onrender.com/chat`.

If you prefer the dashboard instead of a Blueprint, create a **Web Service**, select your repository, set the runtime to **Docker**, leave the Docker command empty, set health check path to `/health`, and add the same two secret environment variables. Render requires the application to bind to `0.0.0.0` and its `PORT` variable; the Dockerfile already does this.

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
