'''
Code to insert "related to" plant on "related plants" files
'''
import os
import csv
import pandas as pd

# Function to insert "related to" plant"
def insert_related_to_plant(directory):
    for filename in os.listdir(directory):
        related_to_plant = filename.replace("related plants.csv", "").strip()
        df=pd.read_csv(f"{directory}/{filename}")
        #print(f"plant: {related_to_plant}-{df.shape[0]}")
        df['Related To'] = related_to_plant
        df.drop('Unnamed: 0', axis=1, inplace=True)
        df.to_csv(f"{directory}/{filename}")


# Directory to search files in
directory = './related_plants_folder'


# insert "related to" plant"
insert_related_to_plant(directory)

