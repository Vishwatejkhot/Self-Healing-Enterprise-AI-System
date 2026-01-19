#from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from config import LLM_MODEL

llm = ChatGroq(model=LLM_MODEL, temperature=0)

def answer(query, context):
    return llm.invoke(f"""
Answer ONLY from context.
If unsure, say "I don't know".

Context:
{context}

Question:
{query}
""").content
