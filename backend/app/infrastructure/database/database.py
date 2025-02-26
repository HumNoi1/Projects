from supabase import create_client
from app.core.config import settings
from fastapi import Depends

# สร้างแบบมีการจัดการข้อผิดพลาด
def get_supabase_client():
    try:
        # ถ้าไม่มีค่า URL หรือ KEY ให้คืนค่า None
        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            print("Warning: SUPABASE_URL or SUPABASE_KEY not set")
            return None
            
        # สร้าง client โดยไม่ใช้พารามิเตอร์เพิ่มเติม
        return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    except Exception as e:
        print(f"Error creating Supabase client: {e}")
        return None

# ตัวแปร global สำหรับเก็บ client
supabase = get_supabase_client()

def get_db():
    """
    Dependency function สำหรับดึง Supabase client
    เพื่อใช้ในเส้นทาง API
    """
    if supabase is None:
        # Mock client สำหรับการพัฒนา - สามารถปรับเปลี่ยนตามความต้องการ
        class MockSupabaseClient:
            def table(self, table_name):
                return self
                
            def select(self, *args):
                return self
                
            def eq(self, *args):
                return self
                
            def execute(self):
                return MockResponse()
                
            def insert(self, data):
                print(f"MOCK: Would insert {data}")
                return self
        
        class MockResponse:
            data = []
        
        print("Warning: Using MockSupabaseClient for development")
        return MockSupabaseClient()
    
    return supabase