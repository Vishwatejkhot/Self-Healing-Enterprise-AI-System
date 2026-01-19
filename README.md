
# 🛡️ AegisAI – Self-Healing Enterprise AI System

AegisAI is a **self-healing Retrieval-Augmented Generation (RAG) system** built for enterprise use.  
It answers questions strictly from internal documents, detects uncertainty or failures, and automatically repairs itself **without blocking the user experience**.

This project demonstrates **production-grade AI engineering**, focusing on reliability, safety, and observability rather than just chatbot responses.

---

## 🔍 What Problem Does AegisAI Solve?

In real companies:
- Internal documents are large and fragmented
- Employees ask repetitive questions
- AI systems hallucinate answers
- Wrong answers can cause serious business risk

**AegisAI solves this by:**
- Answering only from internal documents
- Refusing to hallucinate
- Measuring retrieval confidence
- Detecting failures
- Automatically self-healing when issues occur

---

## ✨ Key Features

- ✅ Retrieval-Augmented Generation (RAG)
- ✅ Vector search using FAISS
- ✅ Confidence-aware answers
- ✅ Hallucination detection
- ✅ Non-blocking self-healing loop
- ✅ Policy and safety enforcement
- ✅ Audit logging and monitoring
- ✅ Modern Flask-based UI
- ✅ API + UI support
- ✅ Groq-hosted LLMs (LLaMA / GPT-OSS)

---

## 🧠 High-Level Architecture

1. User asks a question (UI or API)
2. Relevant document chunks are retrieved from the vector store
3. LLM generates an answer using retrieved context only
4. System evaluates:
   - Answer quality
   - Retrieval confidence
   - Policy compliance
5. If uncertainty is detected:
   - Answer is still returned
   - System self-heals in the background

---

## 📁 Project Structure

```
AegisAI/
├── app.py                 # Flask app (UI + API orchestration)
├── config.py              # Central configuration
├── data/                  # Raw internal documents (source of truth)
│
├── ingestion/
│   ├── ingest.py          # Loads & chunks documents
│   └── fingerprint.py     # Detects document changes
│
├── rag/
│   ├── vectorstore.py     # FAISS vector database
│   └── retriever.py       # Context retrieval + confidence scoring
│
├── agents/
│   ├── answer_agent.py    # Generates grounded answers
│   ├── critic_agent.py    # Detects hallucinations / failures
│   ├── policy_agent.py    # Safety & policy enforcement
│   └── root_cause_agent.py# Failure diagnosis
│
├── healing/
│   ├── self_heal.py       # Automatic system repair
│   └── prompt_repair.py   # Prompt improvement
│
├── evals/
│   ├── groundedness.py    # Answer grounding checks
│   └── regression.py     # Regression testing
│
├── monitoring/
│   ├── metrics.py         # Query & failure metrics
│   └── audit_log.py       # Compliance & audit logs
│
├── tests/
│   └── inject_failures.py # Failure simulation
│
├── vectorstore/           # Generated FAISS index (rebuildable)
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## 🖥️ Running the Project Locally

### 1️⃣ Create virtual environment
```bash
uv init
uv venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 2️⃣ Install dependencies
```bash
uv add -r requirements.txt
```

### 3️⃣ Add your Groq API key
Create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```

---

### 4️⃣ Ingest documents
```bash
python -m ingestion.ingest
```

---

### 5️⃣ Run the application
```bash
python app.py
```

Open in browser:
```
http://127.0.0.1:5000
```

---

## 📊 Confidence & Self-Healing

- High confidence → normal response
- Medium confidence → response + monitoring
- Low confidence → response + background self-healing

---



## 📜 License

MIT License

---

## 🙌 Author

Vishwatej Khot
