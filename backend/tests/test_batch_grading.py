# backend/tests/test_batch_grading.py
import pytest
import uuid
from unittest.mock import MagicMock, patch, AsyncMock
from app.domain.services.batch_grading_service import BatchGradingService
from app.infrastructure.llm.chains import GradingChain

@pytest.fixture
def mock_db():
    """สร้าง fixture สำหรับจำลอง database client"""
    db = MagicMock()
    
    # จำลองการดึงข้อมูล batch
    mock_batch = {
        "id": "batch-123",
        "assignment_id": "assignment-123",
        "teacher_file_id": "teacher-file-123",
        "status": "created"
    }
    db.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [mock_batch]
    
    # จำลองการดึงข้อมูลไฟล์อาจารย์
    mock_teacher_file = {
        "id": "teacher-file-123",
        "text_content": "The correct answer is systematic testing is important."
    }
    db.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [mock_teacher_file]
    
    # จำลองการดึงข้อมูลไฟล์นักเรียน
    mock_student_files = [
        {
            "id": "student-1",
            "student_id": "student-id-1",
            "student_name": "Alice",
            "text_content": "I believe systematic testing is important.",
            "created_at": "2023-01-01"
        },
        {
            "id": "student-2",
            "student_id": "student-id-2",
            "student_name": "Bob",
            "text_content": "Testing is unnecessary in some cases.",
            "created_at": "2023-01-02"
        }
    ]
    
    # สร้างฟังก์ชันเพื่อคืนค่าที่แตกต่างกันตามค่า parameter
    def get_data_based_on_eq(*args, **kwargs):
        result = MagicMock()
        if 'teacher-file-123' in str(args):
            result.data = [mock_teacher_file]
        elif 'batch-123' in str(args):
            result.data = [mock_batch]
        else:
            # ค้นหาไฟล์นักเรียนตาม ID
            for arg in args:
                for student in mock_student_files:
                    if student['id'] == arg:
                        result.data = [student]
                        return result
            # ถ้าไม่พบการค้นหาเฉพาะ คืนค่าทั้งหมด
            result.data = mock_student_files
        return result
    
    # ตั้งค่าการจำลองเพื่อคืนค่าที่แตกต่างกัน
    db.table.return_value.select.return_value.eq.return_value.execute.side_effect = get_data_based_on_eq
    
    return db

@pytest.fixture
def mock_grading_chain():
    """สร้าง fixture สำหรับจำลอง GradingChain"""
    grading_chain = MagicMock(spec=GradingChain)
    
    # จำลองฟังก์ชัน grade_submission ให้เป็น async function
    async def mock_grade(*args, **kwargs):
        teacher_text = kwargs.get('teacher_text', '')
        student_text = kwargs.get('student_text', '')
        
        # จำลองการให้คะแนนอย่างง่าย: ถ้ามีคำสำคัญคล้ายกัน ให้คะแนนสูง
        similarity = set(teacher_text.lower().split()) & set(student_text.lower().split())
        score = min(len(similarity) * 10, 100)
        
        return {
            "score": score,
            "feedback": f"Your answer received a score of {score}/100.",
            "strengths": ["Good understanding"] if score > 60 else [],
            "areas_for_improvement": ["Need more clarity"] if score < 80 else [],
            "missed_concepts": ["Important concept"] if score < 70 else []
        }
    
    grading_chain.grade_submission = AsyncMock(side_effect=mock_grade)
    return grading_chain

