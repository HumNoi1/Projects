from setuptools import setup, find_packages

setup(
    name="app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.103.0",
        "uvicorn>=0.23.2",
        "python-dotenv>=1.0.0",
        "pydantic>=2.3.0",
        "pydantic-settings>=2.0.3",
        "pytest>=7.0.0",
        "pytest-cov>=3.0.0",
        "pytest-asyncio>=0.18.0",
        "asynctest>=0.13.0",
        "coverage>=6.0.0",
        "langchain>=0.3.15",
        "langchain-community>=0.3.15",
        "pymilvus>=2.3.3",
        "httpx",
    ],
    python_requires=">=3.11",
)