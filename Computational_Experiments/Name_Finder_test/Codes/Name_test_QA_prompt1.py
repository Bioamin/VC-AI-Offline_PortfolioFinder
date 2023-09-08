#!/usr/bin/env python
# coding: utf-8

# In[49]:


import os
import pandas as pd
import PyPDF2
import pdfminer
import pdfrw
from pdfminer.high_level import extract_text
from typing import List, Dict
import re
from transformers import pipeline


# In[55]:


# Function to read pdf files in a folder using different PDF reader
def read_pdf_with_pypdf2(file_path: str) -> str:
    content = ""
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        for page_num in range(pdf_reader.numPages):
            content += pdf_reader.getPage(page_num).extractText()
    return content

def read_pdf_with_pdfminer(file_path: str) -> str:
    content = extract_text(file_path)
    return content

def read_pdfs_in_folder(folder_path: str, pdf_reader_packages: List[str]) -> List[Dict[str, str]]:
    pdf_files = []
    for pdf_reader in pdf_reader_packages:
        for file in os.listdir(folder_path):
            if file.endswith(".pdf"):
                file_path = os.path.join(folder_path, file)
                file_name = file[:-4]

                if pdf_reader == "PyPDF2":
                    content = read_pdf_with_pypdf2(file_path)
                elif pdf_reader == "pdfminer":
                    content = read_pdf_with_pdfminer(file_path)

                pdf_files.append({"file_name": file_name, "content": content, "pdf_reader": pdf_reader})

    return pdf_files


# In[56]:


# Function to clean pdf text

def clean_pdf_text(text: str) -> str:
    # Remove headers and footers (assumes they are on separate lines)
    lines = text.split("\n")
    cleaned_lines = [line for line in lines if not re.search(r"^\s*(Page\s+\d+|Header|Footer)", line)]
    
    # Remove page numbers and other unwanted information
    cleaned_lines = [re.sub(r"(\d+)\s*$", "", line) for line in cleaned_lines]
    
    # Join the cleaned lines back into a single string
    cleaned_text = "\n".join(cleaned_lines)
    
    return cleaned_text


# In[57]:


# Function to answer the question using AI question-answering package



def answer_question(text: str, question: str, qa_packages: List[str]) -> dict:
    answers = {}

    for qa_package in qa_packages:
        # Load the question-answering pipeline
        nlp = pipeline("question-answering", model=qa_package)

        # Answer the question
        try:
            answer = nlp(question=question, context=text)
            answers[qa_package] = answer["answer"]
        except Exception as e:
            print(f"Error with {qa_package}: {e}")
            answers[qa_package] = None
            continue

    return answers


# In[60]:


def process_pdf_files(folder_path: str, pdf_reader_packages: List[str] = ["PyPDF2", "pdfminer"], qa_packages: List[str] = [
    "bert-base-uncased",
    "bert-large-uncased",
    "distilbert-base-uncased",
    "albert-base-v2",
    "albert-large-v2",
    "google/electra-base-discriminator",
    "google/electra-large-discriminator",
    "dmis-lab/biobert-base-cased-v1.1",
    "allenai/scibert_scivocab_uncased",
    "microsoft/pubmedbert-base-uncased-abstract",
    "emilyalsentzer/Bio_ClinicalBERT",
    "bionlp/bluebert_pubmed_uncased_L-12_H-768_A-12"]):
    question = "What is the name of the company in the biotechnology or life sciences or bio-related or pharmaceutical sector analyzed in this report?"

    data = {"File_name": [], "PDF_QA_package": [], "Company_Name": []}
    df = pd.DataFrame(data)

    pdf_files = read_pdfs_in_folder(folder_path, pdf_reader_packages)

    for pdf_file in pdf_files:
        cleaned_text = clean_pdf_text(pdf_file["content"])
        answers = answer_question(cleaned_text, question, qa_packages)

        for qa_package, company_name in answers.items():
            if company_name:
                row = {
                    "File_name": pdf_file["file_name"],
                    "PDF_QA_package": f"{pdf_file['pdf_reader']}_{qa_package}",
                    "Company_Name": company_name
                }
                df = df.append(row, ignore_index=True)

    print(df)
    df.to_csv("names_test_QA_Prompt1.csv", index=False)


# In[ ]:


# Run the main function
if __name__ == "__main__":
    folder_path = "/Users/amin/Desktop/33/test"
    process_pdf_files(folder_path)


# The process_pdf_files function takes in a folder path, a list of PDF reader packages, and a list of question-answering (QA) packages as input.
# It starts by creating an empty list to store the PDF files and a list of dictionaries to store the extracted information.
# It calls the read_pdfs_in_folder function to extract the content of each PDF file in the folder using the specified PDF reader packages. The resulting list of PDF files is stored in the pdf_files variable.
# For each PDF file in the pdf_files list, the function first cleans the PDF content by removing headers, footers, and unnecessary information using the clean_pdf_text function.
# It then calls the answer_question function to extract the company name from the PDF content using each QA package specified in the input.
# The resulting company names are stored in a dictionary with the name of the QA package as the key.
# The function then creates a new column in the data frame to store the company name and the name of the PDF reader and QA packages used to extract it.
# Finally, the data frame is printed and saved to a file with a specified name.
# Overall, the function loops over all PDF files in the folder, extracts information from each file using different PDF readers and QA packages, and stores the results in a data frame for easy analysis.
