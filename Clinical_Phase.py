#!/usr/bin/env python
# coding: utf-8

import os
import PyPDF2
import pandas as pd
from transformers import pipeline

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        text = ""
        for page_num in range(pdf_reader.numPages):
            text += pdf_reader.getPage(page_num).extractText()
    return text

def find_clinical_stage(text):
    question = "In which clinical stage phase is the company?"
    nlp = pipeline("question-answering")
    answer = nlp(question=question, context=text)
    return answer["answer"]

def get_clinical_stage_integer(answer_text):
    if "Phase 1" in answer_text:
        return 1
    elif "Phase 2" in answer_text:
        return 2
    elif "Phase 3" in answer_text:
        return 3
    else:
        return 0

def process_pdf_files(folder_path):
    data = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".pdf"):
            pdf_file_path = os.path.join(folder_path, file_name)
            pdf_text = extract_text_from_pdf(pdf_file_path)
            if pdf_text:  # Check if the pdf_text is not empty
                answer_text = find_clinical_stage(pdf_text)
                clinical_stage = get_clinical_stage_integer(answer_text)
                data.append([file_name.replace(".pdf", ""), clinical_stage])
            else:
                print(f"Failed to extract text from {file_name}. Setting clinical stage as 'NA'.")
                data.append([file_name.replace(".pdf", ""), "NA"])
                continue

    df = pd.DataFrame(data, columns=["File", "Clinical"])
    df.to_csv("Clinical.csv", index=False)

def main():
    pdf_folder_path = Address
    process_pdf_files(pdf_folder_path)

if __name__ == "__main__":
    main()
