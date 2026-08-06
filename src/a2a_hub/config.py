"""Application configuration via environment variables and defaults."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for the A2A Hub MVP."""

    model_config = SettingsConfigDict(
        env_prefix="A2A_HUB_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(default="a2a-hub", description="Application name")
    database_path: Path = Field(
        default=Path("data/a2a_hub.db"),
        description="Path to the SQLite database file",
    )
    crawler_timeout_seconds: float = Field(
        default=30.0,
        ge=1.0,
        description="HTTP timeout for crawl fetches (seconds)",
    )
    log_level: str = Field(default="INFO", description="Logging level")
    host: str = Field(default="0.0.0.0", description="API bind host")
    port: int = Field(default=8000, ge=1, le=65535, description="API bind port")


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
