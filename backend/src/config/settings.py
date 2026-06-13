"""Application settings and configuration."""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application configuration from environment variables."""

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # LLM Configuration - Primary Provider
    llm_provider: str = "groq"
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

    # LLM Configuration - Fallback Provider (Ollama)
    ollama_enabled: bool = os.getenv("OLLAMA_ENABLED", "true").lower() == "true"
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama2")
    use_ollama_fallback: bool = os.getenv("USE_OLLAMA_FALLBACK", "true").lower() == "true"

    # CrewAI Configuration
    crew_verbose: bool = False
    crew_memory: bool = True
    workflow_timeout: int = 300

    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = None

    # LangSmith Integration (optional)
    langsmith_api_key: Optional[str] = None
    langsmith_enabled: bool = False

    # Knowledge Base
    chroma_db_path: str = "./data/chroma_db"

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
