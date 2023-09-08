#!/usr/bin/env python
# coding: utf-8

# In[3]:


################################################################################################
#Amin Boroomand
#This file read PDF files and find which method category the company solution belongs to
# 
################################################################################################


# In[1]:


import os
import PyPDF2
import re
import pandas as pd
from collections import Counter

def get_text_from_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ""
        for page_num in range(reader.numPages):
            text += reader.getPage(page_num).extractText()
    return text

def main_method_area(text):
    text = text.lower()

    keywords = {
        "Drug Discovery": ["drug discovery", "drug development", "pharmaceutical"],
        "Genomics or Gene Editing": ["genomics", "gene editing", "crispr", "genome"],
        "Immunotherapy or Cell Engineering": ["immunotherapy", "cell engineering", "cell therapy", "t cell", "car-t"],
        "Microbiome": ["microbiome", "microbial", "microorganisms"],
        "Computational Biology and AI": ["computational biology", "bioinformatics", "machine learning", "artificial intelligence", "ai", "deep learning"],
    }

    keyword_counts = Counter()

    for category, keyword_list in keywords.items():
        for keyword in keyword_list:
            keyword_counts[category] += len(re.findall(r'\b' + keyword + r'\b', text))

    most_common_category = keyword_counts.most_common(1)[0]

    return most_common_category[0] if most_common_category[1] > 0 else "Other"

pdf_folder = Address

data = []

for file_name in os.listdir(pdf_folder):
    if file_name.endswith(".pdf"):
        file_path = os.path.join(pdf_folder, file_name)
        text = get_text_from_pdf(file_path)
        method_area = main_method_area(text)
        data.append({"File": file_name[:-4], "Method": method_area})

df = pd.DataFrame(data)
df.to_csv("Method.csv", index=False)


# In[4]:




