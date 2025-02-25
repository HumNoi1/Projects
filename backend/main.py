# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.api.v1.endpoints import grading, document, health, batch_grading
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# ตั้งค่า CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL ของ Frontend (อาจเปลี่ยนในสภาพแวดล้อมจริง)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# รวม router จาก endpoints ต่างๆ
app.include_router(grading.router, prefix=settings.API_V1_STR + "/grading", tags=["grading"])
app.include_router(document.router, prefix=settings.API_V1_STR + "/document", tags=["documents"])
app.include_router(health.router, prefix=settings.API_V1_STR + "/health", tags=["health"])
app.include_router(batch_grading.router, prefix=settings.API_V1_STR + "/batch-grading", tags=["batch-grading"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # เปลี่ยนเป็น 0.0.0.0 เพื่อให้เข้าถึงได้จากภายนอก