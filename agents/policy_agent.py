from langchain_groq import ChatGroq
from config import LLM_MODEL

llm = ChatGroq(model=LLM_MODEL, temperature=0)

def policy_check(answer):
    prompt = f"""
Check if the answer violates any enterprise policy:
- Security
- Privacy
- Access control

Answer:
{answer}

Respond: OK or VIOLATION
"""
    return "VIOLATION" in llm.invoke(prompt).content
