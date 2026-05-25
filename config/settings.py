import os
from pathlib import Path
from dotenv import load_dotenv

# Resolve the project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from the root .env file
load_dotenv(dotenv_path=ROOT_DIR / ".env")

class Settings:
    PROJECT_NAME: str = "LLM Twin MLOps"
    COLLECTION_NAME: str = "senior_dev_twin"
    
    # API Credentials
    LLM_TWIN_MLOPS: str = os.getenv("LLM_TWIN_MLOPS")
    
    # Directory Configurations
    BASE_DIR: Path = ROOT_DIR
    DATA_DIR: Path = ROOT_DIR / "my_knowledge"
    DB_PATH: Path = ROOT_DIR / "local_db"
    
    # Model Configurations
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    LLM_MODEL_NAME: str = "gemini-1.5-flash"

    def validate(self):
        """Ensure all required environment variables are present."""
        if not self.LLM_TWIN_MLOPS:
            raise ValueError(
                "CRITICAL: LLM_TWIN_MLOPS is missing from .env file. "
                "Please check your root directory for the .env file."
            )

# Global settings instance
settings = Settings()