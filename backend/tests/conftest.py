# tests/conftest.py
import pytest
import asyncio
from typing import Generator

@pytest.fixture(scope="function")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """สร้าง event loop สำหรับแต่ละ test case

    เราใช้ scope="function" เพื่อให้แต่ละ test case มี event loop ของตัวเอง
    และมีการจัดการปิด loop อย่างถูกต้องหลังจากทดสอบเสร็จ
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()