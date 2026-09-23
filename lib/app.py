import os
import re
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_groq import ChatGroq

from lib.embeddings import FastEmbedEmbeddings

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
VECTOR_STORE_PATH = PROJECT_ROOT / "chroma_db"
COLLECTION_NAME = "portfolio"
CURRENT_COMPENSATION_RESPONSE = "Ankit prefers to discuss his current compensation directly. Please contact him for those details."
CURRENT_COMPENSATION_PATTERN = re.compile(
    r"\b(current|present)\s+(?:ctc|compensation|salary|pay|package|remuneration)\b"
    r"|\b(?:ctc|compensation|salary|pay|package|remuneration)\s+(?:current|present)\b",
    re.IGNORECASE,
)


@st.cache_resource(show_spinner="Loading portfolio knowledge base...")
def load_services() -> tuple[Chroma, ChatGroq]:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured")
    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(VECTOR_STORE_PATH),
        embedding_function=embeddings,
    )
    return vector_store, ChatGroq(model="openai/gpt-oss-120b", api_key=api_key)


def main() -> None:
    st.set_page_config(page_title="Ankit's Portfolio Assistant", page_icon="💬")
    st.title("Ankit's Portfolio Assistant")
    question = st.chat_input("Ask about Ankit's experience")
    if not question:
        return
    if CURRENT_COMPENSATION_PATTERN.search(question):
        with st.chat_message("assistant"):
            st.write(CURRENT_COMPENSATION_RESPONSE)
        return
    try:
        vector_store, llm = load_services()
        chunks = vector_store.similarity_search(question, k=5)
        if not chunks:
            st.info("I do not have enough portfolio information to answer that. Please contact Ankit directly.")
            return
        context = "\n\n".join(chunk.page_content for chunk in chunks)
        prompt = (
            "You are Ankit Wadhwa's portfolio assistant. Answer only from the supplied "
            "portfolio context. Never disclose Ankit's current CTC or current compensation; "
            "direct visitors to contact Ankit instead. If the answer is absent, say you do not have that information.\n\n"
            f"Portfolio context:\n{context}\n\nQuestion: {question}"
        )
        with st.chat_message("assistant"):
            st.write(llm.invoke(prompt).content)
    except Exception:
        st.error("The assistant is temporarily unavailable. Please try again shortly.")


if __name__ == "__main__":
    main()
