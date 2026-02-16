# Copyright 2026 The OpenSLM Project
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from datasets import load_dataset

def train_slm(model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
    print(f"Démarrage du Fine-tuning pour {model_id}...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.pad_token = tokenizer.eos_token
    
    # Chargement du dataset local qu'on vient de télécharger
    dataset = load_dataset("json", data_files="data/train_spider.jsonl", split="train")

    def tokenize_function(examples):
        # Formatage pour l'instruction
        prompts = [f"Instruction: {q}
SQL: {s}" for q, s in zip(examples['question'], examples['query'])]
        return tokenizer(prompts, padding="max_length", truncation=True, max_length=512)

    tokenized_datasets = dataset.map(tokenize_function, batched=True)

    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16)

    # Arguments d'entraînement optimisés pour la rapidité
    training_args = TrainingArguments(
        output_dir="./slm-output",
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        num_train_epochs=1,
        learning_rate=2e-4,
        logging_steps=10,
        save_strategy="epoch",
        push_to_hub=False
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets,
    )

    print("Entraînement en cours...")
    trainer.train()
    model.save_pretrained("./fine_tuned_model")
    print("Modèle sauvegardé dans ./fine_tuned_model")

if __name__ == "__main__":
    # Pour tester le script sans lancer un vrai entraînement de 10h
    print("Script d'entraînement prêt. Lancez 'uv run train.py' pour démarrer.")
