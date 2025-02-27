from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.api.v1.router import api_router
from app.core.config import settings
from app.setup import setup_app

# ตั้งค่า logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Grading LLM API",
    description="API for automated grading with LLM",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to Grading LLM API"}

@app.on_event("startup")
async def startup_event():
    """
    ทำงานเมื่อเริ่มต้นระบบ
    """
    logger.info("Starting up application...")
    try:
        # ตั้งค่าระบบ
        setup_app()
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        # ไม่หยุดการทำงานของระบบ แต่บันทึกข้อผิดพลาด