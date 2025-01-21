from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class DocumentBase(BaseModel):
    title: str
    content: str
    document_type: str = Field(..., description="Type of document: answer/reference")
    language: str = Field(default="th", description="Document language")

class DocumentCreate(DocumentBase):
    class_id: int
    assignment_id: int
    created_by: int

class DocumentInDB(DocumentCreate):
    id: int
    created_at: datetime
    embedding_id: Optional[str] = None
    status: str = Field(default="pending", description="pending/processed/failed")