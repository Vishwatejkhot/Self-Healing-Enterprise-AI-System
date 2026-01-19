from langchain_groq import ChatGroq
from config import LLM_MODEL

llm = ChatGroq(model=LLM_MODEL, temperature=0)

def should_fail(hallucinated, confidence):
    # Only fail if BOTH are bad
    if hallucinated:
        return True

    # Confidence is informational, not fatal
    return False


