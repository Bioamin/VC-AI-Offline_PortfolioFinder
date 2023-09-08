#!/usr/bin/env python
# coding: utf-8

# In[5]:


####################################################################################
# Amin Boroomand March2023
#This code moves currupted and encrypted and similar PDF files to junk folder
#
######################################################################################


# In[6]:


import os
import shutil
from PyPDF2 import PdfFileReader, PdfFileMerger

def is_corrupted(file_path):
    try:
        PdfFileReader(file_path)
    except Exception as e:
        return True
    return False

def is_password_protected(file_path):
    reader = PdfFileReader(file_path)
    return reader.isEncrypted

def has_duplicate_pages(file_path, duplicate_threshold=80):
    reader = PdfFileReader(file_path)
    num_pages = reader.getNumPages()
    content_set = set()

    for i in range(num_pages):
        content = reader.getPage(i).extractText()
        if content in content_set:
            content_set.add(content)
        else:
            return False

    if len(content_set) * duplicate_threshold / 100 <= num_pages:
        return True

    return False

source_folder = Address
junk_folder = os.path.join(source_folder, "junk")

if not os.path.exists(junk_folder):
    os.mkdir(junk_folder)

report_path = os.path.join(junk_folder, "report.txt")

with open(report_path, "w") as report_file:
    for filename in os.listdir(source_folder):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(source_folder, filename)

            if is_corrupted(file_path):
                reason = "corrupted"
            elif is_password_protected(file_path):
                reason = "password protected"
            elif has_duplicate_pages(file_path):
                reason = "more than 80% identical pages"
            else:
                continue

            log_message = f"{filename} - Moved to junk folder due to: {reason}\n"
            report_file.write(log_message)
            shutil.move(file_path, os.path.join(junk_folder, filename))

