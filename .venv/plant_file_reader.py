import os

file_path = "plant_profile.txt"


if os.path.exists(file_path):
    with open(file_path, 'r') as f:
        dataFile = f.read()
        edible_uses_index = dataFile.find("Edible Uses:")
        edible_parts_index = dataFile.find("Edible portion:")
        #print(f"uses: {uses}")
        print(dataFile[:edible_uses_index])
        print(dataFile[edible_uses_index:edible_parts_index])
        print(dataFile[edible_parts_index:])
        # for row in dataFile:
        #     print(row)
else:
    print("File not exists!")