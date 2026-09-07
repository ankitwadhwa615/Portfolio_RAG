import logging
import os
import tempfile
from pathlib import Path

from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

LOGGER = logging.getLogger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_BASE_PATH = PROJECT_ROOT / "ankit_wadhwa_portfolio_knowledge_base.md"
VECTOR_STORE_PATH = PROJECT_ROOT / "chroma_db"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
COLLECTION_NAME = "portfolio"


def load_documents():
    try:
        content = KNOWLEDGE_BASE_PATH.read_text(encoding="utf-8").strip()
    except FileNotFoundError as exc:
        raise RuntimeError(f"Knowledge base was not found at {KNOWLEDGE_BASE_PATH}") from exc
    except OSError as exc:
        raise RuntimeError("Knowledge base could not be read") from exc
    if not content:
        raise RuntimeError("Knowledge base is empty")

    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("##", "section"), ("###", "subsection")])
    documents = [document for document in splitter.split_text(content) if document.page_content.strip()]
    if not documents:
        raise RuntimeError("Knowledge base did not produce any documents")
    return documents


def rebuild_vector_store() -> int:
    documents = load_documents()
    try:
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        with tempfile.TemporaryDirectory(dir=PROJECT_ROOT, prefix="portfolio-index-") as temporary_directory:
            temporary_path = Path(temporary_directory)
            staged_store_path = temporary_path / "vector_store"
            Chroma.from_documents(
                documents=documents,
                embedding=embeddings,
                collection_name=COLLECTION_NAME,
                persist_directory=str(staged_store_path),
            )
            previous_store_path = temporary_path / "previous_vector_store"
            if VECTOR_STORE_PATH.exists():
                os.replace(VECTOR_STORE_PATH, previous_store_path)
            try:
                os.replace(staged_store_path, VECTOR_STORE_PATH)
            except OSError:
                if previous_store_path.exists():
                    os.replace(previous_store_path, VECTOR_STORE_PATH)
                raise
    except Exception as exc:
        raise RuntimeError("Vector store could not be created") from exc
    return len(documents)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        count = rebuild_vector_store()
    except RuntimeError as exc:
        LOGGER.error("Ingestion failed: %s", exc)
        raise SystemExit(1) from exc
    LOGGER.info("Indexed %d portfolio documents", count)


if __name__ == "__main__":
    main()
