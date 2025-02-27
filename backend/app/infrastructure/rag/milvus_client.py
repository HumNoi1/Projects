from pymilvus import Collection, connections, utility
from app.core.config import settings

class MilvusClient:
    def __init__(self):
        """Initialize connection to Milvus Vector DB"""
        self.host = settings.MILVUS_HOST
        self.port = settings.MILVUS_PORT
        self.collection_name = settings.MILVUS_COLLECTION
        
        # Connect to Milvus
        connections.connect(
            alias="default", 
            host=self.host, 
            port=self.port
        )
        
        # Check if collection exists, if not create it
        self._ensure_collection_exists()
    
    def _ensure_collection_exists(self):
        """Ensure that the collection exists, create if not"""
        if not utility.has_collection(self.collection_name):
            from pymilvus import CollectionSchema, FieldSchema, DataType
            
            # Define fields for the collection
            fields = [
                FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=100),
                FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=settings.EMBEDDING_DIMENSION),
                FieldSchema(name="metadata", dtype=DataType.JSON)
            ]
            
            schema = CollectionSchema(fields=fields)
            Collection(name=self.collection_name, schema=schema)
    
    def search(self, query_embedding, limit=5):
        """Search for similar vectors in Milvus"""
        collection = Collection(self.collection_name)
        collection.load()
        
        search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}
        results = collection.search(
            data=[query_embedding], 
            anns_field="embedding", 
            param=search_params,
            limit=limit,
            output_fields=["content", "metadata"]
        )
        
        return results
    
    def insert(self, texts, embeddings, metadatas=None):
        """Insert vectors into Milvus"""
        if not metadatas:
            metadatas = [{}] * len(texts)
            
        collection = Collection(self.collection_name)
        
        # Generate IDs
        import uuid
        ids = [str(uuid.uuid4()) for _ in range(len(texts))]
        
        # Insert data
        entities = [
            ids,
            texts,
            embeddings,
            metadatas
        ]
        
        collection.insert(entities)
        collection.flush()
        
        return ids