from fastapi import FastAPI
import uvicorn
from app.api.v1.endpoints import grading, document
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# รวม router จาก endpoints ต่างๆ
app.include_router(grading.router, prefix=settings.API_V1_STR + "/grading", tags=["grading"])
app.include_router(document.router, prefix=settings.API_V1_STR + "/document", tags=["documents"])

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)