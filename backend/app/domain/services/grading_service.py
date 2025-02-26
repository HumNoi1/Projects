from app.infrastructure.llm.chains import GradingChain
from app.infrastructure.rag.embeddings import EmbeddingService
from app.infrastructure.rag.milvus_client import MilvusClient
from typing import List, Dict, Any

class GradingService:
    def __init__(self, db):
        self.db = db
        self.grading_chain = GradingChain()
        self.embedding_service = EmbeddingService()
        self.milvus_client = MilvusClient()
    
    async def get_teacher_file(self, assignment_id: str):
        """
        Get teacher's answer key for an assignment.
        """
        result = self.db.table("files")\
            .select("*")\
            .eq("assignment_id", assignment_id)\
            .eq("file_type", "teacher")\
            .execute()
        
        return result.data[0] if result.data else None
    
    async def get_student_file(self, assignment_id: str, student_id: str):
        """
        Get student submission for an assignment.
        """
        result = self.db.table("files")\
            .select("*")\
            .eq("assignment_id", assignment_id)\
            .eq("student_id", student_id)\
            .eq("file_type", "student")\
            .execute()
        
        return result.data[0] if result.data else None
    
    async def grade_submission(
        self, 
        teacher_text: str, 
        student_text: str, 
        assignment_id: str,
        student_id: str
    ):
        """
        Grade a student submission using LLM.
        """
        # Use the grading chain to evaluate the submission
        grading_result = await self.grading_chain.grade_submission(
            teacher_text=teacher_text,
            student_text=student_text
        )
        
        return grading_result
    
    async def store_grading_result(
        self,
        assignment_id: str,
        student_id: str,
        score: int,
        feedback: str,
        strengths: List[str],
        improvements: List[str],
        missed_concepts: List[str]
    ):
        """
        Store grading result in the database.
        """
        data = {
            "assignment_id": assignment_id,
            "student_id": student_id,
            "score": score,
            "feedback": feedback,
            "strengths": strengths,
            "areas_for_improvement": improvements,
            "missed_concepts": missed_concepts
        }
        
        result = self.db.table("grading_results").insert(data).execute()
        
        return result.data[0] if result.data else None