@patch('app.domain.services.grading_service.GradingService')
@patch('app.domain.services.file_service.FileService')
async def test_batch_process_creation(mock_file_service, mock_grading_service, mock_db):
    """
    ทดสอบการสร้างกระบวนการตรวจงานแบบกลุ่มใหม่
    
    เหตุผลของการทดสอบ: ต้องมั่นใจว่าระบบสามารถสร้างกระบวนการตรวจงานแบบกลุ่มใหม่ได้อย่างถูกต้อง
    และกำหนดค่าเริ่มต้นอย่างเหมาะสม
    """
    # สร้าง BatchGradingService
    batch_service = BatchGradingService(mock_db)
    
    # จำลองไฟล์ที่อัปโหลด
    mock_file = MagicMock()
    mock_file.filename = "teacher_answer.pdf"
    mock_file.content_type = "application/pdf"
    
    # จำลองผลลัพธ์การบันทึกไฟล์
    mock_file_path = "/path/to/uploaded/file.pdf"
    mock_file_service.return_value.save_file.return_value = mock_file_path
    
    # จำลองการสกัดข้อความ
    with patch('app.utils.pdf_processor.extract_text_from_pdf') as mock_extract:
        mock_extract.return_value = "Sample extracted text from teacher file"
        
        # จำลองการสร้างบันทึกไฟล์
        mock_file_record = {"id": "new-file-123"}
        mock_file_service.return_value.create_file_record.return_value = mock_file_record
        
        # ทดสอบฟังก์ชัน process_teacher_file
        assignment_id = "assignment-test"
        batch_id = str(uuid.uuid4())
        
        result = await batch_service.process_teacher_file(mock_file, assignment_id, batch_id)
        
        # ตรวจสอบว่ามีการเรียกฟังก์ชันที่จำเป็น
        assert mock_file_service.return_value.save_file.called, "ไม่มีการเรียกฟังก์ชัน save_file"
        assert mock_extract.called, "ไม่มีการเรียกฟังก์ชัน extract_text_from_pdf"
        assert mock_file_service.return_value.create_file_record.called, "ไม่มีการเรียกฟังก์ชัน create_file_record"
        
        # ตรวจสอบว่ามีการสร้างบันทึก batch
        assert mock_db.table.return_value.insert.called, "ไม่มีการเรียกฟังก์ชัน insert สำหรับบันทึก batch"
        
        # ตรวจสอบผลลัพธ์
        assert result == mock_file_record, "ผลลัพธ์ไม่ตรงกับที่คาดหวัง"

@patch('app.domain.services.grading_service.GradingService')
async def test_batch_process_multiple_students(mock_grading_service, mock_db, mock_grading_chain):
    """
    ทดสอบการตรวจงานของนักเรียนหลายคนในกลุ่มเดียวกัน
    
    เหตุผลของการทดสอบ: ต้องมั่นใจว่าระบบสามารถตรวจงานของนักเรียนหลายคนได้อย่างถูกต้อง
    และบันทึกผลการตรวจแต่ละคนแยกกัน
    """
    # ตั้งค่าการจำลอง GradingService
    mock_grading_service.return_value.grade_submission = mock_grading_chain.grade_submission
    
    # สร้าง BatchGradingService
    batch_service = BatchGradingService(mock_db)
    
    # รายการ IDs ของไฟล์นักเรียน
    student_file_ids = ["student-1", "student-2"]
    batch_id = "batch-123"
    
    # ทดสอบการประมวลผลกลุ่ม
    await batch_service.process_batch(batch_id, student_file_ids)
    
    # ตรวจสอบว่ามีการอัปเดตสถานะ batch เป็น processing
    assert mock_db.table.return_value.update.called, "ไม่มีการอัปเดตสถานะ batch"
    update_calls = mock_db.table.return_value.update.call_args_list
    assert any("processing" in str(call) for call in update_calls), "ไม่พบการอัปเดตสถานะเป็น processing"
    
    # ตรวจสอบว่ามีการตรวจงานของนักเรียนทุกคน
    assert mock_grading_chain.grade_submission.call_count >= len(student_file_ids), f"มีการเรียก grade_submission เพียง {mock_grading_chain.grade_submission.call_count} ครั้ง แต่คาดหวัง {len(student_file_ids)} ครั้ง"
    
    # ตรวจสอบว่ามีการบันทึกผลการตรวจงานของนักเรียนทุกคน
    insert_calls = mock_db.table.return_value.insert.call_args_list
    assert len(insert_calls) >= len(student_file_ids), f"มีการเรียก insert เพียง {len(insert_calls)} ครั้ง แต่คาดหวัง {len(student_file_ids)} ครั้ง"
    
    # ตรวจสอบว่ามีการอัปเดตสถานะ batch เป็น completed
    assert any("completed" in str(call) for call in update_calls), "ไม่พบการอัปเดตสถานะเป็น completed"

