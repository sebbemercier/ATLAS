# ATLAS - Inventory & Knowledge SLM
Le pilier "Commerce" de CEDRA. Responsable de la fiabilité des données produits.

## Rôle
- Génération de requêtes CQL pour ScyllaDB.
- Fallback sur recherche internet si les attributs techniques sont manquants.
- Gestion des sources et citations.

## Installation & Usage
```bash
uv pip install -r requirements.txt
# Entraîner le tokenizer
uv run train_tokenizer.py
# Lancer le modèle
uv run model.py
```

## Dataset (dans /data)
Contient les paires (Question -> Requête CQL) pour le fine-tuning.
