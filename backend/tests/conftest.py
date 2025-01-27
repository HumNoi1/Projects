# tests/conftest.py
import pytest
import asyncio
from typing import Generator
import os
from dotenv import load_dotenv

def pytest_configure(config):
    """
    ตั้งค่าสภาพแวดล้อมสำหรับการทดสอบ
    """
    load_dotenv(".env.test", override=True)
    
    # Set default test values if not provided
    if not os.getenv("SUPABASE_URL"):
        os.environ["SUPABASE_URL"] = "https://test.supabase.co"
    if not os.getenv("SUPABASE_KEY"):
        os.environ["SUPABASE_KEY"] = "test-key"

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """สร้าง event loop สำหรับ async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(autouse=True)
async def setup_test_db():
    """เตรียมฐานข้อมูลสำหรับการทดสอบ"""
    # ตั้งค่าฐานข้อมูลสำหรับทดสอบ
    yield
    # ทำความสะอาดหลังการทดสอบ