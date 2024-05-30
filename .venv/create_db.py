import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('plants_db.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create the first table
cursor.execute('''
               CREATE TABLE IF NOT EXISTS Plant_Details (
                    Latin_name TEXT PRIMARY KEY NOT NULL,
                    Common_name TEXT NOT NULL,
                    Family TEXT NOT NULL,
                    USDA_hardiness TEXT,
                    Known_Hazards TEXT,
                    Habitats TEXT,
                    Range TEXT,
                    Edibility_Rating TEXT,
                    Other_Uses_Rating TEXT,
                    Weed_Potential TEXT,
                    Medicinal_Rating TEXT,
                    Care_info TEXT,
                    Plant_images TEXT,
                    Summary TEXT,
                    Physical_Characteristics TEXT,
                    Synonyms TEXT,
                    Plant_Habitats TEXT,
                    Edible_Parts TEXT,
                    Edible_Uses TEXT,
                    Edible_Description TEXT,
                    Medicinal_Uses TEXT,
                    Medicinal_Description TEXT,
                    Other_Uses TEXT,
                    Other_Uses_Description TEXT,
                    Special_Uses TEXT,
                    Special_Uses_Description TEXT,
                    Cultivation_Details TEXT,
                    Cultivation_Details_Description TEXT,
                    Plant_Propagation TEXT,
                    Other_Names TEXT,
                    Native_Plant_Search TEXT,
                    Found_In TEXT,
                    Weed_Potential_Description TEXT
                )
            ''')

# Create the second table with a foreign key referencing the first table
cursor.execute('''
               CREATE TABLE IF NOT EXISTS Related_plants(
                    Latin_name TEXT PRIMARY KEY NOT NULL,
                    Common_name TEXT NOT NULL,
                    Habitat TEXT,
                    Height TEXT,
                    Hardiness TEXT,
                    Growth TEXT,
                    Soil TEXT,
                    Shade TEXT,
                    Moisture TEXT,
                    Edible TEXT,
                    Medicinal TEXT,
                    Other TEXT,
                    Related_to TEXT,
                    FOREIGN KEY(Related_to) REFERENCES Plant_Details(Latim_name)
                )
            ''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully!")
