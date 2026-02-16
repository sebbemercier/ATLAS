# Copyright 2026 The OpenSLM Project
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from datasets import load_dataset
import os

def train_slm(model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
    # Détection du hardware (MPS pour Mac M4)
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"🚀 Device détecté : {device.upper()}")
    
    print(f"Chargement de {model_id}...")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.pad_token = tokenizer.eos_token
    
    # Dataset Text-to-SQL
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "data", "train_spider.jsonl")
    dataset = load_dataset("json", data_files=data_path, split="train")

    def tokenize_function(examples):
        prompts = [f"Instruction: {q}\nSQL: {s}" for q, s in zip(examples['question'], examples['query'])]
        return tokenizer(prompts, padding="max_length", truncation=True, max_length=512)

    print("Tokenisation du dataset...")
    tokenized_datasets = dataset.map(tokenize_function, batched=True)

    print("Chargement du modèle sur le GPU M4...")
    model = AutoModelForCausalLM.from_pretrained(model_id).to(device)

    training_args = TrainingArguments(
        output_dir="./slm-output",
        per_device_train_batch_size=8, 
        gradient_accumulation_steps=2,
        num_train_epochs=1,
        learning_rate=2e-4,
        logging_steps=5,
        use_mps_device=True if device == "mps" else False,
        save_strategy="no", # On ne sauvegarde pas les checkpoints pour le test
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets,
    )

    print("--- Démarrage de l'entraînement ---")
    trainer.train()
    
    model.save_pretrained("./fine_tuned_atlas")
    print("✅ ATLAS entraîné et sauvegardé.")

if __name__ == "__main__":
    train_slm()
