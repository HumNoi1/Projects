from contextvars import ContextVar
from typing import Union
from .base import SupabaseManager, MilvusManager

# Context variables for database connections
supabase_context: ContextVar[SupabaseManager] = ContextVar("supabase")
milvus_context: ContextVar[MilvusManager] = ContextVar("milvus")

async def get_supabase() -> SupabaseManager:
    try:
        return supabase_context.get()
    except LookupError:
        manager = SupabaseManager()
        await manager.connect()
        supabase_context.set(manager)
        return manager

async def get_milvus() -> MilvusManager:
    try:
        return milvus_context.get()
    except LookupError:
        manager = MilvusManager()
        await manager.connect()
        milvus_context.set(manager)
        return manager