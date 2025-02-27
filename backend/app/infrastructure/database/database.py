# backend/app/infrastructure/database/database.py
from app.core.config import settings
import logging
from supabase import create_client, Client
from typing import Generator, Any, Dict

# ตรวจสอบและบันทึกค่าการตั้งค่า Supabase
logging.info(f"SUPABASE_URL config: {settings.SUPABASE_URL is not None}")
logging.info(f"SUPABASE_KEY config: {settings.SUPABASE_KEY is not None}")

# สร้าง Supabase client
try:
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise ValueError("Missing Supabase credentials. Check your .env file.")
    
    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    logging.info("Supabase client created successfully")
    
except Exception as e:
    logging.error(f"Supabase client creation error: {str(e)}")
    # ยกเว้นจะทำให้แอปเริ่มต้นไม่ได้ ใช้ดัมมี่ object แทน
    supabase = None

class Database:
    """Database adapter for Supabase"""
    
    def __init__(self):
        self.client = supabase
    
    async def execute(self, query: str, values: Dict[str, Any] = None) -> Any:
        """Execute query on Supabase"""
        try:
            if not self.client:
                raise ValueError("Supabase client not initialized")
                
            # แปลง SQL query เป็น Supabase operation (อย่างง่าย)
            if query.strip().upper().startswith("INSERT INTO"):
                # Extract table name from INSERT INTO query
                table_name = self._extract_table_name(query)
                result = self.client.table(table_name).insert(values).execute()
                return SupabaseResult(result)
            elif query.strip().upper().startswith("SELECT"):
                # ตัวอย่างการทำ SELECT query
                table_name = self._extract_table_name(query)
                result = self.client.table(table_name).select("*").execute()
                return SupabaseResult(result)
            else:
                raise ValueError(f"Unsupported query type: {query}")
                
        except Exception as e:
            logging.error(f"Database execution error: {str(e)}")
            raise
    
    def _extract_table_name(self, query: str) -> str:
        """Extract table name from SQL query (simple implementation)"""
        if "INTO" in query.upper():
            # INSERT INTO table_name ...
            parts = query.upper().split("INTO")[1].strip().split(" ")
            return parts[0].lower().strip('()')
        elif "FROM" in query.upper():
            # SELECT * FROM table_name ...
            parts = query.upper().split("FROM")[1].strip().split(" ")
            return parts[0].lower()
        else:
            # Default to 'files' table if can't parse
            return "files"

class SupabaseResult:
    """Wrapper for Supabase result to mimic SQLAlchemy result"""
    
    def __init__(self, result):
        self.result = result
        self.data = result.get('data', [])
    
    def fetchone(self):
        """Get first result"""
        if self.data and len(self.data) > 0:
            return self.data[0]
        return None
    
    def fetchall(self):
        """Get all results"""
        return self.data

def get_db() -> Generator:
    """Get database dependency"""
    db = Database()
    try:
        yield db
    finally:
        # No need to close Supabase client
        pass