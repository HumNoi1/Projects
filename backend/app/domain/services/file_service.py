import os
import uuid
from fastapi import UploadFile
from app.core.config import settings

class FileService:
    def __init__(self, db):
        self.db = db
    
    async def save_file(self, file: UploadFile, file_type: str, assignment_id: str) -> str:
        """
        Save uploaded file to local storage.
        """
        # Generate a unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # Create file path
        file_path = os.path.join(settings.UPLOAD_DIR, assignment_id, unique_filename)
        
        # Save the file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return file_path
    
    async def create_file_record(
        self, 
        file_name: str, 
        file_path: str, 
        file_type: str, 
        file_size: int, 
        mime_type: str, 
        assignment_id: str,
        text_content: str
    ):
        """
        Create a file record in the database.
        """
        bucket_name = "teacher_files" if file_type == "teacher" else "student_files"
        
        # Create record in Supabase
        data = {
            "file_name": file_name,
            "file_path": file_path,
            "file_type": file_type,
            "file_size": file_size,
            "mime_type": mime_type,
            "assignment_id": assignment_id,
            "text_content": text_content
        }
        
        result = self.db.table("files").insert(data).execute()
        
        return result.data[0] if result.data else None