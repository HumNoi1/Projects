# backend/app/api/v1/endpoints/health.py
from fastapi import APIRouter
from app.core.config import settings
import httpx

router = APIRouter()

@router.get("/", response_model=dict)
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "API is running"}

@router.get("/debug", response_model=dict)
async def debug_connections():
    """Debug connections to external services"""
    results = {
        "api": "ok",
        "supabase": "not_tested",
        "milvus": "not_tested",
        "lmstudio": "not_tested"
    }
    
    # ทดสอบ LM-Studio
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