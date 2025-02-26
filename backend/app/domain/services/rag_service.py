from app.infrastructure.rag.embeddings import EmbeddingService
from app.infrastructure.rag.backup_embeddings import BackupEmbeddingService
from app.infrastructure.rag.milvus_client import MilvusClient
from typing import List, Dict, Any
import json

class RAGService:
    def __init__(self):
        try:
            # พยายามใช้ LMStudio embedding service ก่อน
            self.embedding_service = EmbeddingService()
            # ทดสอบว่าใช้งานได้
            test_embedding = self.embedding_service.get_query_embedding("test")
            if not test_embedding or len(test_embedding) == 0:
                raise ValueError("LMStudio embedding returned empty result")
        except Exception as e:
            print(f"Warning: LMStudio embedding service failed: {e}")
            # ถ้าไม่สำเร็จ ให้ใช้บริการสำรอง
            self.embedding_service = BackupEmbeddingService()
        
        self.milvus_client = MilvusClient()
    
    async def index_document(self, document_id: str, text: str, metadata: Dict[str, Any] = None):
        """
        สร้าง index สำหรับเอกสารในฐานข้อมูล Milvus
        """
        # ตัดแบ่งเอกสารเป็นส่วนๆ (chunks)
        chunks = self._split_text(text)
        
        # สร้าง embeddings สำหรับแต่ละ chunk
        embeddings = await self.embedding_service.get_embeddings(chunks)
        
        # เตรียมข้อมูลสำหรับ Milvus
        collection = self.milvus_client.get_collection()
        
        data = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            data.append({
                "document_id": f"{document_id}_chunk_{i}",
                "text": chunk,
                "metadata": json.dumps(metadata) if metadata else json.dumps({}),
                "embedding": embedding
            })
        
        # บันทึกลงใน Milvus
        collection.insert(data)
        
        return {
            "document_id": document_id,
            "chunks_count": len(chunks),
            "indexed": True
        }
    
    async def search_similar(self, query: str, limit: int = 5):
        """
        ค้นหาเอกสารที่คล้ายกับคำถาม
        """
        # สร้าง embedding สำหรับคำถาม
        query_embedding = await self.embedding_service.get_query_embedding(query)
        
        # ค้นหาใน Milvus
        results = await self.milvus_client.search_similar_documents(
            query_embedding=query_embedding,
            limit=limit
        )
        
        # แปลงผลลัพธ์ให้อยู่ในรูปแบบที่ใช้งานง่าย
        formatted_results = []
        for hits in results:
            for hit in hits:
                formatted_results.append({
                    "id": hit.id,
                    "document_id": hit.entity.get('document_id'),
                    "text": hit.entity.get('text'),
                    "metadata": json.loads(hit.entity.get('metadata')),
                    "score": hit.distance
                })
        
        return formatted_results
    
    def _split_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        แบ่งข้อความเป็นส่วนๆ (chunks) เพื่อสร้าง embeddings
        """
        if not text:
            return []
        
        # แบ่งข้อความตามย่อหน้า
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            # ถ้า paragraph ยาวเกินไป ให้แบ่งเป็น chunks ย่อยๆ
            if len(para) > chunk_size:
                words = para.split()
                for i in range(0, len(words), chunk_size // 10):  # ประมาณ 10 คำต่อ 100 ตัวอักษร
                    chunk = ' '.join(words[i:i + chunk_size // 10])
                    if len(current_chunk) + len(chunk) + 1 > chunk_size:
                        chunks.append(current_chunk)
                        current_chunk = chunk
                    else:
                        current_chunk += ('\n' if current_chunk else '') + chunk
            else:
                # ถ้ารวม paragraph นี้แล้วยาวเกินไป ให้สร้าง chunk ใหม่
                if len(current_chunk) + len(para) + 1 > chunk_size:
                    chunks.append(current_chunk)
                    current_chunk = para
                else:
                    current_chunk += ('\n\n' if current_chunk else '') + para
        
        # เพิ่ม chunk สุดท้าย (ถ้ามี)
        if current_chunk:
            chunks.append(current_chunk)
            
        # ถ้าต้องการ overlap ระหว่าง chunks
        if overlap > 0 and len(chunks) > 1:
            overlapped_chunks = []
            for i in range(len(chunks)):
                if i == 0:
                    overlapped_chunks.append(chunks[i])
                else:
                    # หา overlap จาก chunk ก่อนหน้า
                    prev_chunk = chunks[i-1]
                    curr_chunk = chunks[i]
                    overlap_text = prev_chunk[-overlap:] if len(prev_chunk) > overlap else prev_chunk
                    overlapped_chunks.append(overlap_text + curr_chunk)
            chunks = overlapped_chunks
            
        return chunks