# backend/app/domain/services/file_service.py
import os
import uuid
from datetime import datetime
import logging

class FileService:
    def __init__(self, db):
        self.db = db
        
    async def save_file(self, file, file_type, assignment_id):
        """Save uploaded file to disk"""
        # Create unique filename
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        
        # Create directory path
        upload_path = os.path.join("uploads", assignment_id, file_type)
        os.makedirs(upload_path, exist_ok=True)
        
        # Create file path
        file_path = os.path.join(upload_path, unique_filename)
        
        # Write file to disk
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
            
        return file_path
    
    async def create_file_record(self, file_name, file_path, file_type, file_size, 
                             mime_type, assignment_id, text_content):
        """Create a record of the uploaded file in Supabase"""
        try:
            # Extract student_id from filename if it's a student submission
            student_id = None
            if file_type == "student":
                student_id = file_name.split('_')[0] if '_' in file_name else "unknown"
            
            # Create file record in database using Supabase
            file_data = {
                "file_name": file_name,
                "file_path": file_path,
                "file_type": file_type,
                "file_size": file_size,
                "mime_type": mime_type,
                "assignment_id": assignment_id,
                "student_id": student_id,
                "text_content": text_content,
                "created_at": datetime.now().isoformat()
            }
            
            result = await self.db.execute("INSERT INTO files", file_data)
            return result.data[0] if result.data else {}
            
        except Exception as e:
            logging.error(f"Database error: {str(e)}")
            raise Exception(f"Failed to create file record: {str(e)}")