from functools import lru_cache
from pathlib import Path

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.enums import Environment


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parents[3] / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    api_prefix: str = Field(default="/api/v1", description="API prefix for all routes")
    environment: Environment = Field(
        default=Environment.PRODUCTION,
        description="Environment name"
    )
    database_url: PostgresDsn = Field(
        description="PostgreSQL database URL",
        examples=["postgresql+asyncpg://user:password@localhost:5432/sca_db"]
    )
    cat_api_url: str = Field(
        default="https://api.thecatapi.com/v1/breeds",
        description="The Cat API URL for breed validation"
    )

    @property
    def debug(self) -> bool:
        """Debug mode is enabled for development environment."""
        return self.environment == Environment.DEVELOPMENT

    @property
    def database_echo(self) -> bool:
        """Database echo is enabled for development environment."""
        return self.environment == Environment.DEVELOPMENT


@lru_cache
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()


# Global settings instance
settings = get_settings()
