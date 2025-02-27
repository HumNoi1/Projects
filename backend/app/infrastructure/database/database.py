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
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def get_db():
    try:
        # ทดสอบการเชื่อมต่อ
        supabase.table('classes').select('*').limit(1).execute()
        return supabase
    except Exception as e:
        raise Exception(f"Database error: {str(e)})")