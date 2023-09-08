#!/usr/bin/env python
# coding: utf-8

# In[ ]:


##############################################################################
#Amin Boroomand
#This code show how computational a company approach is.
#
#############################################################################


# In[5]:


import os
import PyPDF2
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
import pandas as pd

def read_pdf_files(folder_path):
    files_data = {}
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            with open(os.path.join(folder_path, file), "rb") as pdf_file:
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                file_text = ""
                for page_num in range(pdf_reader.numPages):
                    page = pdf_reader.getPage(page_num)
                    file_text += page.extractText()
                files_data[file] = file_text
    return files_data

def encode_text(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs[0].mean(axis=1).numpy()

def calculate_similarity_scores(files_data, reference_text, model, tokenizer):
    reference_embedding = encode_text(reference_text, model, tokenizer)
    scores = {}
    for file, file_text in files_data.items():
        file_embedding = encode_text(file_text, model, tokenizer)
        similarity_score = np.inner(file_embedding, reference_embedding)
        scores[file] = similarity_score.item()
    return scores

folder_path = Address
reference_text = "Computational biology applies bioinformatics, data analysis, data science, AI, software, and platforms to develop and apply data-analytical and theoretical methods, mathematical modeling, and computational simulations for the study of biological systems, including drug discovery."

# Load a pre-trained NLP model and tokenizer
model_name = "sentence-transformers/stsb-roberta-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Read PDF files and calculate similarity scores
files_data = read_pdf_files(folder_path)
similarity_scores = calculate_similarity_scores(files_data, reference_text, model, tokenizer)

# Normalize similarity scores to a scale of 0 to 10
max_score = max(similarity_scores.values())
min_score = min(similarity_scores.values())
normalized_scores = {file: 10 * (score - min_score) / (max_score - min_score) for file, score in similarity_scores.items()}

# Create a DataFrame from the normalized_scores dictionary
df = pd.DataFrame(normalized_scores.items(), columns=["File", "Computationality"])

# Remove '.pdf' extension from the file names
df["File"] = df["File"].str.replace(".pdf", "", regex=False)

# Round the scores to two decimal places
df["Computationality"] = df["Computationality"].round(2)

# Save the DataFrame as a CSV file
df.to_csv("Computationality.csv", index=False)


# In[ ]:





# In[ ]:




