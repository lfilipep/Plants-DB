import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

url = "https://pfaf.org/user/DatabaseSearhResult.aspx?CName="

headers = {"user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"}

file_path = "plants.csv"

file_data = {
    "Latin Name":[],
    "Common Name":[],
    "Habit":[],
    "Height":[],
    "Hardiness":[],
    "Growth":[],
    "Soil":[],
    "Shade":[],
    "Moisture":[],
    "Edible": [],
    "Medicinal":[],
    "Other":[]
}

def file_creator():
    if os.path.exists(file_path):
        print("File exists!")
    else:
        newFile = pd.DataFrame(file_data)
        newFile.to_csv(file_path)
        print(f"Creating file: '{file_path}'.")
            
def get_data(url, headers, file_path):
    plants_file = pd.read_csv(file_path)
    for char_code in range(ord('A'), ord('Z') + 1):
        char = chr(char_code)
        data = requests.get(f"{url}{char}%", headers=headers)
        print(f"Endpoint: {url}{char}%")
        plants_table = pd.read_html(data.text, match=".+")[1].iloc[1:]
        df = [plants_file, plants_table]
        plants_file = pd.concat(df)
        time.sleep(5)
        
    plants_file.drop('Unnamed: 0', axis=1, inplace=True)
    plants_file.to_csv(file_path)


def get_plants_links(url, headers):
    for char_code in range(ord('A'), ord('Z') + 1):
        char = chr(char_code)
        data = requests.get(f"{url}{char}%", headers=headers)
        print(f"Endpoint: {url}{char}%")
        soup=BeautifulSoup(data.text, 'lxml')
        links = soup.find_all('a')
        links = [l.get("href") for l in links]
        links = [l for l in links if 'LatinName=' in l]
    
    links = [l.replace(" ","+") for l in links]
    plants_urls = [f"https://pfaf.org/user/{l}" for l in links]
    return plants_urls

def plant_files(plants_links):
    for index, plant in enumerate(plants_links):
        data = requests.get(plants_links[index], headers=headers)
        print(print(f"Endpoint: {plants_links[index]}"))
        soup = BeautifulSoup(data.text, 'lxml')
        text = soup.get_text()
        #print(text)
            
        
def main():
    #plants = get_plants_links(url, headers)
    #plant_files(plants)
    file_creator()
    get_data(url, headers, file_path)

if __name__ == "__main__":
    main()