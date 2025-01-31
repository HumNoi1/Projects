# tests/test_pdf_processing.py
import pytest
import asyncio
from pathlib import Path
from fastapi import UploadFile
from app.services.pdf_service import PDFService
from app.services.document_processor import DocumentProcessor
from app.services.embedding_service import EmbeddingService

class TestPDFProcessing:
    """
    ชุดการทดสอบสำหรับกระบวนการประมวลผล PDF และการสร้าง Embeddings
    การทดสอบนี้จะครอบคลุมตั้งแต่การอัพโหลดไฟล์ไปจนถึงการจัดเก็บใน Milvus
    """

    @pytest.fixture
    async def sample_pdf(self):
        """
        Fixture สำหรับสร้างไฟล์ PDF ตัวอย่าง
        ในการทดสอบจริง เราควรมีไฟล์ PDF ตัวอย่างใน tests/fixtures/
        """
        pdf_path = Path("tests/fixtures/sample.pdf")
        if not pdf_path.exists():
            pytest.skip("Sample PDF file not found")
        return pdf_path

    @pytest.fixture
    def pdf_service(self):
        """Fixture สำหรับ PDF Service"""
        return PDFService()

    @pytest.fixture
    def document_processor(self):
        """Fixture สำหรับ Document Processor"""
        return DocumentProcessor()

    @pytest.fixture
    def embedding_service(self):
        """Fixture สำหรับ Embedding Service"""
        return EmbeddingService()

    @pytest.mark.asyncio
    async def test_pdf_text_extraction(self, pdf_service, sample_pdf):
        """
        ทดสอบการสกัดข้อความจากไฟล์ PDF
        การทดสอบนี้จะตรวจสอบว่าสามารถอ่านและแยกเนื้อหาจาก PDF ได้อย่างถูกต้อง
        """
        # สกัดข้อความจาก PDF
        pages = await pdf_service.extract_text(sample_pdf)

        # ตรวจสอบผลลัพธ์
        assert pages is not None
        assert len(pages) > 0
        
        # ตรวจสอบโครงสร้างข้อมูลแต่ละหน้า
        for page in pages:
            assert 'content' in page
            assert 'metadata' in page
            assert 'page_number' in page['metadata']
            assert 'total_pages' in page['metadata']
            assert len(page['content']) > 0

    @pytest.mark.asyncio
    async def test_pdf_embedding_creation(
        self,
        document_processor,
        embedding_service,
        sample_pdf
    ):
        """
        ทดสอบการสร้าง embeddings จากเนื้อหา PDF
        การทดสอบนี้ตรวจสอบว่าสามารถแปลงเนื้อหาเป็น vectors ได้อย่างถูกต้อง
        """
        # ประมวลผล PDF
        additional_metadata = {
            'document_type': 'test',
            'class_id': 1,
            'assignment_id': 1
        }
        
        result = await document_processor.process_pdf(
            sample_pdf,
            additional_metadata
        )

        # ตรวจสอบผลลัพธ์
        assert result['success']
        assert result['total_pages'] > 0
        assert len(result['embedding_ids']) > 0

    @pytest.mark.asyncio
    async def test_milvus_storage_and_retrieval(
        self,
        document_processor,
        embedding_service,
        sample_pdf
    ):
        """
        ทดสอบการจัดเก็บและค้นหา embeddings ใน Milvus
        การทดสอบนี้ตรวจสอบว่าสามารถบันทึกและค้นหาข้อมูลใน Milvus ได้อย่างถูกต้อง
        """
        # ประมวลผลและจัดเก็บ PDF
        process_result = await document_processor.process_pdf(
            sample_pdf,
            {'test_id': 1}
        )
        
        # ทดสอบการค้นหา
        # เราจะใช้ข้อความจากหน้าแรกเป็น query
        pdf_service = PDFService()
        first_page = (await pdf_service.extract_text(sample_pdf))[0]
        query_text = first_page['content'][:100]  # ใช้ 100 ตัวอักษรแรก
        
        search_results = await embedding_service.search_similar(
            query_text,
            top_k=1,
            score_threshold=0.7
        )

        # ตรวจสอบผลการค้นหา
        assert len(search_results) > 0
        assert search_results[0]['similarity_score'] >= 0.7
        assert 'metadata' in search_results[0]
        assert 'text' in search_results[0]

    @pytest.mark.asyncio
    async def test_complete_upload_flow(
        self,
        document_processor,
        embedding_service,
        sample_pdf
    ):
        """
        ทดสอบกระบวนการทั้งหมดตั้งแต่การอัพโหลดจนถึงการค้นหา
        การทดสอบนี้จำลองการทำงานจริงของระบบทั้งหมด
        """
        # จำลองการอัพโหลดไฟล์
        async def mock_file_upload():
            return UploadFile(
                filename=sample_pdf.name,
                file=open(sample_pdf, 'rb')
            )
        
        upload_file = await mock_file_upload()
        
        try:
            # ประมวลผลไฟล์ที่อัพโหลด
            processor = DocumentProcessor()
            metadata = {
                'class_id': 1,
                'assignment_id': 1,
                'upload_id': 'test-123'
            }
            
            result = await processor.process_pdf(
                Path(sample_pdf.name),
                metadata
            )
            
            assert result['success']
            assert len(result['embedding_ids']) > 0
            
            # ทดสอบการค้นหา
            search_service = EmbeddingService()
            search_results = await search_service.search_similar(
                "test query",  # ควรใช้ข้อความที่เกี่ยวข้องกับเนื้อหาใน PDF
                top_k=5
            )
            
            assert len(search_results) > 0
            
        finally:
            await upload_file.close()

    @pytest.mark.asyncio
    async def test_error_handling(self, document_processor):
        """
        ทดสอบการจัดการข้อผิดพลาดในกรณีต่างๆ
        การทดสอบนี้ตรวจสอบว่าระบบสามารถจัดการกับข้อผิดพลาดได้อย่างเหมาะสม
        """
        # ทดสอบกรณีไฟล์ไม่มีอยู่จริง
        with pytest.raises(FileNotFoundError):
            await document_processor.process_pdf(
                Path("nonexistent.pdf"),
                {}
            )
        
        # ทดสอบกรณีไฟล์ไม่ใช่ PDF
        text_file = Path("tests/fixtures/not_a_pdf.txt")
        text_file.write_text("This is not a PDF")
        
        try:
            with pytest.raises(ValueError):
                await document_processor.process_pdf(
                    text_file,
                    {}
                )
        finally:
            text_file.unlink()