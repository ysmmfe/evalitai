from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    database_url: str = ""

    # Redis
    redis_url: str = "redis://localhost:6379"

    # Storage
    minio_root_user: str = "evalitai"
    minio_root_password: str = "evalitai123"
    minio_bucket: str = "evalitai"
    storage_url: str = "http://localhost:9000"

    # LLM providers (at least one must be set to run evaluations)
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    gemini_api_key: str = ""

    # App
    evalitai_password: str = ""
    environment: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
