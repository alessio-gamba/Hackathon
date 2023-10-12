"""
Author: Hackathon
Version: 1.0 12-10-2023
Description: Fine-tuning of the preprocessed data using GPT2 pre-trained model 
Notes: The current version is based on a dataset from AOP help finder and PubMed 
       The path to the files should be modified to user-specified locations for proper execution of the script.
Potential issues: no known issues
"""
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling, TextDataset

model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

max_seq_length = 128
dataset = TextDataset(
    tokenizer=tokenizer,
    file_path="C:/Users/Losti/Desktop/preprocessed_data2.txt",
    block_size=max_seq_length,
)

# Create the data_collator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
)

training_args = TrainingArguments(
    output_dir="C:/Users/Losti/Desktop/gpt2-finetuned",  
    overwrite_output_dir=True,
    num_train_epochs=3,  # Adjust as needed
    per_device_train_batch_size=4,  # Adjust batch size
    save_steps=10,  # Number of training steps before saving the model
    save_total_limit=2,  # Limit the number of saved checkpoints
    evaluation_strategy="steps",  # Evaluation during training steps
    eval_steps=10,  # Number of steps between evaluations
    logging_steps=10,  # Log training progress every N steps
    learning_rate=2e-5,  # Learning rate for fine-tuning (adjust as needed)
    warmup_steps=500,  # Number of warm-up steps
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    data_collator=data_collator,
    eval_dataset=dataset,  
)

trainer.train()
trainer.save_model()
