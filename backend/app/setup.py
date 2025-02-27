from langsmith import expect
from pymilvus import MilvusClient
from app.infrastructure.rag.milvus_client import MilvusClient
from app.core.config import settings
import os

def setup_app():
    """
    เริ่มต้นตั้งค่าระบบ
    """
    print(f"Setting up {settings.PROJECT_NAME}...")
    
    # สร้างโฟลเดอร์สำหรับเก็บไฟล์อัปโหลด
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # ตั้งค่า Milvus
    try:
        client = MilvusClient()
    except Exception as e:
        print(f"Warning: Could not setup Milvus collection: {str(e)}")
        return client