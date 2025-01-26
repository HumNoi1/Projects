# tests/conftest.py
import pytest
import asyncio
from typing import Generator
import os
from dotenv import load_dotenv

@pytest.fixture(scope="function")
async def application_context():
    """Setup application context"""
    yield
    # teardown

@pytest.fixture(autouse=True)
def setup_test_env():
    # โหลด environment variables สำหรับการทดสอบ
    load_dotenv(".env.test")
    
    # ตั้งค่า token สำหรับการทดสอบ
    os.environ["HUGGINGFACE_TOKEN"] = "test_token"
    
    yield
    
    # ล้างค่าหลังจากทดสอบเสร็จ
    if "HUGGINGFACE_TOKEN" in os.environ:
        del os.environ["HUGGINGFACE_TOKEN"]