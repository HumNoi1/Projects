import pytest
import asyncio
from typing import Generator
import os
from dotenv import load_dotenv

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment variables."""
    # Load test environment variables
    load_dotenv(".env.test", override=True)
    
    # Set testing configurations
    os.environ["LMSTUDIO_API_BASE"] = "http://localhost:1234/v1"
    os.environ["LLM_TEMPERATURE"] = "0.7"
    os.environ["LLM_TOP_P"] = "0.95"
    os.environ["LLM_MAX_TOKENS"] = "2048"
    
    yield
    
    # Cleanup after tests
    for key in ["LMSTUDIO_API_BASE", "LLM_TEMPERATURE", "LLM_TOP_P", "LLM_MAX_TOKENS"]:
        if key in os.environ:
            del os.environ[key]