async def test_batch_process_with_error_handling(mock_db, mock_grading_chain):
    """
    ทดสอบการรับมือกับข้อผิดพลาดระหว่างการตรวจงานกลุ่ม
    
    เหตุผลของการทดสอบ: ต้องมั่นใจว่าระบบสามารถจัดการกับข้อผิดพลาดที่อาจเกิดขึ้นได้
    โดยไม่ทำให้การตรวจงานทั้งหมดล้มเหลว (ตรวจงานคนอื่นต่อได้แม้บางคนมีปัญหา)
    """
    # สร้าง BatchGradingService
    batch_service = BatchGradingService(mock_db)
    
    # ปรับ mock เพื่อให้เกิดข้อผิดพลาดกับนักเรียนคนที่ 2
    async def mock_grade_with_error(*args, **kwargs):
        student_text = kwargs.get('student_text', '')
        if "unnecessary" in student_text:  # ข้อความของนักเรียนคนที่ 2
            raise Exception("Testing error handling")
        
        return {
            "score": 80,
            "feedback": "Good job!",
            "strengths": ["Clear explanation"],
            "areas_for_improvement": [],
            "missed_concepts": []
        }
    
    # ตั้งค่า mock
    with patch('app.domain.services.grading_service.GradingService') as mock_grading_service:
        mock_grading_service.return_value.grade_submission = AsyncMock(side_effect=mock_grade_with_error)
        batch_service.grading_service = mock_grading_service.return_value
        
        # รายการ IDs ของไฟล์นักเรียน
        student_file_ids = ["student-1", "student-2"]
        batch_id = "batch-123"
        
        # ทดสอบการประมวลผลกลุ่ม
        await batch_service.process_batch(batch_id, student_file_ids)
        
        # ตรวจสอบว่ายังคงดำเนินการต่อแม้จะมีข้อผิดพลาด
        insert_calls = mock_db.table.return_value.insert.call_args_list
        assert len(insert_calls) >= len(student_file_ids), f"มีการเรียก insert เพียง {len(insert_calls)} ครั้ง แต่คาดหวัง {len(student_file_ids)} ครั้ง"
        
        # ตรวจสอบว่ามีการบันทึกข้อผิดพลาด
        error_recorded = False
        for call in insert_calls:
            call_args = str(call)
            if "student-2" in call_args and "error" in call_args:
                error_recorded = True
                break
        
        assert error_recorded, "ไม่พบการบันทึกข้อผิดพลาดสำหรับนักเรียนคนที่ 2"
        
        # ตรวจสอบว่ามีการอัปเดตสถานะ batch เป็น completed แม้จะมีข้อผิดพลาด
        update_calls = mock_db.table.return_value.update.call_args_list
        assert any("completed" in str(call) for call in update_calls), "ไม่พบการอัปเดตสถานะเป็น completed"

async def test_large_batch_processing(mock_db):
    """
    ทดสอบการตรวจงานกลุ่มขนาดใหญ่
    
    เหตุผลของการทดสอบ: ต้องมั่นใจว่าระบบสามารถจัดการกับงานจำนวนมากได้
    โดยไม่เกิดปัญหาด้านหน่วยความจำหรือประสิทธิภาพ
    """
    # สร้าง mock ข้อมูลนักเรียนจำนวนมาก (50 คน)
    large_student_files = []
    for i in range(50):
        large_student_files.append({
            "id": f"student-{i}",
            "student_id": f"student-id-{i}",
            "student_name": f"Student {i}",
            "text_content": f"Answer from student {i} about testing.",
            "created_at": "2023-01-01"
        })
    
    # ปรับค่า mock database สำหรับกรณีนี้
    mock_db.table.return_value.select.return_value.eq.return_value.execute.return_value.data = large_student_files
    
    # สร้าง BatchGradingService
    batch_service = BatchGradingService(mock_db)
    
    # จำลองการตรวจงานที่ทำงานเร็ว
    async def fast_grade(*args, **kwargs):
        return {
            "score": 75,
            "feedback": "Quick feedback for testing",
            "strengths": ["Good point"],
            "areas_for_improvement": ["Improve clarity"],
            "missed_concepts": []
        }
    
    # ตั้งค่า mock
    with patch('app.domain.services.grading_service.GradingService') as mock_grading_service:
        mock_grading_service.return_value.grade_submission = AsyncMock(side_effect=fast_grade)
        batch_service.grading_service = mock_grading_service.return_value
        
        # สร้างรายการ IDs ของไฟล์นักเรียน
        student_file_ids = [f"student-{i}" for i in range(50)]
        batch_id = "batch-large"
        
        # จับเวลา
        import time
        start_time = time.time()
        
        # ทดสอบการประมวลผลกลุ่ม
        await batch_service.process_batch(batch_id, student_file_ids)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # ตรวจสอบว่ามีการบันทึกผลการตรวจงานทั้งหมด
        insert_calls = mock_db.table.return_value.insert.call_args_list
        
        # นับจำนวนการ insert ที่เกี่ยวข้องกับผลการตรวจ (ไม่รวมการ insert อื่นๆ)
        batch_result_inserts = 0
        for call in insert_calls:
            if "batch_results" in str(call):
                batch_result_inserts += 1
        
        assert batch_result_inserts >= len(student_file_ids), f"มีการบันทึกผลการตรวจเพียง {batch_result_inserts} รายการ แต่คาดหวัง {len(student_file_ids)} รายการ"
        
        # ตรวจสอบว่าใช้เวลาไม่เกินที่กำหนด (เช่น 0.1 วินาทีต่อนักเรียน 1 คน)
        max_expected_time = 0.1 * len(student_file_ids)
        assert processing_time < max_expected_time, f"ใช้เวลานานเกินไป: {processing_time} วินาที ซึ่งมากกว่า {max_expected_time} วินาที"

