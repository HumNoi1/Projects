import pytest
from app.services.document_processor import DocumentProcessor

def test_simple():
    """ทดสอบพื้นฐานเพื่อยืนยันว่าระบบทดสอบทำงานได้"""
    assert True

@pytest.mark.asyncio
async def test_document_processor_creation(event_loop):
    """ทดสอบการสร้าง DocumentProcessor instance
    
    ใช้ event_loop fixture เพื่อจัดการ async context อย่างถูกต้อง
    """
    processor = DocumentProcessor()
    assert processor is not None
    
    # ทดสอบการทำงานพื้นฐาน
    test_content = "This is a test document"
    test_metadata = {"test": True}
    
    chunks = await processor.process_document(test_content, test_metadata)
    assert chunks is not None