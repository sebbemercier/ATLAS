# Copyright 2026 The OpenSLM Project
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import sentencepiece as spm
import os

def train_ecommerce_tokenizer(input_file, model_prefix):
    print(f"Démarrage de l'entraînement sur {input_file}...")
    
    # Paramètres optimisés pour SLM trilingue (FR, NL, EN)
    spm.SentencePieceTrainer.train(
        input=input_file,
        model_prefix=model_prefix,
        vocab_size=300, # Réduit pour le petit corpus de test
        model_type='unigram',
        character_coverage=1.0,
        byte_fallback=True,
        # Symboles pour les tâches futures (Masking, Classification, etc.)
        user_defined_symbols=['[MASK]', '[CLS]', '[SEP]', '[PAD]'],
        normalization_rule_name='nmt_nfkc_cf'
    )
    print(f"Succès ! Fichiers générés : {model_prefix}.model et {model_prefix}.vocab")

if __name__ == "__main__":
    if os.path.exists("corpus.txt"):
        train_ecommerce_tokenizer("corpus.txt", "ecommerce_tokenizer")
    else:
        print("Erreur : corpus.txt introuvable.")