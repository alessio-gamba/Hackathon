"""
Author: Hackathon
Version: 1.0 12-10-2023
Description: Evaluation of the Fine-Tuned model
Notes: The current version is based on a dataset from AOP help finder and PubMed 
       The path to the files should be modified to user-specified locations for proper execution of the script.
Potential issues: no known issues
"""
from transformers import GPT2LMHeadModel
model = GPT2LMHeadModel.from_pretrained("C:/Users/Losti/Desktop/gpt2-finetuned")

from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

input_text = "propofol promoted expression levels of MBD3 and binding to the -1,000 to -1 bp (transcription start site) region of HACE1 gene promoter."

input_ids = tokenizer.encode(input_text, return_tensors="pt")

attention_mask = torch.ones(input_ids.shape, dtype=input_ids.dtype)

generated_text = model.generate(input_ids, max_length=128, num_return_sequences=1, no_repeat_ngram_size=2, attention_mask=attention_mask)

print(tokenizer.decode(generated_text[0], skip_special_tokens=True))
