# backend/tests/conftest.py
import pytest
import asyncio
from unittest.mock import patch

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_supabase():
    with patch('app.db.base.create_client') as mock:
        yield mock

@pytest.fixture
def mock_milvus():
    with patch('app.db.base.connections') as mock:
        yield mock