import pytest
from typing import AsyncGenerator
from app.db.base import SupabaseManager, MilvusManager

@pytest.fixture(scope="function")
async def supabase_client() -> AsyncGenerator[SupabaseManager, None]:
    manager = SupabaseManager()
    await manager.connect()
    yield manager
    await manager.disconnect()

@pytest.fixture(scope="function")
async def milvus_client() -> AsyncGenerator[MilvusManager, None]:
    manager = MilvusManager()
    await manager.connect()
    yield manager
    await manager.disconnect()

@pytest.fixture(scope="function")
async def application_context(supabase_client, milvus_client):
    """Provide application context with database connections"""
    yield