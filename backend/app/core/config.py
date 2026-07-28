from pydantic_settings import SettingsConfigDict
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    project_name: str = "cv_tailor"
    api_v1_str: str = "/api"

    secret_key: str = "its_a_new_project"
    access_token_expire_minutes: int = 60 * 24 * 8

    db_url: Optional[str] = str
    redis_url: Optional[str] = ""

    api_key_llm: Optional[str] = str

    supabase_url: str

    supabase_publishable_key: str

    supabase_secret_key: str

    supabase_jwks_url: str

    model_config = SettingsConfigDict(env_file = ".env")

settings = Settings()
