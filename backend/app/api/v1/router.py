# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.endpoints import grading, document, health

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(document.router, prefix="/document", tags=["document"])
api_router.include_router(grading.router, prefix="/grading", tags=["grading"])