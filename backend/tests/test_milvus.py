import os
from dotenv import load_dotenv
from pymilvus import connections, utility, Collection, FieldSchema, CollectionSchema, DataType

# โหลดตัวแปรจาก .env
load_dotenv()
host = os.getenv("MILVUS_HOST", "localhost")
port = os.getenv("MILVUS_PORT", "19530")

def test_milvus_connection():
    """ทดสอบการเชื่อมต่อกับ Milvus"""
    try:
        # เชื่อมต่อกับ Milvus
        connections.connect(
            alias="default", 
            host=host, 
            port=port
        )
        
        print("✅ เชื่อมต่อกับ Milvus สำเร็จ")
        
        # ตรวจสอบเวอร์ชัน Milvus
        if utility.get_server_version():
            print(f"เวอร์ชัน Milvus: {utility.get_server_version()}")
        
        return True
    except Exception as e:
        print(f"❌ ไม่สามารถเชื่อมต่อกับ Milvus: {str(e)}")
        return False

def test_milvus_collection():
    """ทดสอบการสร้างและลบ collection ใน Milvus"""
    collection_name = "test_collection"
    dim = int(os.getenv("EMBEDDING_DIMENSION", "384"))
    
    try:
        # ตรวจสอบว่า collection มีอยู่แล้วหรือไม่
        if utility.has_collection(collection_name):
            utility.drop_collection(collection_name)
            print(f"ลบ collection {collection_name} เดิม")
        
        # กำหนดโครงสร้าง collection
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim)
        ]
        
        schema = CollectionSchema(fields=fields, description="Test collection for vector search")
        
        # สร้าง collection
        collection = Collection(name=collection_name, schema=schema)
        
        print(f"✅ สร้าง collection {collection_name} สำเร็จ")
        
        # สร้าง index สำหรับการค้นหา
        index_params = {
            "metric_type": "COSINE",
            "index_type": "HNSW",
            "params": {"M": 8, "efConstruction": 64}
        }
        
        collection.create_index(field_name="embedding", index_params=index_params)
        print(f"✅ สร้าง index สำหรับ collection {collection_name} สำเร็จ")
        
        # ลบ collection เพื่อทำความสะอาด
        utility.drop_collection(collection_name)
        print(f"ลบ collection {collection_name} สำเร็จ")
        
        return True
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการทดสอบ Milvus collection: {str(e)}")
        return False

if __name__ == "__main__":
    print("ทดสอบการเชื่อมต่อกับ Milvus...")
    connection_success = test_milvus_connection()
    
    if connection_success:
        print("\nทดสอบการสร้างและลบ collection...")
        test_milvus_collection()