# app/db/base.py
from typing import Any
from abc import ABC, abstractmethod
from app.core.config import settings
from supabase import create_client, Client
from pymilvus import connections, Collection

class DatabaseManager(ABC):
    @abstractmethod
    async def connect(self) -> None:
        """Abstract method สำหรับการเชื่อมต่อกับฐานข้อมูล"""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Abstract method สำหรับการปิดการเชื่อมต่อ"""
        pass

class SupabaseManager(DatabaseManager):
    def __init__(self):
        self.client: Client | None = None
        self.url: str = settings.SUPABASE_URL
        self.key: str = settings.SUPABASE_KEY

    async def connect(self) -> None:
        """สร้างการเชื่อมต่อกับ Supabase"""
        if not self.client:
            self.client = create_client(self.url, self.key)

    async def disconnect(self) -> None:
        """ปิดการเชื่อมต่อกับ Supabase"""
        if self.client and hasattr(self.client, 'postgrest'):
            self.client.postgrest.aclose()
        self.client = None

class MilvusManager(DatabaseManager):
    def __init__(self):
        self.host: str = settings.MILVUS_HOST
        self.port: int = settings.MILVUS_PORT
        self._connected: bool = False

    async def connect(self) -> None:
        """สร้างการเชื่อมต่อกับ Milvus"""
        if not self._connected:
            connections.connect(
                alias="default",
                host=self.host,
                port=self.port
            )
            self._connected = True

    async def disconnect(self) -> None:
        """ปิดการเชื่อมต่อกับ Milvus"""
        if self._connected:
            connections.disconnect("default")
            self._connected = False