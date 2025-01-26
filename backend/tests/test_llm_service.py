import pytest
import os
from dotenv import load_dotenv
from app.services.llm_service import LLMService

# โหลด environment variables สำหรับการทดสอบ
@pytest.fixture(autouse=True)
def setup_test_env():
    # หา path ของไฟล์ .env.test
    test_env_path = os.path.join(os.path.dirname(__file__), '../.env.test')
    load_dotenv(test_env_path)
    yield

@pytest.fixture
def llm_service():
    return LLMService()

@pytest.mark.asyncio
async def test_generate_response(llm_service):
    """
    ทดสอบการสร้างคำตอบจากโมเดล
    
    ทดสอบว่า:
    1. สามารถสร้างคำตอบได้
    2. คำตอบที่ได้เป็น string
    3. คำตอบมีความยาวมากกว่า 0
    """
    prompt = "What is artificial intelligence?"
    response = await llm_service.generate_response(prompt)
    assert isinstance(response, str)
    assert len(response) > 0

@pytest.mark.asyncio
async def test_grade_answer(llm_service):
    """
    ทดสอบการตรวจให้คะแนนคำตอบ
    
    ทดสอบว่า:
    1. สามารถตรวจและให้คะแนนได้
    2. ผลลัพธ์มีรูปแบบตามที่กำหนด
    3. มีข้อมูลครบถ้วนตามที่ต้องการ
    """
    reference = "AI is artificial intelligence"
    student = "AI means artificial intelligence"
    criteria = [{
        "name": "Accuracy",
        "max_score": 10,
        "weight": 1.0
    }]
    
    result = await llm_service.grade_answer(
        reference_answer=reference,
        student_answer=student,
        criteria=criteria
    )
    
    assert isinstance(result, dict)
    assert "total_score" in result
    assert "feedback" in result