# backend/app/api/v1/endpoints/grading.py
from fastapi import APIRouter, HTTPException, Depends
from app.models.grading import GradingRequest, GradingResponse
from app.services.grading_service import GradingService

router = APIRouter()
grading_service = GradingService()

@router.post("/grade/", response_model=GradingResponse)
async def grade_assignment(request: GradingRequest):
    try:
        result = await grading_service.grade_assignment(
            student_answer=request.student_answer,
            reference_answer=request.reference_answer,
            rubric=request.rubric
        )
        return result
    except Exception as e:
        # บันทึก error message ใน log
        import logging, traceback
        logging.error(f"Grading error: {str(e)}")
        logging.error(traceback.format_exc())
        
        # คืนค่า error อย่างปลอดภัย
        return {
            "success": False,
            "grading_result": {
                "error": f"Error occurred: {str(e)}",
                "message": "Please check server logs for details"
            }
        }
        
@router.post("/test/")
async def test_endpoint():
    return {"success": True, "message": "Test endpoint works"}