'''
Code to change "weed potential" duplicated name
'''
import os
import csv
import pandas as pd

# Function to insert "related to" plant"
def change_cell_value(directory):
    for filename in os.listdir(directory):
        df=pd.read_csv(f"{directory}/{filename}")
        #df.iloc[-1, df.columns.get_loc('Attributes')] ="Weed Potencial Description"
        #df = df.iloc[:-1 , :]
        df.drop(['Unnamed: 0','age'], axis=1, inplace=True)
        df.to_csv(f"{directory}/{filename}")


def transpose_df(directory):
     for filename in os.listdir(directory):
        df=pd.read_csv(f"{directory}/{filename}", header=None, index_col=1)
        df=df[1:]
        df.drop(0, axis=1, inplace=True)
        df = df.transpose()
        df.reset_index(drop=True, inplace=True)
        df.to_csv(f"{directory}/{filename}")
        
# Directory to search files in
directory = './plant_details_folder'


# insert "related to" plant"
#change_cell_value(directory)
transpose_df(directory)
