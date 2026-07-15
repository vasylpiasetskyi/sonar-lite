from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://sonar:sonar@localhost:5432/sonar_lite"
    test_database_url: str = "postgresql+asyncpg://sonar:sonar@localhost:5432/sonar_lite_test"
    ai_provider: Literal["mock", "openai"] = "mock"
    openai_api_key: str | None = None
    jwt_secret_key: str = "dev-secret-change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440


settings = Settings()
