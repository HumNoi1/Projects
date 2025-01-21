from langchain.embeddings import HuggingFaceEmbeddings
from pymilvus import connections, Collection, utility
from typing import List, Optional, Dict
import numpy as np
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        # Initialize HuggingFace embedding model
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Connect to Milvus
        self._connect_milvus()
        
        # Collection settings
        self.collection_name = "document_embeddings"
        self.dimension = 384  # all-MiniLM-L6-v2 dimension
        
    def _connect_milvus(self):
        """Establish connection with Milvus"""
        try:
            connections.connect(
                alias="default",
                host=settings.MILVUS_HOST,
                port=settings.MILVUS_PORT
            )
            logger.info("Successfully connected to Milvus")
        except Exception as e:
            logger.error(f"Failed to connect to Milvus: {str(e)}")
            raise

    async def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for given texts"""
        try:
            embeddings = self.embedding_model.embed_documents(texts)
            return embeddings
        except Exception as e:
            logger.error(f"Error creating embeddings: {str(e)}")
            raise

    async def store_embeddings(
        self,
        embeddings: List[List[float]],
        metadata: List[Dict]
    ) -> List[str]:
        """Store embeddings in Milvus"""
        try:
            # Create collection if not exists
            if not utility.has_collection(self.collection_name):
                await self._create_collection()

            collection = Collection(self.collection_name)
            collection.load()

            # Prepare data for insertion
            entities = [
                {
                    "embedding": embedding,
                    "metadata": meta
                }
                for embedding, meta in zip(embeddings, metadata)
            ]

            # Insert data
            insert_result = collection.insert(entities)
            
            return insert_result.primary_keys

        except Exception as e:
            logger.error(f"Error storing embeddings: {str(e)}")
            raise

    async def _create_collection(self):
        """Create Milvus collection with schema"""
        from pymilvus import CollectionSchema, FieldSchema, DataType

        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=self.dimension),
            FieldSchema(name="metadata", dtype=DataType.JSON)
        ]
        
        schema = CollectionSchema(
            fields, 
            "Document embeddings collection"
        )

        Collection(name=self.collection_name, schema=schema)

    async def search_similar(
        self, 
        query_embedding: List[float],
        limit: int = 5
    ) -> List[Dict]:
        """Search for similar documents"""
        try:
            collection = Collection(self.collection_name)
            collection.load()

            search_params = {
                "metric_type": "COSINE",
                "params": {"nprobe": 10},
            }

            results = collection.search(
                data=[query_embedding],
                anns_field="embedding",
                param=search_params,
                limit=limit,
                output_fields=["metadata"]
            )

            return [{
                "id": hit.id,
                "score": hit.score,
                "metadata": hit.metadata
            } for hit in results[0]]

        except Exception as e:
            logger.error(f"Error searching embeddings: {str(e)}")
            raise