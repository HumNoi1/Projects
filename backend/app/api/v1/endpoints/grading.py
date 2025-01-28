from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Optional
from datetime import datetime
import logging

from app.models.grading import (
    GradingRequest,
    GradingResult,
    GradingCriteria,
    BatchGradingRequest,
    GradingStatus
)
from app.services.grading_service import GradingService
from app.services.document_processor import DocumentProcessor
from app.db.session import get_supabase

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/grade/", response_model=GradingResult)
async def grade_single_answer(
    request: GradingRequest,
    grading_service: GradingService = Depends(lambda: GradingService())
):
    """
    ตรวจให้คะแนนคำตอบเดี่ยว และส่งผลลัพธ์กลับทันที
    
    endpoint นี้เหมาะสำหรับการตรวจคำตอบสั้นๆ ที่ต้องการผลลัพธ์ทันที
    """
    try:
        result = await grading_service.grade_answer(
            reference_answer=request.reference_answer,
            student_answer=request.student_answer,
            criteria=request.criteria,
            language=request.language
        )
        
        # ตรวจสอบความมั่นใจในผลการตรวจ
        if not await grading_service.evaluate_grading_confidence(result):
            logger.warning("Low confidence in grading result")
            
        return result
        
    except Exception as e:
        logger.error(f"Error in grade_single_answer: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Grading failed: {str(e)}"
        )

@router.post("/batch-grade/", response_model=List[GradingStatus])
async def start_batch_grading(
    request: BatchGradingRequest,
    background_tasks: BackgroundTasks,
    grading_service: GradingService = Depends(lambda: GradingService()),
    supabase = Depends(get_supabase)
):
    """
    เริ่มกระบวนการตรวจคำตอบแบบ batch 
    
    สำหรับการตรวจคำตอบจำนวนมาก จะทำงานแบบ asynchronous และส่งผลลัพธ์ไปเก็บใน database
    """
    try:
        # สร้าง grading tasks และบันทึกสถานะเริ่มต้น
        task_statuses = []
        for answer in request.answers:
            task_status = GradingStatus(
                answer_id=answer.id,
                status="pending",
                created_at=datetime.now()
            )
            
            # บันทึกสถานะลง Supabase
            await supabase.table("grading_tasks").insert(
                task_status.dict()
            ).execute()
            
            task_statuses.append(task_status)
            
            # เพิ่ม task เข้า background queue
            background_tasks.add_task(
                process_single_answer,
                answer.id,
                request.reference_answer,
                answer.content,
                request.criteria,
                grading_service,
                supabase
            )
            
        return task_statuses
        
    except Exception as e:
        logger.error(f"Error starting batch grading: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start batch grading: {str(e)}"
        )

@router.get("/status/{task_id}", response_model=GradingStatus)
async def get_grading_status(
    task_id: str,
    supabase = Depends(get_supabase)
):
    """
    ตรวจสอบสถานะของการตรวจคำตอบ
    """
    try:
        response = await supabase.table("grading_tasks").select("*").eq(
            "id", task_id
        ).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=404,
                detail=f"Grading task {task_id} not found"
            )
            
        return GradingStatus(**response.data[0])
        
    except Exception as e:
        logger.error(f"Error getting grading status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get grading status: {str(e)}"
        )

@router.get("/history/", response_model=List[GradingResult])
async def get_grading_history(
    answer_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    supabase = Depends(get_supabase)
):
    """
    ดึงประวัติการตรวจคำตอบตามเงื่อนไขที่กำหนด
    """
    try:
        query = supabase.table("grading_results").select("*")
        
        if answer_id:
            query = query.eq("answer_id", answer_id)
        if start_date:
            query = query.gte("created_at", start_date)
        if end_date:
            query = query.lte("created_at", end_date)
            
        response = await query.execute()
        return [GradingResult(**result) for result in response.data]
        
    except Exception as e:
        logger.error(f"Error fetching grading history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch grading history: {str(e)}"
        )

async def process_single_answer(
    answer_id: str,
    reference_answer: str,
    student_answer: str,
    criteria: List[GradingCriteria],
    grading_service: GradingService,
    supabase
):
    """
    ฟังก์ชันสำหรับประมวลผลการตรวจคำตอบแต่ละชิ้นใน background
    """
    try:
        # อัพเดทสถานะเป็น processing
        await supabase.table("grading_tasks").update({
            "status": "processing",
            "updated_at": datetime.now()
        }).eq("answer_id", answer_id).execute()
        
        # ดำเนินการตรวจ
        result = await grading_service.grade_answer(
            reference_answer=reference_answer,
            student_answer=student_answer,
            criteria=criteria
        )
        
        # บันทึกผลการตรวจ
        await supabase.table("grading_results").insert(
            {**result.dict(), "answer_id": answer_id}
        ).execute()
        
        # อัพเดทสถานะเป็น completed
        await supabase.table("grading_tasks").update({
            "status": "completed",
            "updated_at": datetime.now()
        }).eq("answer_id", answer_id).execute()
        
    except Exception as e:
        logger.error(f"Error processing answer {answer_id}: {str(e)}")
        # อัพเดทสถานะเป็น failed
        await supabase.table("grading_tasks").update({
            "status": "failed",
            "error": str(e),
            "updated_at": datetime.now()
        }).eq("answer_id", answer_id).execute()