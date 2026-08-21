from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import List, Optional

class Settings(BaseSettings):
    # Base Paths
    APP_DIR: Path = Path(__file__).resolve().parent
    ROOT_DIR: Path = APP_DIR.parent
    DATA_DIR: Path = ROOT_DIR / "data"
    KNOWLEDGE_BASE_DIR: Path = DATA_DIR / "knowledge_base"

    # Database Settings
    DATABASE_URL: str = f"sqlite:///{DATA_DIR}/hdpilot.db"
    TEST_DATABASE_URL: str = f"sqlite:///{DATA_DIR}/test-hdpilot.db"
    VECTOR_DB_FILE: Path = DATA_DIR / "knowledge_base.db"

    # LLM Settings
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-3.6-flash"
    OLLAMA_MODEL: str = "llama3.2:1b"
    OLLAMA_HOST: str = "http://localhost:11434"

    # RAG Settings
    NUM_RELEVANT_CHUNKS: int = 8

    # CORS Settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
