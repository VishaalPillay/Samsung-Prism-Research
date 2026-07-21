"""Environment-based application configuration."""

from functools import lru_cache

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    database_url: str | None = None
    secret_key: str | None = None
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    allowed_origins: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000",
        description="Comma-separated origins allowed by CORS middleware.",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @computed_field
    @property
    def cors_origins(self) -> list[str]:
        """Return configured CORS origins as a list."""

        return [
            origin.strip()
            for origin in self.allowed_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()


def validate_startup_settings() -> Settings:
    """Validate required settings during application startup."""

    settings = get_settings()
    missing_settings = [
        name
        for name, value in {
            "DATABASE_URL": settings.database_url,
            "SECRET_KEY": settings.secret_key,
        }.items()
        if not value
    ]

    if missing_settings:
        missing = ", ".join(missing_settings)
        raise ValueError(
            f"Missing required environment variable(s): {missing}. "
            "Create a .env file from .env.example and configure these values."
        )

    return settings