async def test_get_batch_results(mock_db):
    """
    ทดสอบการดึงผลการตรวจงานกลุ่ม
    
    เหตุผลของการทดสอบ: ต้องมั่นใจว่าผู้ใช้สามารถดึงผลการตรวจงานของกลุ่มได้
    เพื่อแสดงผลหรือวิเคราะห์ต่อไป
    """
    # จำลองผลการตรวจงาน
    mock_results = [
        {
            "id": "result-1",
            "batch_id": "batch-123",
            "student_file_id": "student-1",
            "student_id": "student-id-1",
            "student_name": "Alice",
            "score": 85,
            "feedback": "Good job!",
            "strengths": ["Clear explanation"],
            "areas_for_improvement": ["Add more examples"],
            "status": "completed",
            "graded_at": "2023-01-05"
        },
        {
            "id": "result-2",
            "batch_id": "batch-123",
            "student_file_id": "student-2",
            "student_id": "student-id-2",
            "student_name": "Bob",
            "score": 70,
            "feedback": "Needs improvement.",
            "strengths": ["Good introduction"],
            "areas_for_improvement": ["Expand on core concepts"],
            "status": "completed",
            "graded_at": "2023-01-05"
        }
    ]
    
    # ตั้งค่า mock สำหรับ get_batch_results
    mock_db.table.return_value.select.return_value.eq.return_value.execute.return_value.data = mock_results
    
    # สร้าง BatchGradingService
    batch_service = BatchGradingService(mock_db)
    
    # ทดสอบการดึงผลการตรวจงาน
    batch_id = "batch-123"
    results = await batch_service.get_batch_results(batch_id)
    
    # ตรวจสอบว่ามีการเรียกใช้ select และ eq ด้วย batch_id ที่ถูกต้อง
    mock_db.table.assert_called_with("batch_results")
    mock_db.table.return_value.select.assert_called_with("*")
    mock_db.table.return_value.select.return_value.eq.assert_called_with("batch_id", batch_id)
    
    # ตรวจสอบผลลัพธ์
    assert results == mock_results, "ผลลัพธ์ไม่ตรงกับที่คาดหวัง"
    assert len(results) == 2, f"จำนวนผลลัพธ์ไม่ถูกต้อง: คาดหวัง 2 แต่ได้ {len(results)}"
    
    # ตรวจสอบข้อมูลสำคัญ
    assert results[0]["student_name"] == "Alice", "ข้อมูลชื่อนักเรียนไม่ถูกต้อง"
    assert results[0]["score"] == 85, "ข้อมูลคะแนนไม่ถูกต้อง"
    assert results[1]["student_name"] == "Bob", "ข้อมูลชื่อนักเรียนไม่ถูกต้อง"
    assert results[1]["score"] == 70, "ข้อมูลคะแนนไม่ถูกต้อง"