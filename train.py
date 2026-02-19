# Copyright 2026 The OpenSLM Project
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from datasets import load_dataset
import os

def train_slm(model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"
    print(f"🚀 Device : {device.upper()}")
    
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.pad_token = tokenizer.eos_token
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "data", "train_spider.jsonl")
    dataset = load_dataset("json", data_files=data_path, split="train")

    def tokenize_function(examples):
        prompts = [f"Instruction: {q}\nSQL: {s}</s>" for q, s in zip(examples['question'], examples['query'])]
        outputs = tokenizer(prompts, padding="max_length", truncation=True, max_length=512)
        # CRUCIAL : Ajouter les labels pour le calcul de la loss
        outputs["labels"] = outputs["input_ids"].copy()
        return outputs

    tokenized_datasets = dataset.map(tokenize_function, batched=True)
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16).to(device)
    
    # Optimisation mémoire
    model.gradient_checkpointing_enable() 

    training_args = TrainingArguments(
        output_dir="./slm-output",
        per_device_train_batch_size=1, # Réduit à 1 pour éviter le Out Of Memory
        gradient_accumulation_steps=8, # On compense par plus d'accumulation
        num_train_epochs=1,
        learning_rate=1e-4,
        logging_steps=10,
        save_strategy="no",
        report_to="none"
    )

    trainer = Trainer(model=model, args=training_args, train_dataset=tokenized_datasets)
    trainer.train()
    model.save_pretrained("./fine_tuned_atlas")

if __name__ == "__main__":
    train_slm()
