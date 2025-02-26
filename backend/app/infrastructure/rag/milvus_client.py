from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
from app.core.config import settings

def setup_milvus_collection():
    """
    สร้าง collection ใน Milvus สำหรับเก็บ embeddings
    """
    # เชื่อมต่อกับ Milvus
    connections.connect(
        alias="default",
        host=settings.MILVUS_HOST,
        port=settings.MILVUS_PORT
    )
    
    collection_name = settings.MILVUS_COLLECTION
    
    # ตรวจสอบว่า collection มีอยู่แล้วหรือไม่
    if utility.has_collection(collection_name):
        print(f"Collection {collection_name} already exists.")
        return Collection(collection_name)
    
    # กำหนดโครงสร้างของ collection
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="document_id", dtype=DataType.VARCHAR, max_length=100),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
        FieldSchema(name="metadata", dtype=DataType.JSON),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=settings.EMBEDDING_DIMENSION)
    ]
    
    schema = CollectionSchema(fields=fields, description=f"Collection for {settings.PROJECT_NAME}")
    collection = Collection(name=collection_name, schema=schema)
    
    # สร้าง index สำหรับการค้นหาด้วย vector similarity
    index_params = {
        "metric_type": "COSINE",
        "index_type": "HNSW",
        "params": {"M": 8, "efConstruction": 64}
    }
    
    collection.create_index(field_name="embedding", index_params=index_params)
    print(f"Created collection {collection_name} with index.")
    
    return collection