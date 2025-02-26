from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, UploadFile, File, Form
from app.infrastructure.database.database import get_db
from app.domain.services.batch_grading_service import BatchGradingService
from app.domain.models.grading import BatchGradingRequest, BatchGradingResponse
from typing import List
import uuid

router = APIRouter()

@router.post("")
async def create_batch_grading(
    teacher_file: UploadFile = File(...),
    assignment_id: str = Form(...),
    db = Depends(get_db)
):
    """
    Start a new batch grading process by uploading teacher's answer key.
    """
    batch_grading_service = BatchGradingService(db)
    
    # Generate a batch ID
    batch_id = str(uuid.uuid4())
    
    # Process teacher file
    teacher_file_record = await batch_grading_service.process_teacher_file(
        teacher_file,
        assignment_id,
        batch_id
    )
    
    return {
        "success": True,
        "batch_id": batch_id,
        "message": "Batch grading initiated"
    }

@router.post("/{batch_id}/students")
async def add_students_to_batch(
    batch_id: str,
    student_file_ids: List[str],
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    """
    Add student submissions to a batch grading process.
    """
    batch_grading_service = BatchGradingService(db)
    
    # Queue the batch grading process
    background_tasks.add_task(
        batch_grading_service.process_batch,
        batch_id=batch_id,
        student_file_ids=student_file_ids
    )
    
    return {
        "success": True,
        "message": f"Processing {len(student_file_ids)} student submissions",
        "batch_id": batch_id
    }

@router.get("/{batch_id}/results")
async def get_batch_results(
    batch_id: str,
    db = Depends(get_db)
):
    """
    Get the results of a batch grading process.
    """
    batch_grading_service = BatchGradingService(db)
    results = await batch_grading_service.get_batch_results(batch_id)
    
    return {
        "batch_id": batch_id,
        "results": results,
        "completed": len(results) > 0
    }