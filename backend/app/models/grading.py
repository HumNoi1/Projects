from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class GradingCriteria(BaseModel):
    """กำหนดเกณฑ์การให้คะแนนแต่ละข้อ"""
    name: str = Field(..., description="ชื่อเกณฑ์การให้คะแนน")
    description: str = Field(..., description="คำอธิบายรายละเอียดของเกณฑ์")
    max_score: float = Field(..., gt=0, description="คะแนนเต็มของเกณฑ์นี้")
    weight: float = Field(1.0, gt=0, le=1.0, description="น้ำหนักคะแนนของเกณฑ์นี้")

class GradingResult(BaseModel):
    """ผลลัพธ์การตรวจให้คะแนน"""
    total_score: float = Field(..., ge=0, description="คะแนนรวมทั้งหมด")
    criteria_scores: Dict[str, float] = Field(..., description="คะแนนแยกตามเกณฑ์แต่ละข้อ")
    feedback: str = Field(..., min_length=10, description="คำแนะนำและข้อเสนอแนะ")
    confidence_score: float = Field(..., ge=0, le=1, description="ระดับความมั่นใจในการตรวจ")
    grading_time: datetime = Field(default_factory=datetime.now, description="เวลาที่ตรวจ")
    evaluator_id: str = Field(..., description="รหัสของ LLM model ที่ใช้ตรวจ")

class GradingStatusEnum(str, Enum):
    """สถานะของการตรวจให้คะแนน"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class GradingStatus(BaseModel):
    """ข้อมูลสถานะการตรวจให้คะแนน"""
    answer_id: str = Field(..., description="รหัสคำตอบที่กำลังตรวจ")
    status: GradingStatusEnum = Field(
        default=GradingStatusEnum.PENDING,
        description="สถานะปัจจุบันของการตรวจ"
    )
    created_at: datetime = Field(default_factory=datetime.now, description="เวลาที่เริ่มตรวจ")
    updated_at: Optional[datetime] = Field(None, description="เวลาที่อัพเดทสถานะล่าสุด")
    error: Optional[str] = Field(None, description="ข้อความแสดงข้อผิดพลาด (ถ้ามี)")

    @field_validator('error')
    @classmethod
    def error_only_on_failed(cls, v: Optional[str], info) -> Optional[str]:
        """ตรวจสอบว่าจะมี error message เฉพาะเมื่อสถานะเป็น FAILED เท่านั้น"""
        status = info.data.get('status')
        if v is not None and status != GradingStatusEnum.FAILED:
            raise ValueError("error message ควรมีเฉพาะเมื่อสถานะเป็น 'failed'")
        return v

class BatchAnswerItem(BaseModel):
    """ข้อมูลคำตอบแต่ละชิ้นในการตรวจแบบ batch"""
    id: str = Field(..., description="รหัสเฉพาะของคำตอบ")
    content: str = Field(..., description="เนื้อหาคำตอบที่ต้องการตรวจ")

class GradingRequest(BaseModel):
    """คำขอสำหรับการตรวจให้คะแนน"""
    reference_answer: str = Field(..., description="คำตอบอ้างอิงที่ถูกต้อง")
    student_answer: str = Field(..., description="คำตอบของนักเรียนที่ต้องการตรวจ")
    criteria: List[GradingCriteria] = Field(..., min_length=1, description="เกณฑ์การให้คะแนน")
    language: str = Field(default="th", description="ภาษาที่ต้องการใช้ในการให้ feedback")

    @field_validator('criteria')
    @classmethod
    def validate_criteria_weights(cls, v: List[GradingCriteria]) -> List[GradingCriteria]:
        """ตรวจสอบว่าน้ำหนักคะแนนรวมกันได้ 1.0"""
        total_weight = sum(criterion.weight for criterion in v)
        if not 0.99 <= total_weight <= 1.01:  # ยอมให้มีความคลาดเคลื่อนเล็กน้อย
            raise ValueError(f"น้ำหนักคะแนนรวมกันต้องได้ 1.0 แต่ได้ {total_weight}")
        return v

class BatchGradingRequest(BaseModel):
    """คำขอสำหรับการตรวจให้คะแนนแบบ batch"""
    reference_answer: str = Field(..., description="คำตอบอ้างอิงที่ถูกต้อง")
    answers: List[BatchAnswerItem] = Field(..., description="รายการคำตอบที่ต้องการตรวจ")
    criteria: List[GradingCriteria] = Field(..., min_length=1, description="เกณฑ์การให้คะแนน")
    language: str = Field(default="th", description="ภาษาที่ต้องการใช้ในการให้ feedback")