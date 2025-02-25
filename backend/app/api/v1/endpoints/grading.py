# backend/app/api/v1/endpoints/grading.py
import tempfile
import json
from fastapi import APIRouter, HTTPException, Path, UploadFile, File, Form, Depends, logger
from app.models.grading import GradingRequest, GradingResponse
from app.services.grading_service import GradingService
from app.services.pdf_service import PDFService

router = APIRouter()
grading_service = GradingService()
pdf_service = PDFService()

@router.post("/grade-pdf/", response_model=GradingResponse)
async def grade_from_pdf(
    teacher_file: UploadFile = File(...),
    student_file: UploadFile = File(...),
    rubric: str = Form(...)  # รับ JSON string
):
    try:
        # อ่านข้อมูลไฟล์
        teacher_content = await teacher_file.read()
        student_content = await student_file.read()
        
        # บันทึกไฟล์ชั่วคราว
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as teacher_temp, \
             tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as student_temp:
            
            teacher_temp.write(teacher_content)
            student_temp.write(student_content)
            
            # สกัดข้อความจาก PDF
            teacher_pages = await pdf_service.extract_text(Path(teacher_temp.name))
            student_pages = await pdf_service.extract_text(Path(student_temp.name))
            
            # รวมเนื้อหาจากทุกหน้า
            teacher_text = "\n".join(page["content"] for page in teacher_pages)
            student_text = "\n".join(page["content"] for page in student_pages)
            
            # แปลง rubric จาก string เป็น JSON
            rubric_json = json.loads(rubric)
            
            # ให้คะแนน
            result = await grading_service.grade_assignment(
                student_answer=student_text,
                reference_answer=teacher_text,
                rubric=rubric_json
            )
            
            return result
                
    except Exception as e:
        logger.error(f"Error grading from PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))