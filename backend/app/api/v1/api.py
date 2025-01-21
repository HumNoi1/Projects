from fastapi import APIRouter
from backend.app.api.v1.endpoints import documents, grading

api_router = APIRouter()
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(grading.router, prefix="/grading", tags=["grading"])