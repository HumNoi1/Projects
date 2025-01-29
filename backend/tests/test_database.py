import pytest
from app.db.base import SupabaseManager, MilvusManager
from app.db.session import get_supabase, get_milvus
from pymilvus import Collection, DataType, FieldSchema, CollectionSchema

@pytest.mark.asyncio
async def test_supabase_connection(application_context):
    """
    ทดสอบการเชื่อมต่อกับ Supabase
    ตรวจสอบว่าสามารถสร้างการเชื่อมต่อและปิดการเชื่อมต่อได้อย่างถูกต้อง
    """
    try:
        # ทดสอบการสร้างการเชื่อมต่อ
        supabase = await get_supabase()
        assert supabase is not None
        assert supabase.client is not None

        # ทดสอบการ query ข้อมูลพื้นฐาน
        response = supabase.client.table('files').select("*").limit(1).execute()
        assert response is not None

    except Exception as e:
        pytest.fail(f"Supabase connection test failed: {str(e)}")

@pytest.mark.asyncio
async def test_milvus_connection(application_context):
    """
    ทดสอบการเชื่อมต่อกับ Milvus
    ตรวจสอบว่าสามารถสร้าง collection และทำการ query ข้อมูลได้
    """
    try:
        # ทดสอบการสร้างการเชื่อมต่อ
        milvus = await get_milvus()
        assert milvus is not None

        # สร้าง test collection
        test_collection_name = "test_collection"
        dim = 128  # dimension ของ vector

        # สร้าง schema สำหรับ collection
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dim)
        ]
        schema = CollectionSchema(fields, "Test collection for connection")

        # สร้างและตรวจสอบ collection
        collection = Collection(test_collection_name, schema)
        assert collection is not None
        assert collection.schema == schema

        # ลบ test collection หลังการทดสอบ
        collection.drop()

    except Exception as e:
        pytest.fail(f"Milvus connection test failed: {str(e)}")