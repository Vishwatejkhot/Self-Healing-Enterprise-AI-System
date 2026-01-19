import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import EMBED_MODEL, VECTOR_PATH

def _get_embeddings():
    """
    Centralized embedding factory.
    Makes swapping models trivial.
    """
    return HuggingFaceEmbeddings(model_name=EMBED_MODEL)

def build_store(documents):
    """
    Build FAISS vector store from documents.
    This is a destructive operation and overwrites existing index.
    """
    os.makedirs(VECTOR_PATH, exist_ok=True)

    embeddings = _get_embeddings()
    db = FAISS.from_documents(documents, embeddings)

    db.save_local(VECTOR_PATH)
    print("[AegisAI] Vectorstore built successfully")

def load_store():
    """
    Load existing FAISS vector store.
    Fails loudly if missing — this is intentional.
    """
    embeddings = _get_embeddings()

    if not os.path.exists(VECTOR_PATH):
        raise RuntimeError(
            "Vectorstore not found. Run ingestion first."
        )

    return FAISS.load_local(
        VECTOR_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
