# Copyright 2026 The OpenSLM Project
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import datetime
import sentencepiece as spm
from ATLAS.database import ScyllaAdapter

class AtlasAgent:
    def __init__(self, db_adapter=None, tokenizer_path="models/ecommerce_tokenizer.model"):
        self.db = db_adapter or ScyllaAdapter()
        self.sp = spm.SentencePieceProcessor(model_file=tokenizer_path)
        self.sources = []

    def handle_query(self, sku):
        self.sources = []
        print(f"\n--- OpenSLM Query for SKU: {sku} ---")
        
        # 1. Database Check (Using ORM)
        product = self.db.get_product(sku)
        
        # 2. Logic: Stock from DB only
        stock = product.stock_count if product else "UNKNOWN (Not in DB)"
        weight = product.weight if product else None
        material = product.material if product else None
        
        # 3. Fallback for attributes only
        if not weight or not material:
            print(f"ATLAS: Attributes missing for {sku}. Checking Web Fallback...")
            web_data = self.search_internet_fallback(sku)
            
            weight = weight or web_data.get('weight')
            material = material or web_data.get('material')
            
            if web_data.get('url'):
                self.sources.append(f"Web Source: {web_data['url']}")
        
        if product:
            self.sources.append("Local ScyllaDB (Verified Inventory)")
            
        return self.format_output(sku, stock, weight, material)

    def search_internet_fallback(self, sku):
        """Simulation du fallback 'Perplexity'"""
        # Dans la version finale, ceci appellerait un module de scraping/search
        return {
            "weight": "850g",
            "material": "Cuir et Mesh",
            "url": "https://nike.com/pdp/air-max-123"
        }

    def format_output(self, sku, stock, weight, material):
        res = f"Fiche Produit : {sku}\n"
        res += f"📦 STOCK : {stock} (Source: ScyllaDB)\n"
        res += f"⚖️ POIDS : {weight or 'N/A'}\n"
        res += f"🧵 MATIÈRE : {material or 'N/A'}\n"
        res += "\nSOURCES ET CITATIONS :\n"
        for i, s in enumerate(self.sources, 1):
            res += f"[{i}] {s}\n"
        return res

if __name__ == "__main__":
    agent = AtlasAgent()
    # Test avec un produit existant mais incomplet
    print(agent.handle_query("NIKE-123"))