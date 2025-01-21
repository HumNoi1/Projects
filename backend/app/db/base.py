from typing import Any
from abc import ABC, abstractmethod
from app.core.config import settings
from supabase import create_client, Client
from pymilvus import connections, Collection

class DatabaseManager(ABC):
    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        pass

class SupabaseManager(DatabaseManager):
    def __init__(self):
        self.client: Client = None
        self.url: str = settings.SUPABASE_URL
        self.key: str = settings.SUPABASE_KEY

    async def connect(self) -> None:
        self.client = create_client(self.url, self.key)

    async def disconnect(self) -> None:
        if self.client:
            await self.client.postgrest.aclose()

class MilvusManager(DatabaseManager):
    def __init__(self):
        self.host: str = settings.MILVUS_HOST
        self.port: int = settings.MILVUS_PORT

    async def connect(self) -> None:
        connections.connect(
            alias="default",
            host=self.host,
            port=self.port
        )

    async def disconnect(self) -> None:
        connections.disconnect("default")