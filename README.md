# VC-AI-Offline_PortfolioFinder
This project harnessed the power of AI to extract and analyze data from a vast assortment of unstructured PDFs, aiming to identify and cluster bio-based companies for potential venture capital investments.

# Machine Learning Prototype for Clustering Potential Bio-Investments

## Problem Statement
This project focuses on developing a machine learning prototype to cluster potential investments in bio-related companies. The dataset comprises 600 unstructured PDF files. The main challenges include:
- Dataset's vast size (varying file sizes and page counts).
- Dealing with corrupted or password-protected files.
- Differentiating between finance reports and general bio-related company information.
- Undefined clustering variables and investment criteria.

The overarching goal is to efficiently extract, clean, and categorize data for in-depth analysis and investment decision-making.

## Approach
To address the problem:
1. Organized the dataset into categories.
2. Conducted a literature review to identify vital success-determining features for bio-related companies.
3. Experimented with various data reading, cleaning, and extraction strategies.
4. Compared AI-driven extraction with manually curated datasets for validation.
5. Organized data before clustering to account for category-specific risk-reward profiles.

Given the constraints and goals, the chosen approach emphasized pre-organization for meaningful clustering results.

## Technical Description of the Prototype
The prototype encompasses:
- File cleaning and reading.
- Data extraction from the PDFs.
- Evaluating extraction accuracy.
- Organizing potential investments.
- Clustering experimentation and evaluation using the silhouette score.
- Final selection of the best clustering method.

For an in-depth understanding, refer to the detailed documentation within the code folder.

## Evaluation
Data extraction was validated against a manually extracted dataset from 5% of the files. The clustering method's efficacy was assessed using the silhouette score.

## Future Steps
1. **Enhance Data Extraction and Evaluation Accuracy:**
   - Explore advanced PDF parsing tools and AI-based Q&A systems.
   - Expand the manually curated dataset.
   - Rectify common extraction errors.
   - Develop a tailored Q&A model.
   
2. **Expand Data and Information Extraction:**
   - Extract team metrics (team size, interdisciplinary structure, field leader connections).
   - Analyze professional online presence and paper citations.
   - Investigate affiliations with trending topics.

3. **Establish Company Priorities:**
   - Work with the team to pinpoint company priorities.
   - Examine factors like market size, innovation degree, and computational focus.
   - Discover collaboration opportunities.

4. **Experiment with Advanced Clustering Techniques:**
   - Optimize various clustering algorithms and hyperparameters.

## Challenge Recap
- Dealt with over 500 diverse, unstructured PDFs.
- Aimed to pinpoint and categorize bio-based companies for investments.

## Solution Breakdown
### 1. **Extraction:**
Focused on efficient, accurate data extraction using tools like PyPDF2 and PDFMiner.six. Key steps involved cleaning, refining, segmenting, and data mining via advanced NLP tools.

### 2. **Clustering:**
This phase involved grouping companies and experimenting with distinct clustering methodologies. Optimization was paramount, using the silhouette score for validation.

## Results
Attained an outstanding 86% accuracy in AI-driven vs. manual data extraction from the PDFs.


# Repository Scripts Description

## **Main_Data_Extraction.py**
_For the data extraction, you only need to run this code._
This script automates the execution of a series of Python files and consolidates their output into a single CSV file. It details:
- Importation of necessary libraries, address parameter setting, and specifying a list of Python files to run.
- A function, `run_python_file`, to execute the files using the 'subprocess' library.
- Iteration over the list of Python files, executing each and printing the status.
- The second part changes the working directory, reads CSV files, and consolidates them into "Data.csv".

## **1_Junk_file_removal.py**
This script:
- Identifies and moves corrupted, encrypted, and similar PDF files to a junk folder.
- Creates a report in the junk folder to log moved files.
- Iterates through files, checks conditions, logs the status, and moves files accordingly.

## **2_Name.py**
This script is:
- Designed to process PDFs, extracting company names, and generating a DataFrame.
- Uses libraries for file management, text extraction, and the Transformers library.
- Calls the `process_pdf_files` function to create a DataFrame, displaying it and saving as 'Name.csv'.

## **Age.py**
This Python script:
- Queries the OpenAI API for company ages.
- Loads API keys, queries for the founding year, and calculates age.
- Reads a CSV file of company names, updates the DataFrame with ages, and saves as "Age.csv".

## **Clinical_Phase.py**
This script:
- Analyzes PDFs, extracts text, and determines the clinical stage from the content.
- Reads PDFs, queries a model with "In which clinical stage phase is the company?", and saves results as "Clinical.csv".

## **Computationality.py**
This script:
- Assesses a company's computational approach by analyzing PDF content.
- Uses the Transformers library for pre-trained NLP models.
- Reads PDFs, calculates similarity scores, and saves results as "Computationality.csv".

## **Diag_Treatment.py**
This script:
- Analyzes PDFs and classifies content into "Disease Diagnosis" or "Disease Treatment".
- Reads PDFs, processes text using a pre-trained NLP model, and saves results as "Diag_Treat.csv".

## **Issue_category_finder.py**
This script has two parts:
1. Uses the transformers library to extract main diseases from PDFs, processes chunks, and saves as a CSV.
2. Uses the OpenAI GPT-3 API to classify disease keywords, reads a CSV, updates a DataFrame, and prints it.

## **Location.py**
This code:
- Determines company locations and classifies them into geographical areas.
- Queries the OpenAI GPT-3 API for locations, classifies into areas, and saves as a CSV.

## **Method.py**
This script:
- Reads PDFs and classifies them based on content.
- Uses keyword counts to determine the main method area and saves as "Method.csv".

