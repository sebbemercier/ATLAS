# Copyright 2026 The OpenSLM Project
from cassandra.cqlengine import columns, models, connection
from cassandra.cluster import Cluster
from ATLAS.database.config import settings
from ATLAS.database.base import BaseAdapter
from common.models.product import ProductBase

class ScyllaProductModel(models.Model):
    __keyspace__ = settings.SCYLLA_KEYSPACE
    sku = columns.Text(primary_key=True)
    name = columns.Text()
    stock_count = columns.Integer(default=0)
    weight = columns.Float()
    material = columns.Text()
    supplier_url = columns.Text()

class ScyllaAdapter(BaseAdapter):
    def __init__(self):
        try:
            connection.setup([settings.SCYLLA_HOST], settings.SCYLLA_KEYSPACE, lazy_connect=True)
        except Exception as e:
            print(f"Erreur connexion ScyllaDB: {e}")

    def init_db(self):
        cluster = Cluster([settings.SCYLLA_HOST])
        session = cluster.connect()
        session.execute(f"CREATE KEYSPACE IF NOT EXISTS {settings.SCYLLA_KEYSPACE} WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': '1'}}")
        connection.setup([settings.SCYLLA_HOST], settings.SCYLLA_KEYSPACE, lazy_connect=True)
        from cassandra.cqlengine.management import sync_table
        sync_table(ScyllaProductModel)
        print(f"ScyllaDB: Table synchronisée dans {settings.SCYLLA_KEYSPACE}")

    def get_product(self, sku: str) -> ProductBase:
        raw = ScyllaProductModel.objects(sku=sku).first()
        if raw:
            # Conversion brute vers Pydantic
            data = {k: getattr(raw, k) for k in ['sku', 'name', 'stock_count', 'weight', 'material', 'supplier_url']}
            return ProductBase(**data)
        return None
