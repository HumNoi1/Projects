# backend/tests/test_pdf_extraction.py
import os
import pytest
from pathlib import Path
from app.utils.pdf_processor import extract_text_from_pdf
from app.domain.services.file_service import FileService
from unittest.mock import MagicMock, patch

# กำหนดพาธสำหรับไฟล์ทดสอบ
TEST_FILES_DIR = Path(__file__).parent / "test_files"

# สร้างฟังก์ชันช่วยสำหรับการจำลองการอัปโหลดไฟล์
def create_mock_upload_file(filename, content=b"test content"):
    mock_file = MagicMock()
    mock_file.filename = filename
    mock_file.read = MagicMock(return_value=content)
    mock_file.content_type = "application/pdf"
    return mock_file

def test_text_extraction_basic_pdf():
    """
    ทดสอบการสกัดข้อความจาก PDF พื้นฐานที่มีเพียงข้อความปกติ
    
    เหตุผลของการทดสอบ: ต้องมั่นใจว่าระบบสามารถสกัดข้อความพื้นฐานได้อย่างถูกต้อง
    ซึ่งเป็นกรณีการใช้งานทั่วไปที่สุด
    """
    # สมมติว่ามีไฟล์ PDF ตัวอย่างเตรียมไว้
    pdf_path = TEST_FILES_DIR / "basic_text.pdf"
    
    # ตรวจสอบว่าไฟล์มีอยู่จริง
    assert pdf_path.exists(), "ไฟล์ทดสอบไม่พบ"
    
    # ทำการสกัดข้อความ
    extracted_text = extract_text_from_pdf(str(pdf_path))
    
    # ตรวจสอบว่าสกัดข้อความได้จริง
    assert extracted_text, "ไม่พบข้อความที่สกัดได้"
    
    # ตรวจสอบว่ามีเนื้อหาที่คาดหวัง
    expected_content = "This is a basic test document."
    assert expected_content in extracted_text, f"ไม่พบเนื้อหาที่คาดหวัง: '{expected_content}'"

def test_text_extraction_with_images_and_tables():
    """
    ทดสอบการสกัดข้อความจาก PDF ที่มีรูปภาพและตาราง
    
    เหตุผลของการทดสอบ: ในการใช้งานจริง เอกสารจะมีองค์ประกอบต่างๆ
    นอกเหนือจากข้อความล้วน เช่น รูปภาพ ตาราง และการจัดรูปแบบ
    ต้องมั่นใจว่าระบบยังคงสกัดข้อความที่มีประโยชน์ได้แม้จะมีองค์ประกอบอื่น
    """
    pdf_path = TEST_FILES_DIR / "complex_document.pdf"
    assert pdf_path.exists(), "ไฟล์ทดสอบไม่พบ"
    
    # ทำการสกัดข้อความ
    extracted_text = extract_text_from_pdf(str(pdf_path))
    
    # ตรวจสอบว่าสกัดข้อความหลักได้ถูกต้อง แม้จะมีส่วนที่เป็นรูปภาพและตาราง
    assert "Introduction to the topic" in extracted_text, "ไม่พบข้อความหัวข้อ"
    assert "Conclusion" in extracted_text, "ไม่พบข้อความสรุป"
    
    # ตรวจสอบว่าโครงสร้างยังคงอยู่ (ลำดับของเนื้อหายังคงเดิม)
    intro_pos = extracted_text.find("Introduction")
    conclusion_pos = extracted_text.find("Conclusion")
    assert intro_pos < conclusion_pos, "ลำดับของเนื้อหาไม่ถูกต้อง"

def test_text_extraction_with_different_languages():
    """
    ทดสอบการสกัดข้อความที่เป็นภาษาต่างๆ นอกจากภาษาอังกฤษ
    
    เหตุผลของการทดสอบ: ระบบควรรองรับภาษาต่างๆ โดยเฉพาะภาษาไทย
    ต้องตรวจสอบว่าการสกัดข้อความไม่ทำให้อักขระพิเศษหรือตัวอักษรภาษาต่างๆ เสียหาย
    """
    pdf_path = TEST_FILES_DIR / "multilingual_document.pdf"
    assert pdf_path.exists(), "ไฟล์ทดสอบไม่พบ"
    
    extracted_text = extract_text_from_pdf(str(pdf_path))
    
    # ตรวจสอบภาษาไทย
    assert "สวัสดี" in extracted_text, "ไม่พบข้อความภาษาไทย"
    
    # ตรวจสอบภาษาอื่นๆ ที่อาจมี
    assert "Hello" in extracted_text, "ไม่พบข้อความภาษาอังกฤษ"
    assert "你好" in extracted_text, "ไม่พบข้อความภาษาจีน"

