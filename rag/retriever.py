from typing import Tuple
from langchain_core.documents import Document

def retrieve(db, query: str, k: int = 4):
    results = db.similarity_search_with_score(query, k=k)

    if not results:
        return "", 0.0

    documents = []
    distances = []

    for doc, score in results:
        documents.append(doc.page_content)
        distances.append(score)

    context = "\n".join(documents)

    avg_distance = sum(distances) / len(distances)

    # ---- Proper normalization ----
    # distance ~ 0   -> confidence ~ 1
    # distance ~ 1.5 -> confidence ~ 0.5
    # distance >= 3  -> confidence ~ 0
    confidence = max(0.0, min(1.0, 1.0 - (avg_distance / 3.0)))

    return context, round(confidence, 2)
