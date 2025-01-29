# tests/test_database.py
import pytest
import time
from pymilvus import Collection, DataType, FieldSchema, CollectionSchema
from app.db.base import SupabaseManager, MilvusManager

# Supabase connection
@pytest.mark.asyncio
async def test_supabase_connection(supabase_client):
    """ทดสอบการเชื่อมต่อกับ Supabase"""
    assert supabase_client.client is not None
    response = supabase_client.client.table('files').select("*").limit(1).execute()
    assert response is not None

@pytest.mark.asyncio
async def test_connection_performance():
    """ทดสอบประสิทธิภาพการเชื่อมต่อ"""
    async def connection_cycle():
        start_time = time.time()
        manager = SupabaseManager()
        await manager.connect()
        await manager.disconnect()
        return time.time() - start_time

    # ทำการทดสอบ 5 ครั้งและหาค่าเฉลี่ย
    times = []
    for _ in range(5):
        duration = await connection_cycle()
        times.append(duration)
    
    average_time = sum(times) / len(times)
    assert average_time < 1.0, f"Connection cycle took {average_time:.2f} seconds on average"

# Milvus connection
@pytest.mark.asyncio
async def test_milvus_connection(milvus_client):
    """ทดสอบการเชื่อมต่อกับ Milvus"""
    assert milvus_client._connected

    # สร้าง test collection
    test_collection_name = "test_collection"
    dim = 128

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dim)
    ]
    schema = CollectionSchema(fields, "Test collection for connection")

    collection = Collection(test_collection_name, schema)
    assert collection is not None
    assert collection.schema == schema

    # Cleanup
    collection.drop()

@pytest.mark.asyncio
async def test_milvus_connection_error():
    """ทดสอบการจัดการ error กรณีเชื่อมต่อ Milvus ไม่สำเร็จ"""
    manager = MilvusManager()
    manager.host = "invalid_host"
    
    with pytest.raises(Exception):
        await manager.connect()