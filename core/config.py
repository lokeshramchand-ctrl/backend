from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGODB_URI: str
    MONGODB_DB_NAME: str = "velar"
    MILVUS_URI: str = "https://milvus.lokeshrc.me:443"
    OLLAMA_URI: str = "http://ollama:11434"   # <-- add this

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
