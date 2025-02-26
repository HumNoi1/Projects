from app.infrastructure.rag.milvus_client import setup_milvus_collection
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
        collection = setup_milvus_collection()
        print(f"Milvus collection setup complete: {collection.name}")
    except Exception as e:
        print(f"Error setting up Milvus: {e}")
        print("You may need to start Milvus server first or check your connection settings.")
    
    print("Setup complete!")