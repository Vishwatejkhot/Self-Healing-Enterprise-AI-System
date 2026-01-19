import os
import json
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.vectorstore import build_store
from ingestion.fingerprint import fingerprint_docs

DATA_DIRS = [
    "data/policies",
    "data/api_docs",
    "data/incidents"
]

META_FILE = "vectorstore/meta.json"

def ingest(force=False):
    docs = []

    for directory in DATA_DIRS:
        if not os.path.exists(directory):
            continue

        for filename in os.listdir(directory):
            if filename.endswith(".txt") or filename.endswith(".md"):
                path = os.path.join(directory, filename)
                loader = TextLoader(path, encoding="utf-8")
                docs.extend(loader.load())

    if not docs:
        raise RuntimeError("No documents found for ingestion")

    fingerprint = fingerprint_docs(docs)

    if os.path.exists(META_FILE) and not force:
        with open(META_FILE, "r") as f:
            old_fp = json.load(f)["fingerprint"]
        if old_fp == fingerprint:
            print("[AegisAI] No data drift detected")
            return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(docs)
    build_store(chunks)

    os.makedirs("vectorstore", exist_ok=True)
    with open(META_FILE, "w") as f:
        json.dump({"fingerprint": fingerprint}, f)

    print("[AegisAI] Ingestion completed successfully")

if __name__ == "__main__":
    ingest()
