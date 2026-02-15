# Copyright 2026 The OpenSLM Project
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import datetime

from common.models.product import ProductBase

class AtlasAgent:
    def __init__(self, db_adapter=None):
        self.db = db_adapter
        self.sources = []

    def handle_query(self, sku):
        self.sources = []
        print(f"
--- OpenSLM Query for SKU: {sku} ---")
        
        # 1. Database Check
        product = self.get_product_from_db(sku)
        
        # 2. Logic: Stock from DB only, Attributes can fallback to Web
        stock = product.stock_count if product else "UNKNOWN"
        weight = product.weight if product else None
        
        if not weight:
            web_data = self.web_fallback(sku)
            weight = web_data.get('weight')
            if web_data.get('url'):
                self.sources.append(f"Web Source: {web_data['url']}")
        
        if product:
            self.sources.append("Local Database")
            
        return self.format_output(sku, stock, weight)

    def query_scylla(self, sku):
        """Simule SELECT stock_count, weight, material FROM product_details WHERE sku = ..."""
        # Simulation d'un produit qui a du stock mais pas de détails techniques
        if sku == "NIKE-123":
            return {
                "sku": "NIKE-123",
                "stock_count": 42,
                "weight": None, # Manquant !
                "material": "Synthétique"
            }
        return None

    def search_internet_fallback(self, sku):
        """Simulation du fallback 'Perplexity'"""
        return {
            "weight": "850g",
            "material": "Cuir et Mesh",
            "url": "https://nike.com/pdp/air-max-123"
        }

    def format_output(self, sku, stock, weight, material):
        res = f"Fiche Produit : {sku}
"
        res += f"📦 STOCK : {stock} (Source: ScyllaDB uniquement)
"
        res += f"⚖️ POIDS : {weight}
"
        res += f"🧵 MATIÈRE : {material}
"
        res += "
SOURCES ET CITATIONS :
"
        for i, s in enumerate(self.sources, 1):
            res += f"[{i}] {s}
"
        return res

if __name__ == "__main__":
    agent = AtlasAgent()
    # Test avec un produit existant mais incomplet
    print(agent.handle_query("NIKE-123"))