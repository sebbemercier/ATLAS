# Copyright 2026 The OpenSLM Project
from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from ATLAS.database.base import BaseAdapter
from common.models.product import ProductBase
import asyncio

class NoSQLProduct(Document):
    sku: str
    name: str
    stock_count: int
    weight: float = None
    material: str = None

    class Settings:
        name = "products"

from ATLAS.database.config import settings

class NoSQLAdapter(BaseAdapter):
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db_name = settings.MONGODB_NAME

    def init_db(self):
        # Beanie est asynchrone, on utilise une petite boucle pour l'init
        loop = asyncio.get_event_loop()
        loop.run_until_complete(init_beanie(database=self.client[self.db_name], document_models=[NoSQLProduct]))
        print(f"NoSQL: MongoDB connecté à {self.db_name}")

    def get_product(self, sku: str) -> ProductBase:
        loop = asyncio.get_event_loop()
        async def _get():
            await init_beanie(database=self.client[self.db_name], document_models=[NoSQLProduct])
            doc = await NoSQLProduct.find_one(NoSQLProduct.sku == sku)
            return ProductBase(**doc.dict()) if doc else None
        return loop.run_until_complete(_get())
