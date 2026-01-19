from rag.vectorstore import load_store
from agents.answer_agent import answer

# --- Golden regression dataset ---
REGRESSION_TESTS = [
    {
        "query": "How many days of annual leave are employees entitled to?",
        "expected_keywords": ["25"]
    },
    {
        "query": "What security measures are required for customer data?",
        "expected_keywords": ["encrypted"]
    }
]

def run_regression_eval():
    db = load_store()
    failures = []

    for test in REGRESSION_TESTS:
        query = test["query"]
        docs = db.similarity_search(query, k=4)
        context = "\n".join([d.page_content for d in docs])

        ans = answer(query, context)

        missing = [
            kw for kw in test["expected_keywords"]
            if kw.lower() not in ans.lower()
        ]

        if missing:
            failures.append({
                "query": query,
                "answer": ans,
                "missing": missing
            })

    return failures

if __name__ == "__main__":
    failures = run_regression_eval()

    if not failures:
        print("Regression check passed. No quality degradation detected.")
    else:
        print("Regression failures detected:")
        for f in failures:
            print("=" * 60)
            print("Query:", f["query"])
            print("Answer:", f["answer"])
            print("Missing keywords:", f["missing"])
