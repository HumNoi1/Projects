from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class GradingCriteria(BaseModel):
    name: str
    description: str
    max_score: float
    weight: float = 1.0

class GradingResult(BaseModel):
    total_score: float
    criteria_scores: Dict[str, float]
    feedback: str
    confidence_score: float
    grading_time: datetime
    evaluator_id: str = Field(..., description="LLM model identifier")

class GradingRequest(BaseModel):
    student_answer_id: int
    reference_answer_id: int
    criteria: List[GradingCriteria]
    max_total_score: float = 100.0
    language: str = "th"