# %% 
# import necesary libraries
import requests
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# %%
# create a function to get the data from the API
crime_data_NYC = 'https://data.cityofnewyork.us/resource/5uac-w243.json'

def get_data(url):
    response = requests.get(url) # Telling requests to get the data from the url, it will package the information in the response variable
    # error handling
    try:
        response.raise_for_status()
        # raise an exception if the request fails
    except requests.exceptions.HTTPError as err:
        return "Error: " + str(err)
    
    # if the status code is 200, then the request was successful
    raw_data = response.json() # the data is in json format

    # returns a list of dictionaries, so lets return just the dictionaries
    parsed_data = {}
    for index, item in enumerate(raw_data):
        # key is the index of the dictionary from the list, value is the dictionary itself
        parsed_data[index] = item

    return parsed_data

data = get_data(crime_data_NYC)

# %%
data
# %%
keys_to_keep = ['cmplnt_num', 'cmplnt_fr_dt', 'crm_atpt_cptd_cd', 
                'juris_desc', 'law_cat_cd', 'loc_of_occur_desc', 
                'ofns_desc', 'susp_age_group', 'susp_race', 'susp_sex', 
                'vic_age_group', 'vic_race', 'vic_sex', 'latitude', 'longitude']
# delete keys if its not in keys_to_keep
new_list = []
for k, v in data.items():
    for k1, v2 in v.items():
        if (k1 in keys_to_keep):
            new_list.append(k1)
            new_list.append(v2)
# %%
from collections import defaultdict # to create a dictionary with the current values
# for every 2 items in the list create a list of tuples
new_tuple = []
for i in range(0, len(new_list), 2):
    new_tuple = new_tuple + [(new_list[i], new_list[i+1])]

final = defaultdict(list) # final dataset
for k, v in new_tuple:
    final[k].append(v)

# %%
# quick summary of the data dimensions
for index, item in enumerate(final):
    print(f'{index}: {item} - {len(final[item])}') # pandas must have equal number of rows and columns so we have to transpose the data first
# %%
# put the data into a dataframe with the orientation as index
df = pd.DataFrame.from_dict(final, orient='index')
# replace the None values as UNKNOWN 
df = df.fillna(value='UNKNOWN')
# Transpose the dataframe
df = df.T
# %%
# display the dataframe
df

# %%