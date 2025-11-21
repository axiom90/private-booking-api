# db.py
from supabase import acreate_client, create_client, Client, AsyncClient
from .config import config


def get_supabase_client() -> Client:
    return create_client(
        config.SUPABASE_URL, 
        config.SUPABASE_KEY
    )


async def get_supabase_async_client() -> AsyncClient:
    return await acreate_client(
        config.SUPABASE_URL, 
        config.SUPABASE_KEY
    )
