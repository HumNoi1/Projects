# tests/conftest.py
import pytest
from typing import AsyncGenerator
from app.db.base import SupabaseManager, MilvusManager

@pytest.fixture
async def supabase_client() -> AsyncGenerator[SupabaseManager, None]:
    """Fixture สำหรับการจัดการ Supabase connection ในการทดสอบ"""
    manager = SupabaseManager()
    await manager.connect()
    yield manager
    if manager.client is not None:
        await manager.disconnect()

@pytest.fixture
async def milvus_client() -> AsyncGenerator[MilvusManager, None]:
    """Fixture สำหรับการจัดการ Milvus connection ในการทดสอบ"""
    manager = MilvusManager()
    await manager.connect()
    yield manager
    await manager.disconnect()

@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup สภาพแวดล้อมสำหรับการทดสอบ"""
    from dotenv import load_dotenv
    load_dotenv(".env.test")