#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#85%


# In[6]:


import os
import PyPDF2
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np

def pdf_to_text(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        text = ' '.join([pdf_reader.getPage(i).extractText() for i in range(pdf_reader.numPages)])
    return text

def process_text(text, model, categories):
    tokens = text.split()
    chunk_size = 300
    chunks = [' '.join(tokens[i:i + chunk_size]) for i in range(0, len(tokens), chunk_size)]

    diag_count = treat_count = 0

    for chunk in chunks:
        input_embedding = model.encode(chunk, convert_to_tensor=True)
        scores = {
            cat: [util.pytorch_cos_sim(input_embedding, phrase_embedding).numpy() for phrase_embedding in phrase_embeddings]
            for cat, phrase_embeddings in category_embeddings.items()
        }
        average_scores = {cat: np.mean(np.array(cat_scores)) for cat, cat_scores in scores.items()}
        most_relevant_category = max(average_scores, key=average_scores.get)
        
        if most_relevant_category == 'Disease Diagnosis':
            diag_count += 1
        else:
            treat_count += 1

    return 'Diagnosis' if diag_count > treat_count else 'Treatment'

# Load the pre-trained sentence transformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Define the categories and their related phrases
categories = {
    "Disease Diagnosis": [
        "medical diagnosis",
        "condition identification",
        "illness detection",
        "disorder diagnosis",
        "health problem identification",
        "pathology detection",
    ],
    "Disease Treatment": [
        "medical treatment",
        "therapeutic intervention",
        "medication",
        "therapy",
        "care plan",
        "healing regimen",
        "cure",
        "rehabilitation",
        "management",
    ],
}

category_embeddings = {cat: model.encode(phrases, convert_to_tensor=True) for cat, phrases in categories.items()}

# Path to the folder containing the PDF files
pdf_folder = Address

# Read PDF files and process them
data = []

for file_name in os.listdir(pdf_folder):
    if file_name.endswith('.pdf'):
        file_path = os.path.join(pdf_folder, file_name)
        text = pdf_to_text(file_path)
        diag_treat = process_text(text, model, categories)
        data.append((file_name[:-4], diag_treat))

# Create a DataFrame with the results
df = pd.DataFrame(data, columns=['File', 'Diag_Treat'])

df.to_csv('Diag_Treat.csv', index=False)


# In[ ]:





# In[ ]:




