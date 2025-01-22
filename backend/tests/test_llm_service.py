import os
import pytest
from app.services.llm_service import LLMService

@pytest.fixture
def llm_service():
    return LLMService()

def test_model_file_exists(llm_service):
    model_path = "models/llama-3.2-typhoon2-3b-instruct-q4_k_m.gguf"
    assert os.path.exists(model_path), f"Model file not found at {model_path}. Please download the model first."

def test_llm_service_initialization(llm_service):
    assert llm_service is not None

def test_llm_service_error_handling():
    with pytest.raises(FileNotFoundError):
        LLMService()