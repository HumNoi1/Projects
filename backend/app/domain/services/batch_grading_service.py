from app.domain.services.file_service import FileService
from app.domain.services.grading_service import GradingService
from fastapi import UploadFile
from typing import List, Dict, Any
import asyncio

class BatchGradingService:
    def __init__(self, db):
        self.db = db
        self.file_service = FileService(db)
        self.grading_service = GradingService(db)
    
    async def process_teacher_file(
        self,
        teacher_file: UploadFile,
        assignment_id: str,
        batch_id: str
    ):
        """
        Process and store the teacher's answer key.
        """
        # Save the file
        file_path = await self.file_service.save_file(
            teacher_file,
            "teacher",
            assignment_id
        )
        
        # Extract text content
        from app.utils.pdf_processor import extract_text_from_pdf
        text_content = extract_text_from_pdf(file_path)
        
        # Create file record
        file_record = await self.file_service.create_file_record(
            file_name=teacher_file.filename,
            file_path=file_path,
            file_type="teacher",
            file_size=0,  # Will be updated after saving
            mime_type=teacher_file.content_type,
            assignment_id=assignment_id,
            text_content=text_content
        )
        
        # Create batch record
        batch_data = {
            "id": batch_id,
            "assignment_id": assignment_id,
            "teacher_file_id": file_record["id"],
            "status": "created",
            "created_at": "now()"
        }
        
        self.db.table("batch_grading").insert(batch_data).execute()
        
        return file_record
    
    async def process_batch(self, batch_id: str, student_file_ids: List[str]):
        """
        Process a batch of student submissions.
        """
        # Get batch info
        batch_info = self.db.table("batch_grading")\
            .select("*")\
            .eq("id", batch_id)\
            .execute()\
            .data[0]
            
        if not batch_info:
            raise ValueError(f"Batch {batch_id} not found")
        
        # Update batch status
        self.db.table("batch_grading")\
            .update({"status": "processing"})\
            .eq("id", batch_id)\
            .execute()
        
        # Get teacher file
        teacher_file = self.db.table("files")\
            .select("*")\
            .eq("id", batch_info["teacher_file_id"])\
            .execute()\
            .data[0]
            
        if not teacher_file:
            raise ValueError("Teacher file not found")
        
        # Process each student submission
        for student_file_id in student_file_ids:
            # Get student file
            student_file = self.db.table("files")\
                .select("*")\
                .eq("id", student_file_id)\
                .execute()\
                .data[0]
                
            if not student_file:
                continue
            
            try:
                # Grade the submission
                result = await self.grading_service.grade_submission(
                    teacher_text=teacher_file["text_content"],
                    student_text=student_file["text_content"],
                    assignment_id=batch_info["assignment_id"],
                    student_id=student_file["student_id"]
                )
                
                # Store the result
                result_data = {
                    "batch_id": batch_id,
                    "student_file_id": student_file_id,
                    "student_id": student_file["student_id"],
                    "score": result["score"],
                    "feedback": result["feedback"],
                    "strengths": result.get("strengths", []),
                    "areas_for_improvement": result.get("areas_for_improvement", []),
                    "missed_concepts": result.get("missed_concepts", []),
                    "status": "completed",
                    "graded_at": "now()"
                }
                
                self.db.table("batch_results").insert(result_data).execute()
                
            except Exception as e:
                print(f"Error processing student {student_file_id}: {str(e)}")
                # Record the error
                error_data = {
                    "batch_id": batch_id,
                    "student_file_id": student_file_id,
                    "student_id": student_file.get("student_id"),
                    "status": "error",
                    "error_message": str(e)
                }
                
                self.db.table("batch_results").insert(error_data).execute()
        
        # Update batch status
        self.db.table("batch_grading")\
            .update({"status": "completed", "completed_at": "now()"})\
            .eq("id", batch_id)\
            .execute()
    
    async def get_batch_results(self, batch_id: str):
        """
        Get the results of a batch grading process.
        """
        results = self.db.table("batch_results")\
            .select("*")\
            .eq("batch_id", batch_id)\
            .execute()\
            .data
            
        return results