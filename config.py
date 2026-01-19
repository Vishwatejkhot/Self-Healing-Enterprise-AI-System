import os
from dotenv import load_dotenv

load_dotenv()

#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
#LLM_MODEL = "gpt-4o-mini"
LLM_MODEL="openai/gpt-oss-20b"
VECTOR_PATH = "vectorstore"
