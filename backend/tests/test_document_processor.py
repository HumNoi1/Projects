# backend/tests/test_document_processor.py
import pytest
import asyncio
from app.services.document_processor import DocumentProcessor
from langchain.docstore.document import Document

def test_simple():
    """
    ทดสอบพื้นฐานเพื่อยืนยันว่าระบบทดสอบทำงานได้
    ทดสอบนี้เป็นการทดสอบง่ายๆ เพื่อตรวจสอบว่าระบบการทดสอบทำงานได้ตามปกติ
    """
    assert True

@pytest.mark.asyncio
async def test_document_processor_creation(application_context):
    """
    ทดสอบการสร้างและการทำงานของ DocumentProcessor
    
    การทดสอบนี้ครอบคลุม:
    1. การสร้าง DocumentProcessor instance
    2. การประมวลผลเอกสารทดสอบ
    3. การตรวจสอบการแบ่งชิ้นส่วนของเอกสาร
    4. การรักษา metadata ในแต่ละชิ้นส่วน
    """
    processor = DocumentProcessor()
    assert processor is not None
    
    # สร้างข้อมูลทดสอบที่มีความหลากหลาย
    test_content = "This is a test document. " * 10
    test_metadata = {
        "test": True,
        "source": "unit_test",
        "language": "en",
        "timestamp": "2024-01-22T10:00:00Z"
    }
    
    # ประมวลผลเอกสาร
    chunks = await processor.process_document(test_content, test_metadata)
    
    # ตรวจสอบผลลัพธ์อย่างละเอียด
    assert chunks is not None, "ต้องได้รับผลลัพธ์ที่ไม่เป็น None"
    assert len(chunks) > 0, "ต้องมีอย่างน้อยหนึ่งชิ้นส่วน"
    
    # ตรวจสอบแต่ละชิ้นส่วน
    for i, chunk in enumerate(chunks):
        assert isinstance(chunk, Document), f"ชิ้นส่วนที่ {i} ต้องเป็น Document object"
        assert chunk.metadata == test_metadata, f"metadata ในชิ้นส่วนที่ {i} ต้องตรงกับ metadata ต้นฉบับ"
        assert len(chunk.page_content) <= 500, f"ชิ้นส่วนที่ {i} ต้องมีขนาดไม่เกิน 500 ตัวอักษร"
        assert chunk.page_content.strip(), f"ชิ้นส่วนที่ {i} ต้องไม่เป็นข้อความว่าง"