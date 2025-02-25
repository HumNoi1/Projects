# backend/app/api/v1/endpoints/batch_grading.py
import tempfile
import json
import uuid
from pathlib import Path
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends, BackgroundTasks
from pydantic import BaseModel
import logging

from app.services.grading_service import GradingService, GradingServiceError
from app.services.pdf_service import PDFService
from app.models.grading import GradingResponse
from app.db.session import get_supabase

router = APIRouter()
grading_service = GradingService()
pdf_service = PDFService()
logger = logging.getLogger(__name__)

# ใช้เก็บสถานะของการตรวจงานแบบกลุ่ม
batch_status = {}

class StudentFileIds(BaseModel):
    student_file_ids: List[str]

class BatchResult(BaseModel):
    success: bool
    batch_id: str

@router.post("/", response_model=BatchResult)
async def create_batch_grading(
    teacher_file: UploadFile = File(...),
    assignment_id: str = Form(...)
):
    """
    เริ่มการตรวจงานแบบกลุ่มโดยอัปโหลดไฟล์อาจารย์
    """
    try:
        # สร้าง batch_id เป็น UUID
        batch_id = str(uuid.uuid4())
        
        # อ่านข้อมูลไฟล์
        teacher_content = await teacher_file.read()
        
        # บันทึกไฟล์ชั่วคราว
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as teacher_temp:
            teacher_temp.write(teacher_content)
            
            # สกัดข้อความจาก PDF
            teacher_pages = await pdf_service.extract_text(Path(teacher_temp.name))
            
            # รวมเนื้อหาจากทุกหน้า
            teacher_text = "\n".join(page["content"] for page in teacher_pages)
            
            # เก็บข้อมูลใน batch_status
            batch_status[batch_id] = {
                'teacher_text': teacher_text,
                'assignment_id': assignment_id,
                'student_files': [],
                'status': 'created',
                'results': {}
            }
            
            return {"success": True, "batch_id": batch_id}
                
    except Exception as e:
        logger.error(f"Error creating batch grading: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{batch_id}/students", response_model=dict)
async def assign_students_to_batch(
    batch_id: str,
    student_data: StudentFileIds,
    background_tasks: BackgroundTasks,
    supabase = Depends(get_supabase)
):
    """
    กำหนดรายการไฟล์นักเรียนที่ต้องการตรวจ
    """
    if batch_id not in batch_status:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    try:
        # เก็บ ID ไฟล์นักเรียน
        batch_status[batch_id]['student_files'] = student_data.student_file_ids
        batch_status[batch_id]['status'] = 'processing'
        
        # เริ่มกระบวนการตรวจงานในเบื้องหลัง
        background_tasks.add_task(
            process_batch_grading,
            batch_id,
            student_data.student_file_ids,
            supabase.client
        )
        
        return {"success": True, "message": "Students assigned to batch"}
                
    except Exception as e:
        logger.error(f"Error assigning students to batch: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{batch_id}/status", response_model=dict)
async def get_batch_status(batch_id: str):
    """
    ตรวจสอบสถานะการตรวจงานแบบกลุ่ม
    """
    if batch_id not in batch_status:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    return {
        "batch_id": batch_id,
        "status": batch_status[batch_id]['status'],
        "total": len(batch_status[batch_id]['student_files']),
        "completed": len(batch_status[batch_id]['results'])
    }

@router.get("/{batch_id}/results", response_model=Dict[str, Any])
async def get_batch_results(batch_id: str):
    """
    ดึงผลการตรวจงานแบบกลุ่ม
    """
    if batch_id not in batch_status:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    if batch_status[batch_id]['status'] != 'completed':
        return {
            "batch_id": batch_id,
            "status": batch_status[batch_id]['status'],
            "results": batch_status[batch_id]['results']
        }
    
    return {
        "batch_id": batch_id,
        "status": "completed",
        "results": batch_status[batch_id]['results']
    }

async def process_batch_grading(batch_id: str, student_file_ids: List[str], supabase_client):
    """
    กระบวนการตรวจงานในเบื้องหลัง
    """
    teacher_text = batch_status[batch_id]['teacher_text']
    assignment_id = batch_status[batch_id]['assignment_id']
    
    try:
        # ดึงข้อมูลไฟล์นักเรียนจาก Supabase
        response = supabase_client.table('files').select('*').in_('id', student_file_ids).execute()
        
        if hasattr(response, 'error') and response.error:
            raise Exception(f"Supabase error: {response.error}")
            
        student_files = response.data
        
        # สร้าง rubric ตัวอย่าง (ในระบบจริงอาจดึงจากฐานข้อมูล)
        sample_rubric = {
            "Content": {
                "weight": 40,
                "criteria": "Evaluates understanding of concepts"
            },
            "Clarity": {
                "weight": 30,
                "criteria": "Clear expression of ideas"
            },
            "Organization": {
                "weight": 20,
                "criteria": "Structured presentation of information"
            },
            "Grammar": {
                "weight": 10,
                "criteria": "Correct grammar and spelling"
            }
        }
        
        # ตรวจงานแต่ละไฟล์
        for student_file in student_files:
            try:
                # ในระบบจริงควรดึงเนื้อหาจากไฟล์
                # แต่ในตัวอย่างนี้เราจะสร้างข้อมูลตัวอย่าง
                student_text = f"Sample student answer for {student_file['file_name']}"
                
                # ส่งให้ grading service
                result = await grading_service.grade_assignment(
                    student_answer=student_text,
                    reference_answer=teacher_text,
                    rubric=sample_rubric
                )
                
                # จัดเก็บผลลัพธ์
                batch_status[batch_id]['results'][student_file['id']] = {
                    'student_id': student_file.get('student_id', 'unknown'),
                    'student_name': student_file.get('student_name', 'Unknown'),
                    'file_name': student_file['file_name'],
                    'score': 85,  # สมมติคะแนน
                    'feedback': "This is sample feedback from LLM.",
                    'graded_at': student_file['created_at'],
                    'rubric_scores': {
                        "Content": 85,
                        "Clarity": 80,
                        "Organization": 90,
                        "Grammar": 95
                    }
                }
                
            except Exception as e:
                logger.error(f"Error grading student file {student_file['id']}: {str(e)}")
                # เก็บข้อผิดพลาด
                batch_status[batch_id]['results'][student_file['id']] = {
                    'student_id': student_file.get('student_id', 'unknown'),
                    'student_name': student_file.get('student_name', 'Unknown'),
                    'file_name': student_file['file_name'],
                    'error': str(e)
                }
                
        # อัปเดตสถานะ
        batch_status[batch_id]['status'] = 'completed'
        
    except Exception as e:
        logger.error(f"Error processing batch grading: {str(e)}")
        # อัปเดตสถานะเป็นข้อผิดพลาด
        batch_status[batch_id]['status'] = 'error'
        batch_status[batch_id]['error'] = str(e)