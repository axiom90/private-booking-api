from pydantic_settings import BaseSettings
from pydantic import  AnyHttpUrl
from typing import List, Literal


class Config(BaseSettings):
    # App metadata
    APP_TITLE: str       = "Private booking api"
    APP_DESCRIPTION: str = ""
    APP_VERSION: str     = "0.1.0"

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl | Literal["*"]]

    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str

    model_config = {
        "env_file": ".env",
        "extra": "allow"
    }

config = Config()