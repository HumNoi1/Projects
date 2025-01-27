# tests/test_api_endpoints.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.grading import GradingRequest, GradingCriteria

# สร้าง test client สำหรับทดสอบ API
client = TestClient(app)

def test_grade_endpoint():
    """ทดสอบ API endpoint สำหรับการตรวจให้คะแนน"""
    payload = GradingRequest(
        student_answer_id=1,
        reference_answer_id=1,
        criteria=[
            GradingCriteria(
                name="ความถูกต้อง",
                description="ความถูกต้องของเนื้อหา",
                max_score=10.0,
                weight=1.0
            )
        ],
        language="th"
    ).model_dump()

    try:
        response = client.post("/api/v1/grading/grade", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "total_score" in data
    except Exception as e:
        pytest.fail(f"API test failed: {str(e)}")