from fastapi import APIRouter, Depends
from app.infrastructure.database.database import get_db

router = APIRouter()

@router.get("")
async def health_check():
    """
    Health check endpoint for the API.
    """
    return {"status": "ok", "message": "Service is running"}

@router.get("/db")
async def db_health_check(db = Depends(get_db)):
    """
    Database connection health check.
    """
    try:
        # Simple query to check database connection
        db.execute("SELECT 1")
        return {"status": "ok", "message": "Database connection is healthy"}
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}