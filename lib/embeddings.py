import os
from collections.abc import Sequence

from fastembed import TextEmbedding
from langchain_core.embeddings import Embeddings


class FastEmbedEmbeddings(Embeddings):
    def __init__(self, model_name: str) -> None:
        cache_directory = os.getenv("FASTEMBED_CACHE_PATH")
        self.model = TextEmbedding(model_name=model_name, cache_dir=cache_directory, threads=1)

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        return [embedding.tolist() for embedding in self.model.embed(texts, batch_size=32)]

    def embed_query(self, text: str) -> list[float]:
        return next(self.model.query_embed(text)).tolist()
