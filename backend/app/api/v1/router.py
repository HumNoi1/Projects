from fastapi import APIRouter
from app.api.v1.endpoints import health, files, grading, batch_grading

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
api_router.include_router(grading.router, prefix="/grading", tags=["grading"])
api_router.include_router(batch_grading.router, prefix="/batch-grading", tags=["batch-grading"])