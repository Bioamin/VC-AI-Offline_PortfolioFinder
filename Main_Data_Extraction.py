#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import subprocess
import os
import pandas as pd

# Address parameter
address = "/Users/amin/Desktop/Symbiosis_Amin"

# List of Python files to run in the specified order
python_files = [
    "1_Junk_file_removal.py",
    "2_Name.py",
    "Age.py",
    "Clinical_Phase.py",
    "Computationality.py",
    "Diag_Treatment.py",
    "Issue_category_finder.py",
    "Location.py",
    "Method.py",
]

# List of Python files that require the Address parameter
files_needing_address = [
    "Age.py",
    "Clinical_Phase.py",
    "Computationality.py",
    "Diag_Treatment.py",
    "Issue_category_finder.py",
    "Location.py",
    "Method.py",
]

# Function to run a Python file
def run_python_file(file, address=None):
    if address and file in files_needing_address:
        command = ["python", file, address]
    else:
        command = ["python", file]
    
    process = subprocess.run(command, check=True)
    return process.returncode

# Run all Python files in the specified order
for file in python_files:
    print(f"Running {file}...")
    return_code = run_python_file(file, address)
    if return_code == 0:
        print(f"{file} completed successfully.")
    else:
        print(f"{file} encountered an error. Return code: {return_code}")
        break


# In[ ]:


# Set the working directory to where the CSV files are located
os.chdir("/Users/amin/Desktop/33/1_100/Code")

# Read CSV files into pandas dataframes
df_name = pd.read_csv("Name.csv")
df_issue = pd.read_csv("issue.csv")
df_method = pd.read_csv("Method.csv")
df_location = pd.read_csv("Location.csv")
df_computationality = pd.read_csv("Computationality.csv")
df_clinical = pd.read_csv("Clinical.csv")
df_age = pd.read_csv("Age.csv")
df_DT = pd.read_csv("Diag_Treat.csv")

# Concatenate dataframes using inner join on the first column
df = pd.concat([df_name.set_index("File"),
                df_issue.set_index("File"),
                df_method.set_index("File"),
                df_location.set_index("File"),
                df_computationality.set_index("File"),
                df_clinical.set_index("File"),
                df_age.set_index("File"),
                df_DT.set_index("File")],
               axis=1,
               join="inner")

# Save the final dataframe to a new CSV file
df.to_csv("Data.csv")

