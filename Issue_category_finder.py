#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#80%


# In[2]:


import os
import PyPDF2
import pandas as pd
from transformers import pipeline
from tqdm import tqdm
import configparser
import openai
import re
import time

def extract_pdf_text(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ""
        for page_num in range(reader.numPages):
            text += reader.getPage(page_num).extractText()
    return text

def split_into_chunks(text, chunk_size):
    tokens = text.split()
    chunks = [' '.join(tokens[i:i+chunk_size]) for i in range(0, len(tokens), chunk_size)]
    return chunks

def find_diseases(chunks, nlp):
    diseases = []
    for chunk in chunks:
        answer = nlp(question="What is the main disease this text is about?", context=chunk)
        diseases.append(answer['answer'])
    return list(set(diseases))

def process_files(input_folder):
    nlp = pipeline("question-answering", model="distilbert-base-cased-distilled-squad", revision="626af31")
    data = []

    for file_name in tqdm(os.listdir(input_folder)):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(input_folder, file_name)
            text = extract_pdf_text(file_path)
            chunks = split_into_chunks(text, 300)
            diseases = find_diseases(chunks, nlp)
            data.append([file_name[:-4], ', '.join(diseases)])

    return data

def create_dataframe(data):
    df = pd.DataFrame(data, columns=['File', 'KW'])
    return df

def save_dataframe(df, output_file):
    df.to_csv(output_file, index=False)

input_folder = Address
output_file = 'KW.csv'

data = process_files(input_folder)
df = create_dataframe(data)
save_dataframe(df, output_file)


# In[8]:





# In[1]:


import configparser
import openai
import pandas as pd
import re
import time

def load_openai_api_key():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config["openai"]["api_key"]

def find_matching_area(answer):
    areas = [
        "Vaccines or infectious",
        "Gastrointestinal or metabolism",
        "Neurological",
        "Cancer or tumors or oncology",
        "Dermatological",
        "Organ health",
        "Mental",
        "Other",
    ]
    for area in areas:
        if re.search(area.lower(), answer.lower()):
            return area
    return "Other"

def get_related_area(keywords):
    openai.api_key = load_openai_api_key()
    prompt = f"Which of the following areas is more related to the keywords: {keywords}?\n\nAreas:\n" \
             "Vaccines or infectious\n" \
             "Gastrointestinal or metabolism\n" \
             "Neurological\n" \
             "Cancer or tumors or oncology\n" \
             "Dermatological\n" \
             "Organ health\n" \
             "Mental\n" \
             "Other\n\nAnswer: "

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=10,
        n=1,
        stop=None,
        temperature=0.5,
    )

    answer = response.choices[0].text.strip()
    matching_area = find_matching_area(answer)
    time.sleep(1)  # Add a 1-second delay
    return matching_area

def main():
    # Load DataFrame
    df = pd.read_csv("KW.csv")

    # Add a new column 'Issue'
    df["Issue"] = df["KW"].apply(get_related_area)

    # Drop the 'KW' column
    df = df.drop(columns=["KW"])
    print(df)

    # Save the DataFrame to a new CSV file
    df.to_csv("issue.csv", index=False)

if __name__ == "__main__":
    main()


# In[ ]:




