'''
Code to check if is missing plant's files after scraping plants data links
'''

import os
import csv
import pandas as pd

# Function to search for files and filter out those with "related plants"
def search_files(directory):
    file_list = []
    for filename in os.listdir(directory):
        if "related plants" not in filename:
            filename = filename.replace(" details.csv", "").strip()
            file_list.append(filename)
    return file_list

# Function to read a list from a CSV file
def read_csv(file_path):
    #csv_list = []
    df = pd.read_csv(file_path)
    csv_list = df['Latin Name']
    # with open(file_path, newline='') as csvfile:
    #     csvreader = csv.reader(csvfile)
    #     for row in csvreader:
    #         for file in files:
    #             if file not in row:
    #                 csv_list.append(file)
    return csv_list

# Directory to search files in
directory = './plant_details_folder'
# CSV file path
csv_file_path = 'plants.csv'

# Get the list of files without "related plants"
file_names = search_files(directory)

# Read the list from the CSV file
csv_list = read_csv(csv_file_path)

# Compare the two lists
#common_files = set(file_names).intersection(set(csv_list))
different_files = set(csv_list).difference(set(file_names))
different_files = list(different_files)
for file in different_files:
    if file not in file_names:
        print(file)
    
#print("Diferent files:", different_files)

# This will print out the common files between the directory and the CSV file
