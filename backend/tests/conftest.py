# tests/conftest.py
import pytest
import asyncio
from typing import Generator

@pytest.fixture(scope="function")
async def application_context():
    """Setup application context"""
    yield
    # teardown