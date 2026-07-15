from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://sonar:sonar@localhost:5432/sonar_lite"
    test_database_url: str = "postgresql+asyncpg://sonar:sonar@localhost:5432/sonar_lite_test"
    ai_provider: Literal["mock", "openai"] = "mock"
    openai_api_key: str | None = None


settings = Settings()
