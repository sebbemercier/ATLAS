# Copyright 2026 The OpenSLM Project
from ATLAS.database.config import settings
from ATLAS.database.adapters.scylla_adapter import ScyllaAdapter
from ATLAS.database.adapters.sql_adapter import SQLAdapter
from ATLAS.database.adapters.nosql_adapter import NoSQLAdapter

def get_db_adapter():
    db_type = settings.DB_TYPE.lower()
    
    if db_type in ["scylla", "cql"]:
        return ScyllaAdapter()
    elif db_type in ["nosql", "mongodb", "mongo"]:
        return NoSQLAdapter()
    else:
        return SQLAdapter()
