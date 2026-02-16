# Copyright 2026 The OpenSLM Project
# Licensed under the Apache License, Version 2.0

from abc import ABC, abstractmethod
from common.models.product import ProductBase

class BaseAdapter(ABC):
    @abstractmethod
    def get_product(self, sku: str) -> ProductBase:
        """Récupère un produit par son SKU"""
        pass

    @abstractmethod
    def init_db(self):
        """Initialise la base (création tables/keyspace)"""
        pass
