import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
from dataclasses import asdict, dataclass, field, fields
import re
from sqlalchemy import create_engine

@dataclass
class Plant:
    Latin_name: str 
    Common_name: str 
    Family: str 
    USDA_hardiness:str | None
    Known_Hazards: str | None
    Habitats: str | None
    Range: str | None
    Edibility_Rating: str | None
    Other_Uses_Rating: str | None
    Weed_Potential: str | None
    Medicinal_Rating: str | None
    Care_info:str | None
    Form: str | None
    Physical_Characteristics: str | None
    Synonyms: str | None
    Plant_Habit: str | None
    Edible_Parts: str | None
    Edible_Uses: str | None
    Edible_Description: str | None
    Medicinal_Uses: str | None
    Medicinal_Description: str | None
    Other_Uses: str | None
    Other_Uses_Description: str | None
    Special_Uses: str | None
    Special_Uses_Description: str | None
    Cultivation_Details: str | None
    Plant_Propagation: str | None
    Other_Names: str | None
    Native_Plant_Search: str | None
    Found_In: str | None
    Weed_Potential_Description: str | None


url = "https://pfaf.org/user/DatabaseSearhResult.aspx?CName="

headers = {"user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"}

pattern = 'Weed Potential|Habitats'

file_path = "plant_profile.txt"

edible_parts = ["root", "roots", "tuber", "tubers", "buld", "bulds", "stem", "stems", "leave", "leaves",
                "flower", "flowers", "fruit", "fruits", "seed", "seeds", "seedpod", "nut", "nuts", "shoot", "shoots"]


diff_plants = ["Impatiens noli-tangere",
"Nephelium ramboutan-ake",
"Veronica anagallis-aquatica",
"Astragalus pictus-filifolius",
"Alisma plantago-aquatica",
"Zanthoxylum clava-herculis",
"Athyrium filix-femina",
"Pyracantha crenato-serrata",
"Capsella bursa-pastoris",
"Legousia speculum-veneris",
"Opuntia ficus-indica",
"Atropa bella-donna",
"Vicia pseudo-orobus",
"Ferula assa-foetida",
"Laurelia novae-zealandiae",
"Paliurus spina-christi",
"Dryopteris filix-mas",
"Adiantum capillus-veneris",
"Vitex agnus-castus",
"Erythronium dens-canis",
"Chenopodium bonus-henricus",
"Aster novi-belgii",
"Lysimachia foenum-graecum",
"Trigonella foenum-graecum",
"Echinochloa crus-galli",
"Lychnis flos-cuculi",
"Oxalis pes-caprae",
"Fimbristylis sub-bispicata",
"Taraxacum kok-saghyz",
"Corylus hybrids & neohybrids"
"Erythrina crista-galli",
"Vaccinium vitis-idaea",
"Arctostaphylos uva-ursi",
"Scorzonera tau-saghyz",
"Coix lacryma-jobi",
"Smilax bona-nox",
"Ribes uva-crispa",
"Asplenium ruta-muraria",
"Aster novae-angliae",
"Thymus herba-barona",
"Carya carolinae-septentrionalis",
"Achillea erba-rotta moschata",
"Hibiscus rosa-sinensis",
"Asplenium adiantum-nigrum",
"Aspidosperma quebracho-blanco",
"Crataegus crus-galli",
"Scandix pecten-veneris",
"Salvia multiorrhiza",
"Raphia palma-pinus"]

def create_db():
    engine = create_engine('sqlite:///plants_db.db')
    return engine

def import_to_db(engine, table_name, df):
    # we can use 'if_exists' with fail or append
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    
def file_creator(file_path):
    if os.path.exists(file_path):
        print("File exists!")
    else:
        file = open(file_path, 'w')
        file.close()


