FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV FASTEMBED_CACHE_PATH=/app/.cache/fastembed
ENV PORT=8000

WORKDIR /app

RUN groupadd --system app && useradd --system --gid app --home-dir /app app

COPY requirements.txt .
RUN python -m pip install --upgrade pip && python -m pip install -r requirements.txt

COPY lib ./lib
COPY ankit_wadhwa_portfolio_knowledge_base.md .

RUN python -c "from fastembed import TextEmbedding; TextEmbedding(model_name='BAAI/bge-small-en-v1.5', cache_dir='/app/.cache/fastembed', threads=1)"
RUN python -m lib.ingest
RUN chown -R app:app /app

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 CMD ["python", "-c", "from urllib.request import urlopen; urlopen('http://127.0.0.1:8000/live', timeout=3)"]

CMD ["sh", "-c", "python -m uvicorn lib.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"]
