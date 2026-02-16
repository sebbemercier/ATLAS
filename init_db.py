# Copyright 2026 The OpenSLM Project
# Licensed under the Apache License, Version 2.0

from ATLAS.database.adapters.scylla_adapter import ScyllaAdapter

if __name__ == "__main__":
    print("Initialisation de ScyllaDB pour ATLAS...")
    try:
        adapter = ScyllaAdapter()
        adapter.init_db()
        print("Base de données prête.")
    except Exception as e:
        print(f"Erreur : Assurez-vous que ScyllaDB est lancé. Détails: {e}")