def extract_title(h2_title):
    h2_titles = []
    if h2_title:           
        for h2 in h2_title:
            title = h2.text.strip()
            if (h2.text == "Summary"):
                h2_titles.append(title)
            elif (h2.text == "Physical Characteristics"):
                h2_titles.append(title)
            elif (h2.text == "Synonyms"):
                h2_titles.append(title)                             
            elif (h2.text == "Plant Habitats"):
                h2_titles.append(title)
            elif (h2.text == "Edible Uses"):
                h2_titles.append(title)
            elif (h2.text == "Medicinal Uses"):
                h2_titles.append(title) 
            elif (h2.text == "Other Uses"):
                h2_titles.append(title)        
            elif (h2.text == "Special Uses"):
                h2_titles.append(title)
            elif (h2.text == "Cultivation details"):
                h2_titles.append(title)   
            elif (h2.text == "Plant Propagation"):
                h2_titles.append(title)
            elif (h2.text == "Other Names"):
                h2_titles.append(title) 
            elif (h2.text == "Native Plant Search"):
                h2_titles.append(title)    
            elif (h2.text == "Found In"):
                h2_titles.append(title)
            elif (h2.text == "Weed Potential"):
               h2_titles.append(title)                  
    else:
        print("No H2 attributes found on the webpage.")
        
    return h2_titles 

def extract_text(soup, tag):
    # Extract paragraphs text       
    text = soup.select_one(tag)
    if text:
        # if text.text == "":
        #     print("There's no Text")
        # else:
        #     print(text.text)
        return text    
    else:
        #print("There's no cultivation details info found on the webpage.")    
        return "" 
     

def get_missing_plants_links(plants_links):
    plants = [link.replace(" ","+") for link in plants_links]
    plants_urls = [f"https://pfaf.org/user/Plant.aspx?LatinName={link}" for link in plants]
    print(f"Numero links:{len(plants_urls)} ")
    for plant in plants_urls:
        print(plant)
    return plants_urls


def get_plants_links(url, headers):
    plants_links = []
    for char_code in range(ord('A'), ord('Z') + 1):
        char = chr(char_code)
        data = requests.get(f"{url}{char}%", headers=headers)
        print(f"Endpoint: {url}{char}%")
        soup=BeautifulSoup(data.text, 'lxml')
        links = soup.find_all('a')
        links = [l.get("href") for l in links]
        links = [l for l in links if 'LatinName=' in l]
        for link in links:
            plants_links.append(link)
     
    plants_links = [l.replace(" ","+") for l in plants_links]
    plants_urls = [f"https://pfaf.org/user/{l}" for l in plants_links]
    print(f"Numero links:{len(plants_urls)} ")
    return plants_urls


# def insert_table_rows(links, text, table):
#     aux_list = []
#     for link in links:
#         aux_list.append(f"{link.text}: {link['title']}") 
                    
#     links_desc = ','.join(aux_list)              
#     description = text
#     for character in '\n\r':
#         description = description.replace(character, '')
                         
#     table.loc[len(table)] = ["Other Uses", links_desc]    # adding a row
#     table.loc[len(table)] = ["Other Uses Description", description]    # adding a row 
#     return table

def format_text(text):
    description = text
    for character in '\n\r\t':
        description = description.replace(character, '')
    return description


