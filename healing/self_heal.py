from ingestion.ingest import ingest
from healing.prompt_repair import repair_prompt

def heal(reason):
    print("[AegisAI] Healing due to:", reason)

    if "Retrieval" in reason:
        ingest(force=True)
    else:
        repair_prompt()
