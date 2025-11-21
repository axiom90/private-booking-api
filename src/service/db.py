from functools import lru_cache
from supabase import (
    acreate_client, create_client, Client, AsyncClient
)
from .config import config

@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    return create_client(
        config.SUPABASE_URL, 
        config.SUPABASE_KEY
    )
