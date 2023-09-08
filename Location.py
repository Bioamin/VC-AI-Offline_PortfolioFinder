#!/usr/bin/env python
# coding: utf-8

# In[ ]:


####################################################################
#Amin Boroomand
# This code find the location of a company
####################################################################


# In[17]:


import openai
import configparser
import pandas as pd
import time

def load_openai_api_key():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config["openai"]["api_key"]

def get_company_location(company_name, api_key):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Provide the company location (city and state, if in the USA) of {company_name} in the format: Company Name, Location",
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message

def get_company_locations(name_df, api_key):
    company_locations = []
    for index, row in name_df.iterrows():
        company = row['Company']
        file = row['File']
        try:
            location = get_company_location(company, api_key)
            if location is not None:
                company_locations.append([file, location])
            else:
                company_locations.append([file, "N/A"])
        except openai.error.RateLimitError as e:
            wait_time = 5  # Fixed waiting time in seconds
            print(f"Rate limit reached. Waiting for {wait_time} seconds.")
            time.sleep(wait_time)
            location = get_company_location(company, api_key)
            if location is not None:
                company_locations.append([file, location])
            else:
                company_locations.append([file, "N/A"])
    return company_locations

if __name__ == "__main__":
    # Read the companies from the 'Name.csv' file
    name_df = pd.read_csv("Name.csv")

    api_key = load_openai_api_key()
    company_locations = get_company_locations(name_df, api_key)
    
    df = pd.DataFrame(company_locations, columns=['File', 'Location'])
    #print(df)

    # Save the DataFrame to a CSV file
    df.to_csv("city.csv", index=False)


# In[ ]:


def get_location_area(location):
    east_usa_keywords = ['Maine', 'ME', 'New Hampshire', 'NH', 'Vermont', 'VT', 'Massachusetts', 'MA', 'Rhode Island', 'RI', 'Connecticut', 'CT', 'New York', 'NY', 'New Jersey', 'NJ', 'Pennsylvania', 'PA', 'Delaware', 'DE', 'Maryland', 'MD', 'Virginia', 'VA', 'West Virginia', 'WV', 'North Carolina', 'NC', 'South Carolina', 'SC', 'Georgia', 'GA', 'Florida', 'FL']
    west_usa_keywords = ['California', 'CA', 'Oregon', 'OR', 'Washington', 'WA', 'Alaska', 'AK', 'Hawaii', 'HI', 'Utah', 'UT']
    heartland_usa_keywords = ['Ohio', 'OH', 'Michigan', 'MI', 'Indiana', 'IN', 'Wisconsin', 'WI', 'Illinois', 'IL', 'Minnesota', 'MN', 'Iowa', 'IA', 'Missouri', 'MO', 'North Dakota', 'ND', 'South Dakota', 'SD', 'Nebraska', 'NE', 'Kansas', 'KS', 'Montana', 'MT', 'Wyoming', 'WY', 'Colorado', 'CO', 'New Mexico', 'NM', 'Oklahoma', 'OK', 'Texas', 'TX', 'Arkansas', 'AR', 'Louisiana', 'LA', 'Mississippi', 'MS', 'Alabama', 'AL', 'Kentucky', 'KY', 'Tennessee', 'TN']

    if any(keyword in location for keyword in east_usa_keywords):
        return 'East_USA'
    elif any(keyword in location for keyword in west_usa_keywords):
        return 'West_USA'
    elif any(keyword in location for keyword in heartland_usa_keywords):
        return 'Heartland_USA'
    else:
        return 'None_USA'

# Load OpenAI API key
openai.api_key = load_openai_api_key()

# Read the CSV file into a pandas dataframe
file_name = 'city.csv'
df = pd.read_csv(file_name)

# Print the column names
#print(df.columns)

# Process the second column to extract the location information and determine the location area
df['location_area'] = df.iloc[:, 1].apply(get_location_area)

# Create a new dataframe with the desired columns
# Replace 'company' with the correct column name from the print output
new_df = df[['File', 'location_area']]
#print(new_df)

# Save the new dataframe into a file
new_df.to_csv('Location.csv', index=False)


# In[ ]:




