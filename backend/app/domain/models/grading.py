from pydantic import BaseModel
from typing import List, Optional

class GradingRequest(BaseModel):
    student_id: str

class GradingResponse(BaseModel):
    assignment_id: str
    student_id: str
    score: int
    feedback: str
    strengths: List[str] = []
    areas_for_improvement: List[str] = []
    missed_concepts: List[str] = []

class GradingSimilarity(BaseModel):
    teacher_text: str
    student_text: str
    similarity: float
    
class BatchGradingRequest(BaseModel):
    student_id: List[str]
    
class BatchGradingResponse(BaseModel):
    batch_id: str
    assignment_id: str
    completed: bool
    results: List[GradingResponse] = []