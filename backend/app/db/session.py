from contextvars import ContextVar
from typing import Union
from venv import logger
from .base import SupabaseManager, MilvusManager

# Context variables for database connections
supabase_context: ContextVar[SupabaseManager] = ContextVar("supabase")
milvus_context: ContextVar[MilvusManager] = ContextVar("milvus")

async def get_supabase() -> SupabaseManager:
    try:
        manager = SupabaseManager()
        await manager.connect()
        return manager
    except Exception as e:
        logger.error(f"Error connecting to Supabase: {str(e)}")
        raise

async def get_milvus() -> MilvusManager:
    try:
        return milvus_context.get()
    except LookupError:
        manager = MilvusManager()
        await manager.connect()
        milvus_context.set(manager)
        return manager