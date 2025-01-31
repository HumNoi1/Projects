# tests/test_database_connection.py
import pytest
from app.db.base import SupabaseManager, MilvusManager
import time
from pymilvus import Collection, DataType, FieldSchema, CollectionSchema
import logging

logger = logging.getLogger(__name__)

class TestDatabaseConnections:
    """ทดสอบการเชื่อมต่อกับฐานข้อมูลทั้ง Supabase และ Milvus"""

    @pytest.fixture
    async def supabase_manager(self):
        manager = SupabaseManager()
        await manager.connect()
        yield manager
        await manager.disconnect()

    @pytest.fixture
    async def milvus_manager(self):
        manager = MilvusManager()
        await manager.connect()
        yield manager
        await manager.disconnect()

    @pytest.mark.asyncio
    async def test_supabase_connection(self, supabase_manager):
        """ทดสอบการเชื่อมต่อ Supabase"""
        try:
            assert supabase_manager.client is not None
            
            # ทดสอบการ query
            response = supabase_manager.client.table('files').select("*").limit(1).execute()
            assert response is not None
            
            logger.info("Supabase connection test successful")
            
        except Exception as e:
            logger.error(f"Supabase connection test failed: {str(e)}")
            raise

    @pytest.mark.asyncio
    async def test_milvus_connection(self, milvus_manager):
        """ทดสอบการเชื่อมต่อ Milvus"""
        try:
            assert milvus_manager._connected
            
            # สร้าง test collection
            test_collection_name = "test_connection_collection"
            dim = 1024  # ขนาดของ bge-m3

            fields = [
                FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dim)
            ]
            schema = CollectionSchema(fields, "Test collection")
            
            # สร้างและลบ collection เพื่อทดสอบ
            collection = Collection(test_collection_name, schema)
            assert collection is not None
            
            collection.drop()
            logger.info("Milvus connection test successful")
            
        except Exception as e:
            logger.error(f"Milvus connection test failed: {str(e)}")
            raise

    @pytest.mark.asyncio
    async def test_connection_performance(self):
        """ทดสอบประสิทธิภาพการเชื่อมต่อ"""
        async def connection_cycle():
            start_time = time.time()
            
            # ทดสอบ Supabase
            supabase = SupabaseManager()
            await supabase.connect()
            await supabase.disconnect()
            
            # ทดสอบ Milvus
            milvus = MilvusManager()
            await milvus.connect()
            await milvus.disconnect()
            
            return time.time() - start_time

        # ทำการทดสอบ 5 ครั้ง
        times = []
        for i in range(5):
            duration = await connection_cycle()
            times.append(duration)
            logger.info(f"Connection cycle {i+1}: {duration:.2f} seconds")
        
        average_time = sum(times) / len(times)
        assert average_time < 2.0, f"Connection cycle too slow: {average_time:.2f} seconds"
        
        logger.info(f"Average connection cycle time: {average_time:.2f} seconds")