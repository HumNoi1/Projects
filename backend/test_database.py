# backend/test_database.py (แก้ไขใหม่)
import asyncio
from app.core.config import settings
from supabase import create_client
from pymilvus import connections

def test_database_connections():
    print("Testing database connections...")
    
    # Test Supabase (ใช้แบบ synchronous)
    print("\nTesting Supabase connection:")
    try:
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        result = supabase.table('files').select('*').limit(1).execute()
        print(f"✅ Supabase connection successful")
    except Exception as e:
        print(f"❌ Supabase connection failed: {str(e)}")
    
    # Test Milvus
    print("\nTesting Milvus connection:")
    try:
        connections.connect("default", host=settings.MILVUS_HOST, port=settings.MILVUS_PORT)
        print("✅ Milvus connection successful")
        connections.disconnect("default")
    except Exception as e:
        print(f"❌ Milvus connection failed: {str(e)}")

if __name__ == "__main__":
    test_database_connections()