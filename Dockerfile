# Copyright 2026 The OpenSLM Project
FROM python:3.9-slim

WORKDIR /app

# Installation de uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uv /usr/bin/

# Copie des fichiers de dépendances et modèles
COPY pyproject.toml .
COPY ATLAS/ ATLAS/
COPY common/ common/

# Installation des dépendances
RUN uv pip install --system -e .

WORKDIR /app/ATLAS

# Commande par défaut (peut être remplacée par train.py pour le premier lancement)
CMD ["python", "model.py"]
