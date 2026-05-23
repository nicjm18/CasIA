from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    openrouter_api_key: str = "sk-or-v1-placeholder"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    llm_model: str = "openai/gpt-4o-mini"
    embedding_model: str = "all-MiniLM-L6-v2"
    database_url: str = "sqlite:///./housing.db"
    cors_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    debug: bool = True
    log_level: str = "INFO"
    max_iterations: int = 5
    min_recommendations: int = 3
    min_average_score: float = 0.75
    data_dir: str = "data"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