def plant_files(plants_links):
    plants_edible_uses = []
    plants_edible_parts = []
    links = []
    try:
        for index, plant in enumerate(plants_links):
     
        #for index in range(0,4):
            data = requests.get(plants_links[index], headers=headers)
            # Check if the request was successful (status code 200)
            if data.status_code == 200:
                print(f"Endpoint: {plants_links[index]}")
                soup = BeautifulSoup(data.text, 'lxml')
                #plant_file = pd.read_html(data.text, match=pattern) #match=".+"
                # Extract plant profile data
                plant_table = pd.read_html(data.text, attrs={"class": "table table-hover table-striped"})
                #del plant_table[-1]
                plant_table = plant_table[0][:-1]
                
                # Extract related plants data 
                related_list = soup.select_one("#ContentPlaceHolder1_gvresults")
                # print(related_list.text)
                # print(type(related_list.text))
                # if type(related_list.text) == "<class 'list'>":
                related_plants = pd.read_html(data.text, attrs={"id": "ContentPlaceHolder1_gvresults"})
                related_plants = related_plants[0][:-1]
                
                #Extract plant latin name
                plant_latin_name = extract_text(soup, "#ContentPlaceHolder1_lbldisplatinname").text.split("-")[0].strip()
                
                
                #Save related plants to csv
                related_plants.to_csv(f"./plant_details_folder/{plant_latin_name} related plants.csv") 
                 
                # Insert plant name in related plants table
                #related_plants['Plant Name'] = plant_latin_name
                
                # Change columns order
                # cols = related_plants.columns.tolist()
                # cols = cols[-1:] + cols[:-1]
                # related_plants = related_plants[cols]
                
                 
               
                # Extract care row data
                care_row = soup.select_one("#ContentPlaceHolder1_tblIcons")
               
                if care_row:
                    care_img = []
                                
                    # Extract image links from cells
                    img_tags = care_row.find_all('img')
                    care_img = [img['title'] for img in img_tags]
                    care_img = ",".join(care_img)
                    plant_table.loc[10, 1] = care_img
                    
                    
                    #plant_table.to_csv("plant_table.csv")
               
                else:
                    print("There's no care info attribute found on the webpage.")
                    
                
                if (len(plant_table.columns) > 2):
                    for i in range(2,len(plant_table.columns)):
                        plant_table.drop([i], axis=1, inplace=True)   
                             
                # if 3 in plant_table.columns:
                #     plant_table.drop([2,3], axis=1, inplace=True)
                # else:
                #     plant_table.drop(2, axis=1, inplace=True)
                    
                plant_table = plant_table.rename(columns={0: 'Attributes', 1: 'Description'})    
                     
                plant_name = pd.DataFrame([["Latin Name", plant_latin_name]], columns=plant_table.columns)
                plant_table = pd.concat([plant_name, plant_table], ignore_index=True)
                plant_table = plant_table.sort_index().reset_index(drop=True)
            
                # Extract plants photos data
                plant_photos = soup.select_one("#ContentPlaceHolder1_tblPlantImges")
                if plant_photos:
                    img_tags = plant_photos.find_all('img')
                    plants_img = []
                    for index, img in enumerate(img_tags):
                        if index < 2:
                            plants_img.append(f"https://pfaf.org/{img['src']}")
                            
                    
                    imgs = (", ").join(plants_img)
                    plant_table.loc[len(plant_table)] = ["Plant Images", imgs]  # adding a row   
                    # for img in plants_img:
                    #     print(img)
                    
                    
                                            
                else:
                    print("There's no plant photos found on the webpage.")
                    
                # Extract page subtitles
                h2_title = soup.find_all('h2')
                h2_titles = extract_title(h2_title)  
                 
                # Extract summary text
                if "Summary" in h2_titles:
                    summary_text = extract_text(soup, "#ContentPlaceHolder1_txtSummary")
                    plant_table.loc[len(plant_table)] = ["Summary", format_text(summary_text.text).strip()]  # adding a row   
                           
                # Extract physical characteristics text
                if "Physical Characteristics" in h2_titles:
                    physical_characteristics = extract_text(soup, "#ContentPlaceHolder1_lblPhystatment") 
                    plant_table.loc[len(plant_table)] = ["Physical Characteristics", format_text(physical_characteristics.text).strip()]  # adding a row           
                
                # Extract Synonyms text
                if "Synonyms" in h2_titles:
                    synonyms = extract_text(soup, "#ContentPlaceHolder1_lblSynonyms")
                    plant_table.loc[len(plant_table)] = ["Synonyms", format_text(synonyms.text).strip()]  # adding a row                        
                             
                # Extract plant habitats text
                if "Plant Habitats" in h2_titles:
                    plant_habitats = extract_text(soup, "#ContentPlaceHolder1_lblhabitats")
                    plant_table.loc[len(plant_table)] = ["Plant Habitats", format_text(plant_habitats.text).strip()]  # adding a row     
                     
                       
                # Extract edible uses text
                if "Edible Uses" in h2_titles:
                    text_description_index = 0
                    edible_parts_index = -2
                    edible_uses_index = -2
                    edible_portion_index = -2
                    edible_uses_text_index = 0
                    edible_uses_text_index = 0
                    plants_edible_parts = []
                    plants_edible_uses = []
                    
                    
                    #Get text of edible uses
                    edible_uses = extract_text(soup, "#ContentPlaceHolder1_txtEdibleUses")
                    text = edible_uses.get_text()

                    # Check if Edible Parts, Edible uses and Edible portions exists, and get their positions in the text
                    if ("Edible Parts:" in text):
                        links = edible_uses.find_all('a')
                        edible_parts_index = text.find("Edible Parts:")
                        
                        if ("Edible Uses:" in text):
                            edible_uses_index = text.find("Edible Uses:")
                        
                        if ("Edible portion:" in text):
                             edible_portion_index = text.find("Edible portion:")
                    
                    # Check if there are links, divide them by category and save the items in two list
                    if (len(links) > 0):            
                        for link in links:
                            if link.text.lower() in edible_parts:
                                plants_edible_parts.append(f"{link.text}: {link['title']}")
                            else:
                                plants_edible_uses.append(f"{link.text}: {link['title']}")
                                edible_uses_text_index += len(link.text)
                        
                        edible_parts_text = ",".join(plants_edible_parts)
                        edible_uses_text = ",".join(plants_edible_uses)        
                        plant_table.loc[len(plant_table)] = ["Edible Parts", edible_parts_text]  # adding a row     
                        plant_table.loc[len(plant_table)] = ["Edible Uses", edible_uses_text]    # adding a row 
                                
                    # Find the index where the description begins and write the description to the screen
                    if (edible_parts_index > -1):
                        text_description_index = edible_parts_index + len("Edible Parts:")
                        if (edible_uses_index > -1):
                           if (text_description_index < edible_uses_index):
                               text_description_index = edible_uses_index + len("Edible Uses:")
                        if(edible_portion_index > -1):
                            if (text_description_index < edible_portion_index):
                                text_description_index = edible_portion_index
                    else:
                        text_description_index = 0
                                            
                    if (edible_uses_text_index > 0):        
                        edible_uses_text_index+=1 
                                 
                    plant_table.loc[len(plant_table)] = ["Edible Uses Description", format_text(text[text_description_index+edible_uses_text_index:]).strip()]    # adding a row 
                
                # Extract medical uses text
                if "Medicinal Uses" in h2_titles:
                    medicinal_uses_list = []
                    medical_uses = extract_text(soup, "#ContentPlaceHolder1_txtMediUses")
                    text = medical_uses.get_text()
                    links = medical_uses.find_all('a')
                    
                    for link in links:
                        medicinal_uses_list.append(f"{link.text}: {link['title']}")  
                    
                    medical_uses_desc = ','.join(medicinal_uses_list)              
                    
                    plant_table.loc[len(plant_table)] = ["Medicinal Uses", medical_uses_desc]    # adding a row
                    plant_table.loc[len(plant_table)] = ["Medicinal Uses Description", format_text(text).strip()]    # adding a row 
                                       
                
                # Extract other uses text
                if "Other Uses" in h2_titles:
                    other_uses_list = []
                    link_text = []
                    other_uses = extract_text(soup, "#ContentPlaceHolder1_txtOtherUses")
                    text = other_uses.get_text()
                    links = other_uses.find_all('a')
                    
                    for link in links:
                        other_uses_list.append(f"{link.text}: {link['title']}") 
                        link_text.append(link.text)
                    other_uses_desc = ','.join(other_uses_list)              
                    
                    for word in link_text:
                        text = text.replace(word,"")
                      
                    plant_table.loc[len(plant_table)] = ["Other Uses", other_uses_desc]    # adding a row
                    plant_table.loc[len(plant_table)] = ["Other Uses Description", format_text(text).strip()]    # adding a row 
                                   
                        
                # Extract special uses text
                if "Special Uses" in h2_titles:
                    special_uses_list = []
                    special_uses = extract_text(soup, "#ContentPlaceHolder1_txtSpecialUses")
                    text = special_uses.get_text()
                    links = special_uses.find_all('a')
                    
                    for link in links:
                        special_uses_list.append(f"{link.text}: {link['title']}") 
                    
                    special_uses_desc = ','.join(special_uses_list)              
                     
                    plant_table.loc[len(plant_table)] = ["Special Uses", special_uses_desc]    # adding a row
                    plant_table.loc[len(plant_table)] = ["Special Uses Description", format_text(text).strip()]    # adding a row 
                                 
                
                # Extract cultivation details text
                if "Cultivation details" in h2_titles:
                    cultivation_details_list = []
                    cultivation_details = extract_text(soup, "#ContentPlaceHolder1_txtCultivationDetails")
                    text = cultivation_details.get_text()
                    links = cultivation_details.find_all('a')
                    
                    for link in links:
                        cultivation_details_list.append(f"{link.text}: {link['title']}") 
                    
                    cultivation_details_desc = ','.join(cultivation_details_list)              
        
                    plant_table.loc[len(plant_table)] = ["Cultivation Details", cultivation_details_desc]    # adding a row
                    plant_table.loc[len(plant_table)] = ["Cultivation Details Description", format_text(text).strip()]    # adding a row 
                   
                     
                
                # Extract plant propagation text
                if "Plant Propagation" in h2_titles:
                    plant_propagation = extract_text(soup, "#ContentPlaceHolder1_txtPropagation")
                    plant_table.loc[len(plant_table)] = ["Plant Propagation", format_text(plant_propagation.text).strip()]  # adding a row   
                
                # Extract other names text
                if "Other Names" in h2_titles:
                    paragraph_text = extract_text(soup, "#ContentPlaceHolder1_lblOtherNameText")
                    other_names = paragraph_text.parent.find_previous('p').text
                    plant_table.loc[len(plant_table)] = ["Other Names", other_names.strip()]  # adding a row  
                
                # Extract native plants search text
                if "Native Plant Search" in h2_titles:
                    paragraph_text = soup.find(string=re.compile("Native Plant Search"))
                    native_plant_search = paragraph_text.find_next('p').text
                    plant_table.loc[len(plant_table)] = ["Native Plant Search", native_plant_search.strip()]  # adding a row  
                
                # Extract "found in"  in text
                if "Found In" in h2_titles:
                    paragraph_text = soup.find(string=re.compile("Found In"))
                    found_in = paragraph_text.find_next('p').text
                    plant_table.loc[len(plant_table)] = ["Found In", found_in.strip()]  # adding a row 
                    
                    
                # Extract weed potencial text
                if "Weed Potential" in h2_titles:
                    paragraph_text = extract_text(soup, "#ContentPlaceHolder1_lblWeedPotentialText")
                    weed_potencial = paragraph_text.parent.find_previous('p')
                    plant_table.loc[len(plant_table)] = ["Weed Potencial", format_text(weed_potencial.text).strip()]  # adding a row 
   
                # Save plant table to csv
                plant_table.to_csv(f"./plant_details_folder/{plant_latin_name} details.csv")                             
                                  
            else:
                print(f"Failed to retrieve content from {url}. Status code: {data.status_code}")        
    except Exception as e:
        print(f"An error occurred: {e}")
 
            
     
def main():
    #file_creator(file_path)
    #plants = get_missing_plants_links(diff_plants)
    plants = get_plants_links(url, headers)
    plant_files(plants)

if __name__ == "__main__":
    main()





# def Convert(lst):
#     res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
#     return res_dct
         
# # Driver code
# lst = ['a', 1, 'b', 2, 'c', 3]
# print(Convert(lst))


#Query from a database
# query = "SELECT * FROM table"
# result_df = pd.read_sql(query, engine)


# def parse_item_page(html):
# 	new_item = Item(
# 		name=extract_text(html, "h1#product-page-title"),
# 		item_num=extract_text(html, "span#product-item-number"),
# 		price=extract_text(html, "span#buy-box-product-price"),
# 		rating=extract_text(html, "span.cdr-rating__number_13-5-3")
# 	)
# 	return asdict(new_item)