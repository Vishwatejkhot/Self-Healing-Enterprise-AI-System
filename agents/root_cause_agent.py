from langchain_groq import ChatGroq
from config import LLM_MODEL

llm = ChatGroq(model=LLM_MODEL, temperature=0)

def diagnose(query, confidence):
    if confidence > 0.7:
        return "Retrieval drift"
    return llm.invoke(f"""
Query failed: {query}
Choose root cause:
- Retrieval
- Prompt
- Data staleness
""").content
