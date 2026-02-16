# Copyright 2026 The OpenSLM Project
from sqlmodel import SQLModel, Field, create_engine, Session, select
from ATLAS.database.base import BaseAdapter
from common.models.product import ProductBase
from typing import Optional

class SQLProduct(SQLModel, table=True):
    __tablename__ = "products"
    sku: str = Field(primary_key=True)
    name: str
    stock_count: int = 0
    weight: Optional[float] = None
    material: Optional[str] = None

class SQLAdapter(BaseAdapter):
    def __init__(self, database_url="sqlite:///./inventory.db"):
        self.engine = create_engine(database_url)

    def init_db(self):
        SQLModel.metadata.create_all(self.engine)
        print("SQL: Tables créées avec succès.")

    def get_product(self, sku: str) -> ProductBase:
        with Session(self.engine) as session:
            statement = select(SQLProduct).where(SQLProduct.sku == sku)
            result = session.exec(statement).first()
            if result:
                return ProductBase(**result.dict())
            return None
