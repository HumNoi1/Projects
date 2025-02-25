# app/api/v1/endpoints/document.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from pathlib import Path
import tempfile
import shutil
import logging
import json
from typing import List, Dict, Any, Optional
from app.services.document.processor import DocumentProcessor

router = APIRouter()
logger = logging.getLogger(__name__)
document_processor = DocumentProcessor()

@router.post("/upload/pdf/", response_model=Dict[str, Any])
async def upload_pdf(
    file: UploadFile = File(...),
    collection_name: Optional[str] = Form(None),
    metadata: Optional[str] = Form(None),
    background_tasks: BackgroundTasks = None
):
    """Upload and process a PDF document."""
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Create temporary file to store the upload
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        try:
            # Save uploaded file
            shutil.copyfileobj(file.file, temp_file)
            
            # Parse additional metadata
            additional_metadata = {}
            if metadata:
                try:
                    additional_metadata = json.loads(metadata)
                except json.JSONDecodeError:
                    raise HTTPException(
                        status_code=400,
                        detail="Invalid metadata JSON format"
                    )
            
            # Add original filename to metadata
            additional_metadata["original_filename"] = file.filename
            
            # Use default collection name based on file if not provided
            if not collection_name:
                collection_name = f"doc_{Path(file.filename).stem}"
            
            # Process PDF in background or foreground
            if background_tasks:
                result = {"status": "processing", "filename": file.filename}
                background_tasks.add_task(
                    document_processor.process_pdf,
                    Path(temp_file.name),
                    collection_name,
                    additional_metadata
                )
            else:
                # Process immediately and wait for result
                result = await document_processor.process_pdf(
                    Path(temp_file.name),
                    collection_name,
                    additional_metadata
                )
            
            return result

        except Exception as e:
            logger.error(f"Error processing uploaded PDF: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing PDF: {str(e)}"
            )
        finally:
            # Clean up temporary file (in case of immediate processing)
            if not background_tasks:
                Path(temp_file.name).unlink(missing_ok=True)

@router.post("/query/", response_model=Dict[str, Any])
async def query_document(
    query_text: str = Form(...),
    collection_name: Optional[str] = Form(None),
    similarity_top_k: int = Form(3)
):
    """Query document collection."""
    try:
        # Create LlamaIndex service and query
        llama_index_service = document_processor.llama_index_service
        
        result = await llama_index_service.query_index(
            query_text=query_text,
            collection_name=collection_name,
            similarity_top_k=similarity_top_k
        )
        
        return {
            "success": True,
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Error querying document: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error querying document: {str(e)}"
        )