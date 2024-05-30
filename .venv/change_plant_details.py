'''
Code to change "weed potential" duplicated name
'''
import os
import csv
import pandas as pd

# Function to insert "related to" plant"
def insert_related_to_plant(directory):
    for filename in os.listdir(directory):
        df=pd.read_csv(f"{directory}/{filename}")
        df.iloc[-1, df.columns.get_loc('Attributes')] ="Weed Potencial Description"
        #df = df.iloc[:-1 , :]
        df.drop('Unnamed: 0', axis=1, inplace=True)
        df.to_csv(f"{directory}/{filename}")


# Directory to search files in
directory = './plant_details_folder'


# insert "related to" plant"
insert_related_to_plant(directory)

