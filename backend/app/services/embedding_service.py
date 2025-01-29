# app/services/embedding_service.py
from typing import List, Dict, Any, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from pymilvus import Collection, FieldSchema, CollectionSchema, DataType, utility
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class EmbeddingService:
    """
    บริการสร้างและจัดการ embeddings โดยใช้ SentenceTransformer และ Milvus
    
    คลาสนี้รับผิดชอบ:
    1. การสร้าง embeddings จากข้อความโดยใช้ SentenceTransformer
    2. การจัดการ collection ใน Milvus
    3. การจัดเก็บและค้นหา embeddings
    """

    def __init__(self):
        # กำหนดค่าพื้นฐานสำหรับ embedding model
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.collection_name = "document_embeddings"
        self.dimension = 384  # ขนาดของ vector จาก all-MiniLM-L6-v2
        self._collection: Optional[Collection] = None

    async def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        สร้าง embeddings จากรายการข้อความ
        
        Args:
            texts: รายการข้อความที่ต้องการสร้าง embeddings
            
        Returns:
            รายการของ embeddings vectors
        """
        try:
            # แปลงข้อความเป็น embeddings
            embeddings = self.model.encode(
                texts,
                normalize_embeddings=True,  # Normalize vectors ให้มีขนาด = 1
                show_progress_bar=True,     # แสดง progress bar สำหรับข้อความจำนวนมาก
                batch_size=32               # ประมวลผลครั้งละ 32 ข้อความ
            )
            
            # แปลง numpy arrays เป็น list of lists
            return embeddings.tolist()
        
        except Exception as e:
            logger.error(f"Error creating embeddings: {str(e)}")
            raise

    def _ensure_collection(self) -> Collection:
        """
        สร้างหรือเชื่อมต่อกับ Milvus collection
        
        สร้าง collection ใหม่ถ้ายังไม่มี หรือเชื่อมต่อกับ collection ที่มีอยู่
        พร้อมทั้งสร้าง index ถ้าจำเป็น
        """
        try:
            if not utility.has_collection(self.collection_name):
                # กำหนดโครงสร้างของ collection
                fields = [
                    FieldSchema(
                        name="id",
                        dtype=DataType.INT64,
                        is_primary=True,
                        auto_id=True
                    ),
                    FieldSchema(
                        name="embedding",
                        dtype=DataType.FLOAT_VECTOR,
                        dim=self.dimension
                    ),
                    FieldSchema(
                        name="metadata",
                        dtype=DataType.JSON,
                        description="Document metadata"
                    ),
                    FieldSchema(
                        name="text_chunk",
                        dtype=DataType.VARCHAR,
                        max_length=65535,
                        description="Original text chunk"
                    )
                ]
                
                schema = CollectionSchema(
                    fields,
                    description="Document embeddings collection"
                )
                
                # สร้าง collection
                collection = Collection(
                    name=self.collection_name,
                    schema=schema,
                    using='default'
                )
                
                # สร้าง IVF_FLAT index สำหรับการค้นหาแบบ approximate nearest neighbors
                index_params = {
                    "metric_type": "COSINE",  # ใช้ cosine similarity
                    "index_type": "IVF_FLAT", # อัลกอริทึมสำหรับ ANN search
                    "params": {"nlist": 128}   # จำนวน clusters
                }
                
                collection.create_index(
                    field_name="embedding",
                    index_params=index_params
                )
                
                logger.info(f"Created new collection: {self.collection_name}")
                return collection
            else:
                collection = Collection(self.collection_name)
                # ตรวจสอบและสร้าง index ถ้ายังไม่มี
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
                return collection
                
        except Exception as e:
            logger.error(f"Error ensuring collection: {str(e)}")
            raise

    async def store_embeddings(
        self,
        embeddings: List[List[float]],
        metadata_list: List[Dict[str, Any]],
        texts: List[str]
    ) -> List[int]:
        """
        จัดเก็บ embeddings และ metadata ใน Milvus
        
        Args:
            embeddings: รายการของ embedding vectors
            metadata_list: รายการของ metadata สำหรับแต่ละ embedding
            texts: รายการข้อความต้นฉบับ
            
        Returns:
            รายการของ IDs ที่ถูกสร้างโดย Milvus
        """
        try:
            # เตรียม collection
            collection = self._ensure_collection()
            collection.load()  # โหลด collection เข้าหน่วยความจำ
            
            # เตรียมข้อมูลสำหรับการเก็บ
            entities = [
                {
                    "embedding": embedding,
                    "metadata": metadata,
                    "text_chunk": text
                }
                for embedding, metadata, text in zip(embeddings, metadata_list, texts)
            ]
            
            # บันทึกข้อมูล
            insert_result = collection.insert(entities)
            collection.flush()  # บังคับให้บันทึกลง disk ทันที
            
            logger.info(f"Successfully stored {len(embeddings)} embeddings")
            return insert_result.primary_keys
            
        except Exception as e:
            logger.error(f"Error storing embeddings: {str(e)}")
            raise
        finally:
            # ปล่อย collection เพื่อประหยัดหน่วยความจำ
            if collection is not None:
                collection.release()

    async def search_similar(
        self,
        query_text: str,
        top_k: int = 5,
        score_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        ค้นหาข้อความที่คล้ายกับ query
        
        Args:
            query_text: ข้อความที่ต้องการค้นหา
            top_k: จำนวนผลลัพธ์ที่ต้องการ
            score_threshold: คะแนนความคล้ายคลึงขั้นต่ำ (0-1)
            
        Returns:
            รายการของผลการค้นหา พร้อม metadata และคะแนนความคล้ายคลึง
        """
        try:
            # สร้าง embedding สำหรับ query
            query_embedding = await self.create_embeddings([query_text])
            
            # เตรียม collection
            collection = self._ensure_collection()
            collection.load()
            
            # ค้นหา vectors ที่ใกล้เคียงที่สุด
            search_params = {
                "metric_type": "COSINE",
                "params": {"nprobe": 16}  # จำนวน clusters ที่จะค้นหา
            }
            
            results = collection.search(
                data=query_embedding,
                anns_field="embedding",
                param=search_params,
                limit=top_k,
                output_fields=["metadata", "text_chunk"]
            )
            
            # กรองผลลัพธ์ตาม threshold และจัดรูปแบบ
            similar_docs = []
            for hits in results:
                for hit in hits:
                    if hit.score >= score_threshold:
                        similar_docs.append({
                            'text': hit.entity.get('text_chunk'),
                            'metadata': hit.entity.get('metadata'),
                            'similarity_score': hit.score
                        })
            
            return similar_docs
            
        except Exception as e:
            logger.error(f"Error searching similar documents: {str(e)}")
            raise
        finally:
            if collection is not None:
                collection.release()