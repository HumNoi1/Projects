from datetime import date
import datetime
import stat
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from typing import List
from app.models.document import DocumentCreate, DocumentInDB
from app.services.document_processor import DocumentProcessor

router = APIRouter()
document_processor = DocumentProcessor()

@router.post("/upload/", response_model=DocumentInDB)
async def upload_document(
    file: UploadFile = File(...),
    class_id: int = None,
    assignment_id: int = None,
    document_type: str = None
):
    """
    Upload and process a document
    """
    try:
        # Read file content
        content = await file.read()
        content_text = content.decode("utf-8")
        
        # Create metadata
        metadata = {
            "filename": file.filename,
            "class_id": class_id,
            "assignment_id": assignment_id,
            "document_type": document_type
        }
        
        # Process document
        processed_chunks = await document_processor.process_document(
            content_text,
            metadata
        )
        
        # Here we'll add database storage logic later
        # For now, return the first chunk as a sample
        return {
            "id": 1,  # Temporary ID
            "title": file.filename,
            "content": processed_chunks[0].page_content,
            "document_type": document_type,
            "class_id": class_id,
            "assignment_id": assignment_id,
            "created_by": 1,  # Temporary user ID
            "created_at": "2024-01-21T00:00:00",  # Temporary timestamp
            "status": "processed"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/process/", response_model=List[DocumentInDB])
async def process_documents(document: DocumentCreate):
    """
    Process a list of documents
    """
    try:
        # Initialize services
        doc_processor = DocumentProcessor()
        
        # Process document and create embeddings
        result = await doc_processor.process_and_embed_documents(
            content=document.content,
            metadata={
                "document_id": document.id,
                "class_id": document.class_id,
                "assignment_id": document.assignment_id,
                "document_type": document.document_type
            }
        )
        
        # Update documents status
        document_db = DocumentInDB(
            **document.dict(),
            id=1, # Temporary ID
            created_at = datetime.now(),
            embedding_id = str(result["embedding_ids"][0]),
            status = "processed"
        )
        
        return [document_db]
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))