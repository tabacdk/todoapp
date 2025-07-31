# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional

class AppSettings(BaseSettings):
    database_url: str
    alembic_database_url: Optional[str] = None
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_prefix="TODOAPP__",
        env_file_encoding="utf-8"
    )

@lru_cache
def get_settings(env_file: str = ".env.dev") -> AppSettings:
    return AppSettings(_env_file=env_file)
