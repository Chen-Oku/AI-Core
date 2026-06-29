from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = "postgresql+psycopg://aicore:aicore@localhost:5432/aicore"
    chroma_host: str = "localhost"
    chroma_port: int = 8000
    embedding_model: str = "nomic-embed-text"
    automatic1111_base_url: str = "http://127.0.0.1:7860"


settings = Settings()
