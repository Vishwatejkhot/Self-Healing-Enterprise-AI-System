from langchain_openai import ChatOpenAI
from config import LLM_MODEL
from rag.vectorstore import load_store
from agents.answer_agent import answer

llm = ChatOpenAI(model=LLM_MODEL, temperature=0)

# --- Evaluation dataset ---
GROUNDING_TESTS = [
    {
        "query": "How often should API keys be rotated?",
        "must_contain": ["90 days"]
    },
    {
        "query": "Is remote work allowed?",
        "must_contain": ["3 days"]
    }
]

def check_groundedness(answer_text, context):
    prompt = f"""
You are evaluating an AI system.

Context:
{context}

Answer:
{answer_text}

Question:
Is the answer fully supported by the context?

Respond ONLY with:
YES or NO
"""
    verdict = llm.invoke(prompt).content.strip()
    return verdict == "YES"

def run_groundedness_eval():
    db = load_store()
    results = []

    for test in GROUNDING_TESTS:
        query = test["query"]
        docs = db.similarity_search(query, k=4)
        context = "\n".join([d.page_content for d in docs])

        ans = answer(query, context)
        grounded = check_groundedness(ans, context)

        passed = grounded and all(
            phrase.lower() in ans.lower()
            for phrase in test["must_contain"]
        )

        results.append({
            "query": query,
            "answer": ans,
            "grounded": grounded,
            "passed": passed
        })

    return results

if __name__ == "__main__":
    results = run_groundedness_eval()
    for r in results:
        print("=" * 60)
        print("Query:", r["query"])
        print("Answer:", r["answer"])
        print("Grounded:", r["grounded"])
        print("PASS:", r["passed"])
