# Copyright 2026 The OpenSLM Project
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class AtlasSettings(BaseSettings):
    # Type de DB : 'sql', 'nosql' (mongodb), 'cql' (scylladb)
    DB_TYPE: str = "sql"
    
    # Configuration SQL (Postgres, SQLite, MySQL)
    DATABASE_URL: str = "sqlite:///./inventory.db"
    
    # Configuration NoSQL (MongoDB)
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_NAME: str = "openslm_inventory"
    
    # Configuration CQL (ScyllaDB)
    SCYLLA_HOST: str = "127.0.0.1"
    SCYLLA_KEYSPACE: str = "openslm_inventory"
    
    # AI Settings
    TOKENIZER_PATH: str = "models/ecommerce_tokenizer.model"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = AtlasSettings()
