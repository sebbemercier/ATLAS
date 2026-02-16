# Copyright 2026 The OpenSLM Project
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import os
from cassandra.cqlengine import columns, models, connection
from cassandra.cluster import Cluster
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    scylla_host: str = "127.0.0.1"
    scylla_keyspace: str = "openslm_inventory"

    class Config:
        env_file = ".env"

settings = Settings()

class ProductModel(models.Model):
    __keyspace__ = settings.scylla_keyspace
    sku = columns.Text(primary_key=True)
    name = columns.Text()
    stock_count = columns.Integer(default=0)
    weight = columns.Float()
    material = columns.Text()
    supplier_url = columns.Text()

def init_db():
    """Initialise la connexion et crée le keyspace/table si besoin"""
    cluster = Cluster([settings.scylla_host])
    session = cluster.connect()
    
    # Création du keyspace
    session.execute(f"""
        CREATE KEYSPACE IF NOT EXISTS {settings.scylla_keyspace} 
        WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': '1'}}
    """)
    
    # Connexion de cqlengine
    connection.setup([settings.scylla_host], settings.scylla_keyspace, lazy_connect=True)
    connection.get_session().execute(f"USE {settings.scylla_keyspace}")
    
    # Création des tables
    from cassandra.cqlengine.management import sync_table
    sync_table(ProductModel)
    print(f"ScyllaDB: Table ProductModel synchronisée dans {settings.scylla_keyspace}")

class ScyllaAdapter:
    def __init__(self):
        try:
            connection.setup([settings.scylla_host], settings.scylla_keyspace, lazy_connect=True)
        except Exception as e:
            print(f"Erreur connexion ScyllaDB: {e}")

    def get_product(self, sku):
        try:
            return ProductModel.objects(sku=sku).first()
        except Exception as e:
            print(f"Erreur requête ScyllaDB: {e}")
            return None
