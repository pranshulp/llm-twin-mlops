import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

class Settings:
    PROJECT_NAME = "LLM Twin MLOps"
    COLLECTION_NAME = "senior_dev_twin"
    
    DATA_DIR = ROOT_DIR / "my_knowledge"
    DB_PATH = ROOT_DIR / "local_db"
    
    # --- RAG Configurations ---
    CHUNK_SIZE = 600
    CHUNK_OVERLAP = 100
    
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    LLM_MODEL = "phi3"
    TEMPERATURE = 0

    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

settings = Settings()