def test_large_pdf_handling():
    """
    ทดสอบการจัดการกับไฟล์ PDF ขนาดใหญ่
    
    เหตุผลของการทดสอบ: ไฟล์ขนาดใหญ่อาจทำให้เกิดปัญหาด้านหน่วยความจำหรือประสิทธิภาพ
    ต้องมั่นใจว่าระบบสามารถจัดการได้โดยไม่ล่มหรือใช้เวลานานเกินไป
    """
    pdf_path = TEST_FILES_DIR / "large_document.pdf"  # ไฟล์ 20+ หน้า
    assert pdf_path.exists(), "ไฟล์ทดสอบไม่พบ"
    
    # ให้เวลาทำงานมากกว่าปกติเนื่องจากเป็นไฟล์ใหญ่
    import time
    start_time = time.time()
    
    extracted_text = extract_text_from_pdf(str(pdf_path))
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    # ตรวจสอบว่ามีข้อความที่สกัดได้
    assert len(extracted_text) > 1000, "สกัดข้อความได้น้อยเกินไปสำหรับเอกสารขนาดใหญ่"
    
    # ตรวจสอบว่าเวลาที่ใช้ไม่เกินที่กำหนด (ตัวอย่าง: 30 วินาที)
    assert processing_time < 30, f"ใช้เวลานานเกินไป: {processing_time} วินาที"

def test_corrupted_pdf_handling():
    """
    ทดสอบการจัดการกับไฟล์ PDF ที่เสียหาย
    
    เหตุผลของการทดสอบ: ในสถานการณ์จริง อาจมีการอัปโหลดไฟล์ที่เสียหายหรือไม่สมบูรณ์
    ระบบควรจัดการข้อผิดพลาดอย่างสง่างามและให้ข้อความแจ้งเตือนที่มีประโยชน์
    """
    pdf_path = TEST_FILES_DIR / "corrupted.pdf"
    assert pdf_path.exists(), "ไฟล์ทดสอบไม่พบ"
    
    # ทดสอบว่าฟังก์ชันจัดการข้อผิดพลาดได้ดี
    try:
        extracted_text = extract_text_from_pdf(str(pdf_path))
        # อาจพยายามสกัดข้อความได้บางส่วนหรือคืนค่าว่าง แต่ไม่ควรล่ม
        assert True  # ผ่านการทดสอบหากไม่เกิดข้อผิดพลาดร้ายแรง
    except Exception as e:
        # หากเกิดข้อผิดพลาด ควรเป็นข้อผิดพลาดเฉพาะทาง ไม่ใช่ข้อผิดพลาดทั่วไป
        assert "PDF" in str(e) or "corrupted" in str(e), f"ข้อผิดพลาดไม่ชัดเจน: {str(e)}"

@patch("app.utils.pdf_processor.extract_text_from_pdf")
async def test_file_service_upload_and_extraction(mock_extract):
    """
    ทดสอบบริการไฟล์ในการอัปโหลดและสกัดข้อความ
    
    เหตุผลของการทดสอบ: ตรวจสอบว่ากระบวนการอัปโหลดและสกัดข้อความทำงานร่วมกันได้ดี
    โดยใช้การจำลอง (mocking) เพื่อแยกการทดสอบออกจากการสกัดข้อความจริง
    """
    # จำลองการสกัดข้อความ
    mock_extract.return_value = "This is the extracted text from the document."
    
    # จำลอง Supabase client
    mock_db = MagicMock()
    mock_insert = MagicMock()
    mock_db.table.return_value.insert.return_value.execute.return_value.data = [{"id": "123"}]
    mock_db.table.return_value.insert.return_value = mock_insert
    
    # สร้างบริการไฟล์
    file_service = FileService(mock_db)
    
    # จำลองไฟล์อัปโหลด
    mock_file = create_mock_upload_file("test_document.pdf")
    
    # ทดสอบการบันทึกไฟล์
    with patch("builtins.open", MagicMock()):
        file_path = await file_service.save_file(mock_file, "teacher", "assignment123")
        assert file_path, "ไม่ได้รับพาธของไฟล์"
    
    # ทดสอบการสร้างบันทึกไฟล์
    file_record = await file_service.create_file_record(
        file_name="test_document.pdf",
        file_path=file_path,
        file_type="teacher",
        file_size=1000,
        mime_type="application/pdf",
        assignment_id="assignment123",
        text_content="This is the extracted text from the document."
    )
    
    # ตรวจสอบว่ามีการเรียกใช้งาน insert
    assert mock_db.table.called, "ไม่มีการเรียกใช้ table()"
    assert mock_db.table.return_value.insert.called, "ไม่มีการเรียกใช้ insert()"
    
    # ตรวจสอบว่าได้รับผลลัพธ์
    assert file_record == {"id": "123"}, "ไม่ได้รับบันทึกไฟล์ที่คาดหวัง"