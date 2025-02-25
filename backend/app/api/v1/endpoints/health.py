# app/api/v1/endpoints/health.py
from fastapi import APIRouter
import httpx
from pymilvus import utility
from app.core.config import settings
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=dict)
async def health_check():
    """Basic health check endpoint."""
    return {"status": "ok", "message": "API is running"}

@router.get("/debug", response_model=dict)
async def debug_connections():
    """Debug connections to external services."""
    results = {
        "api": "ok",
        "milvus": "not_tested",
        "lmstudio": "not_tested"
    }
    
    # Test Milvus connection
    try:
        is_connected = utility.has_collection("test_connection")
        results["milvus"] = "ok"
    except Exception as e:
        results["milvus"] = f"error: {str(e)}"
        
    # Test LM-Studio connection
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{settings.LMSTUDIO_API_BASE}/v1/models")
            if response.status_code == 200:
                results["lmstudio"] = "ok"
            else:
                results["lmstudio"] = f"error: status {response.status_code}"
    except Exception as e:
        results["lmstudio"] = f"error: {str(e)}"
        
    return results