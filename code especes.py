# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 10:59:48 2024

@author: geofd
"""

import requests
import pandas as pd
from difflib import get_close_matches

url ="https://www.marinespecies.org/rest/AphiaRecordByAphiaID/138675"
r = requests.get(url)
data = r.json()
dt = pd.read_excel("C:/Users/geofd/OneDrive/Documents/Data to info M2/Table_espece_UTF8_simplifie.xlsx", sheet_name= "Espece_incomplet")

def create_mapping(data_keys, dt_columns, threshold=0.6):
    mapping = {}
    for key in data_keys:
        # Trouver les colonnes les plus proches de la clé en fonction de la similitude des noms
        match = get_close_matches(key, dt_columns, n=1, cutoff=threshold)
        if match:
            mapping[key] = match[0]  # Associer la clé à la colonne la plus similaire
    return mapping

data_keys =data.keys()
dt_columns = dt.columns 
mapping = create_mapping(data_keys, dt_columns)

print(mapping)

for index, row in dt.iterrows():
    aphia_id = row['aphiaid_accepted']  # Assurez-vous que le nom de la colonne est correct

    url = f"https://www.marinespecies.org/rest/AphiaRecordByAphiaID/{aphia_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()

        for key, column in mapping.items():
            if key in data: 
                dt.at[index, column] = data[key]

dt.to_excel("Updated_Table_espece.xlsx", index=False)

