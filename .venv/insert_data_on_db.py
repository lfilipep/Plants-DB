import os
import csv
import json
import sqlite3

# Define the directory containing the files
plant_details_folder = './plant_details_folder'
related_plants_folder = './related_plants_folder'

# Define the database connection and cursor
conn = sqlite3.connect('plants_db.db')
cursor = conn.cursor()


# Function to insert data into table_a
def insert_into_table_plant_details(latim_name, common_name, family, us_hardiness, hazards, habitats, range, edible_rate, other_uses_rate, weed_potencial, med_rating, care_info,
                                    imgs, summary, physic_char_synonyms, plant_habitat, edible_parts, edible_uses, edible_desc, medic_uses, medic_desc, other_uses, other_uses_desc,
                                    special_uses, special_uses_desc, cult_details, cult_details_desc, plant_propag, other_names, nat_plant_search, found_in, weed_pot_desc):
    cursor.execute('''INSERT INTO Plant_Details (Latin_name, Common_name, Family, USDA_hardiness,
                   Known_Hazards, Habitats, Range, Edibility_Rating, Other_Uses_Rating, Weed_Potential,
                   Medicinal_Rating, Care_info, Plant_images, Summary, Physical_Characteristics,
                   Synonyms, Plant_Habitats, Edible_Parts, Edible_Uses, Edible_Description, Medicinal_Uses,
                   Medicinal_Description, Other_Uses, Other_Uses_Description, Special_Uses, Special_Uses_Description,
                   Cultivation_Details, Cultivation_Details_Description, Plant_Propagation, Other_Names,
                   Native_Plant_Search, Found_In, Weed_Potential_Description) VALUES (?, ?, ?, ?, ?, ?,
                   ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (latim_name, common_name, family, us_hardiness, hazards, habitats, range, 
                    edible_rate, other_uses_rate, weed_potencial, med_rating, care_info, imgs, summary, physic_char_synonyms, plant_habitat, edible_parts, edible_uses, edible_desc,
                    medic_uses, medic_desc, other_uses, other_uses_desc, special_uses, special_uses_desc, cult_details, cult_details_desc, plant_propag, other_names, nat_plant_search,
                    found_in, weed_pot_desc))
    return cursor.lastrowid

# Function to insert data into table_b
def insert_into_related_plants(latim_name, common_name, habitat, height, hardiness, growth, soil, shade, moisture, edible,
                               medicinal, other, related_to):
    cursor.execute('''INSERT INTO Related_plants (Latin_name, Common_name, Habitat, Height, Hardiness, Growth, Soil, Shade,
                   Moisture, Edible, Medicinal, Other, Related_to) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (latim_name, common_name, habitat, height, hardiness, growth, soil, shade, moisture, edible, medicinal,
                   other, related_to))

# Process CSV files and insert into table plant_details
for filename in os.listdir(plant_details_folder):
    if filename.endswith('.csv'):
        with open(os.path.join(plant_details_folder, filename), 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                for key, value in row.items():
                    print(key)
                    #table_plants_details_id = insert_into_table_plant_details(row['name'], row['value'])
                    #conn.commit()

# Process JSON files and insert into table_b
for filename in os.listdir(related_plants_folder):
    if filename.endswith('.csv'):
        with open(os.path.join(related_plants_folder, filename), 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                for key, value in row.items():
                    print(key)
                    #table_related_plants_id = insert_into_related_plants(row['name'], row['value'])
                    #conn.commit()

# Close the database connection
conn.close()
