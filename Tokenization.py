"""
Author: Hackathon
Version: 1.0 10-10-2023
Description: Tokenize the CSV file of dataset using GPT2 pre-trained model from Hugging Face
Notes: The current version is based on a dataset from AOP help finder and PubMed.
       The path to the files should be modified to user-specified locations for proper execution of the script.
Potential issues: no known issues
"""
from transformers import GPT2Tokenizer, GPT2LMHeadModel
model_name = "gpt2"  
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

import pandas as pd
from transformers import TextDataset, DataCollatorForLanguageModeling

df = pd.read_csv('C:/Users/Losti/Desktop/Dataset01.csv', encoding='latin1')

questions = df['questions']
inputs = df['inputs']
outputs = df['outputs']

from transformers import GPT2Tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

tokenized_inputs = [tokenizer.encode(text, add_special_tokens=True) for text in inputs]
tokenized_outputs = [tokenizer.encode(text, add_special_tokens=True) for text in outputs]

max_seq_length = 128
input_output_pairs = []

for input_tokens, output_tokens in zip(tokenized_inputs, tokenized_outputs):
    if len(input_tokens) + len(output_tokens) <= max_seq_length:
        input_output_pairs.append((input_tokens, output_tokens))

input_output_pairs = [(input_seq[:max_seq_length], output_seq[:max_seq_length]) for input_seq, output_seq in input_output_pairs]

input_output_pairs = [(input_seq + [tokenizer.pad_token_id] * (max_seq_length - len(input_seq)), output_seq + [tokenizer.pad_token_id] * (max_seq_length - len(output_seq))) for input_seq, output_seq in input_output_pairs]

save_path = 'C:/Users/Losti/Desktop/preprocessed_data2.txt'

with open(save_path, 'w', encoding='utf-8') as f:
    for input_seq, output_seq in input_output_pairs:
        input_text = ' '.join([tokenizer.convert_ids_to_tokens(token_id) for token_id in input_seq if token_id != tokenizer.pad_token_id])
        output_text = ' '.join([tokenizer.convert_ids_to_tokens(token_id) for token_id in output_seq if token_id != tokenizer.pad_token_id])
        f.write(f"Input: {input_text}\nOutput: {output_text}\n\n")
