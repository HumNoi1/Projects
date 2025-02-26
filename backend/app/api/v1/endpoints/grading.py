from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from app.infrastructure.database.database import get_db
from app.domain.services.grading_service import GradingService
from app.domain.models.grading import GradingRequest, GradingResponse
from typing import Optional

router = APIRouter()

@router.post("/{assignment_id}")
async def grade_submission(
    assignment_id: str,
    grading_request: GradingRequest,
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    """
    Grade a student submission for a specific assignment.
    """
    grading_service = GradingService(db)
    
    try:
        # Get teacher's answer key
        teacher_file = await grading_service.get_teacher_file(assignment_id)
        if not teacher_file:
            raise HTTPException(status_code=404, detail="Teacher answer key not found")
        
        # Get student submission
        student_file = await grading_service.get_student_file(
            assignment_id, 
            grading_request.student_id
        )
        if not student_file:
            raise HTTPException(status_code=404, detail="Student submission not found")
        
        # Perform grading (this can be time-consuming, so do it in background)
        result = await grading_service.grade_submission(
            teacher_file["text_content"],
            student_file["text_content"],
            assignment_id,
            grading_request.student_id
        )
        
        # Store grading result in database
        background_tasks.add_task(
            grading_service.store_grading_result,
            assignment_id=assignment_id,
            student_id=grading_request.student_id,
            score=result["score"],
            feedback=result["feedback"],
            strengths=result.get("strengths", []),
            improvements=result.get("areas_for_improvement", []),
            missed_concepts=result.get("missed_concepts", [])
        )
        
        return GradingResponse(
            assignment_id=assignment_id,
            student_id=grading_request.student_id,
            score=result["score"],
            feedback=result["feedback"],
            strengths=result.get("strengths", []),
            areas_for_improvement=result.get("areas_for_improvement", []),
            missed_concepts=result.get("missed_concepts", [])
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Grading error: {str(e)}")