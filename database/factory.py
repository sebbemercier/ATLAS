# Copyright 2026 The OpenSLM Project
import os
from ATLAS.database.adapters.scylla_adapter import ScyllaAdapter
from ATLAS.database.adapters.sql_adapter import SQLAdapter
from ATLAS.database.adapters.nosql_adapter import NoSQLAdapter

def get_db_adapter():
    db_type = os.getenv("DB_TYPE", "sql").lower()
    
    if db_type == "scylla" or db_type == "cql":
        return ScyllaAdapter()
    elif db_type == "nosql" or db_type == "mongodb":
        return NoSQLAdapter(mongodb_url=os.getenv("MONGODB_URL", "mongodb://localhost:27017"))
    else:
        return SQLAdapter(database_url=os.getenv("DATABASE_URL", "sqlite:///./inventory.db"))
