#!/usr/bin/env python
# coding: utf-8

# In[ ]:


############################################################
#Amin Boroomand
#This code search the web for company age
#
############################################################


# In[1]:


import openai
import configparser
import re
import pandas as pd
import time

def load_openai_api_key():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config["openai"]["api_key"]

def get_founding_year(company_name, api_key):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"When was {company_name} founded?",
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    match = re.search(r"(\d{4})", message)
    if match:
        return int(match.group(1))
    else:
        return None

def rate_limited_request(company_name, api_key, sleep_time=1):
    while True:
        try:
            year = get_founding_year(company_name, api_key)
            return year
        except openai.error.RateLimitError:
            time.sleep(sleep_time)

def get_company_age(founding_year, current_year=2023):
    if founding_year is None:
        return None
    return current_year - founding_year

def get_founding_years_and_ages(df, api_key):
    df['Age'] = None
    for index, row in df.iterrows():
        company = row['Company']
        year = rate_limited_request(company, api_key)  # Use rate_limited_request
        age = get_company_age(year)
        if year is not None and age is not None:
            df.at[index, 'Age'] = age
        else:
            print({company},"N/A")
    return df

if __name__ == "__main__":
    # Read the CSV file
    df = pd.read_csv("Name.csv")

    # Load API key and get company ages
    api_key = load_openai_api_key()
    df_with_ages = get_founding_years_and_ages(df, api_key)

    # Remove the 'Company' column
    df_with_ages.drop(columns=['Company'], inplace=True)

    # Save the resulting dataframe to a CSV file
    df_with_ages.to_csv("Age.csv", index=False)


# In[ ]:




