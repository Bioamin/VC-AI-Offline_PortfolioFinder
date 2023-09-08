#!/usr/bin/env python
# coding: utf-8

# In[5]:


import os
import pandas as pd
from transformers import pipeline
from pdfminer.high_level import extract_text

def read_pdf(file_path):
    """
    Read a PDF file and return its text content using Pdfminer.

    Args:
        file_path (str): The path of the PDF file.

    Returns:
        str: The text content of the PDF file.
    """
    text = extract_text(file_path)
    return text

def extract_company_name(text):
    """
    Use a pre-trained question-answering model to extract the company name from the text.

    Args:
        text (str): The text content to analyze.

    Returns:
        str: The company name.
    """
    nlp = pipeline('question-answering')
    question = "What is the name of the company?"
    answer = nlp(question=question, context=text)
    return answer['answer']

def process_pdf_files(directory):
    """
    Read PDF files in a directory, extract company names, and build a pandas DataFrame.

    Args:
        directory (str): The path of the directory containing the PDF files.

    Returns:
        pd.DataFrame: A pandas DataFrame with the file names and company names.
    """
    data = []

    for file_name in os.listdir(directory):
        if file_name.endswith('.pdf'):
            file_path = os.path.join(directory, file_name)
            text = read_pdf(file_path)
            company_name = extract_company_name(text)
            file_name_without_extension = file_name[:-4]  # Remove ".pdf" from the file name
            data.append({'File': file_name_without_extension, 'Company': company_name})

    df = pd.DataFrame(data)
    return df


# Set the path of the directory containing the PDF files
pdf_directory = Address

# Process the PDF files and get a pandas DataFrame
result_df = process_pdf_files(pdf_directory)
print(result_df)

# Save the DataFrame to a CSV file
result_df.to_csv('Name.csv', index=False)


# 
# Reader: pdfminer            
# QA:pipeline (distilbert-base-cased-distilled-squad model)        
# Not cleaned       prompt: What is the name of the company?
