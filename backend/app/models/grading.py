# app/models/grading.py
from typing import Dict, Any
from .base import BaseSchema

class GradingRequest(BaseSchema):
    student_answer: str
    reference_answer: str
    rubric: Dict[str, Any]

class GradingResponse(BaseSchema):
    success: bool
    grading_result: Dict[str, Any]