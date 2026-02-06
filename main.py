from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import torch
from transformers import pipeline
import sys
import os

# Ajouter le répertoire parent au path pour importer shared_data
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared_data import get_product_by_query, get_all_products

app = FastAPI(title="ATLAS | L'Architecte Produit")

@app.get("/search")
async def search_product(q: str):
    """Cherche un produit électrique par nom ou référence."""
    product = get_product_by_query(q)
    if product:
        return {"status": "found", "data": product}
    return {"status": "not_found", "message": "Référence inconnue en DB interne."}

@app.get("/catalog")
async def get_catalog():
    return get_all_products()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
