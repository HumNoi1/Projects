# backend/tests/test_api_endpoints.py
import pytest
from fastapi.testclient import TestClient
from main import app
from app.models.grading import GradingRequest
from unittest.mock import patch, AsyncMock

client = TestClient(app)

def test_grade_assignment_endpoint():
    # Test data
    test_data = {
        "student_answer": "This is a student answer",
        "reference_answer": "This is the reference answer",
        "rubric": {
            "Content": {
                "weight": 40,
                "criteria": "Evaluates understanding of concepts"
            },
            "Clarity": {
                "weight": 30,
                "criteria": "Clear expression of ideas"
            }
        }
    }
    
    # Mock the grading service
    with patch('app.api.v1.endpoints.grading.grading_service.grade_assignment') as mock_grade:
        mock_grade.return_value = {
            "success": True,
            "grading_result": {
                "score": 85,
                "feedback": "Good answer",
                "areas_for_improvement": ["Could add more detail"]
            }
        }
        
        # Make request
        response = client.post("/api/v1/grading/grade/", json=test_data)
        
        # Verify
        assert response.status_code == 200
        assert response.json() == {
            "success": True,
            "grading_result": {
                "score": 85,
                "feedback": "Good answer",
                "areas_for_improvement": ["Could add more detail"]
            }
        }
        
        mock_grade.assert_called_once()