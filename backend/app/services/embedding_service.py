from langchain_community.embeddings import HuggingFaceEmbeddings
from pymilvus import connections, Collection, utility, FieldSchema, DataType, CollectionSchema
from typing import List, Optional, Dict
import numpy as np
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        # ส่วนของการกำหนดค่าเริ่มต้น
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        self.collection_name = "document_embeddings"
        self.dimension = 384  # all-MiniLM-L6-v2 dimension
        self._collection: Optional[Collection] = None
        
        self._connect_milvus()

    def _connect_milvus(self) -> None:
        """เชื่อมต่อกับ Milvus server"""
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

    def _ensure_collection(self) -> Collection:
        """สร้างและตั้งค่า collection ถ้ายังไม่มี"""
        try:
            if not utility.has_collection(self.collection_name):
                fields = [
                    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=self.dimension),
                    FieldSchema(name="metadata", dtype=DataType.JSON)
                ]
                schema = CollectionSchema(fields, description="Document embeddings collection")
                collection = Collection(name=self.collection_name, schema=schema)
                
                # สร้าง index ทันที
                index_params = {
                    "metric_type": "COSINE",
                    "index_type": "IVF_FLAT",
                    "params": {"nlist": 128}
                }
                collection.create_index(
                    field_name="embedding",
                    index_params=index_params
                )
                logger.info(f"Created new collection and index: {self.collection_name}")
                return collection
            else:
                collection = Collection(self.collection_name)
                # ตรวจสอบว่ามี index หรือยัง
                if not collection.has_index():
                    index_params = {
                        "metric_type": "COSINE",
                        "index_type": "IVF_FLAT",
                        "params": {"nlist": 128}
                    }
                    collection.create_index(
                        field_name="embedding",
                        index_params=index_params
                    )
                    logger.info(f"Created index for existing collection: {self.collection_name}")
                return collection
        except Exception as e:
            logger.error(f"Error ensuring collection: {str(e)}")
            raise

    async def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """สร้าง embeddings จากข้อความ"""
        try:
            embeddings = self.embedding_model.embed_documents(texts)
            logger.info(f"Successfully created embeddings for {len(texts)} texts")
            return embeddings
        except Exception as e:
            logger.error(f"Error creating embeddings: {str(e)}")
            raise

    async def store_embeddings(
        self,
        embeddings: List[List[float]],
        metadata: List[Dict]
    ) -> List[str]:
        """บันทึก embeddings ลงใน Milvus"""
        try:
            # ดึงหรือสร้าง collection และโหลดทันที
            collection = self._ensure_collection()
            collection.load()  # โหลด collection เข้าหน่วยความจำ
            
            # เตรียมข้อมูลสำหรับบันทึก
            entities = [
                {
                    "embedding": embedding,
                    "metadata": meta
                }
                for embedding, meta in zip(embeddings, metadata)
            ]

            # บันทึกข้อมูล
            result = collection.insert(entities)
            collection.flush()  # บังคับให้บันทึกลง disk ทันที
            
            logger.info(f"Successfully stored {len(embeddings)} embeddings")
            return result.primary_keys

        except Exception as e:
            logger.error(f"Error storing embeddings: {str(e)}")
            raise
        finally:
            # ปล่อย collection เพื่อประหยัดหน่วยความจำ
            if collection is not None:
                collection.release()