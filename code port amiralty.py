# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 08:56:33 2024

@author: geofd
"""
import requests
import pandas as pd
import folium

r = requests.get('http://data.portic.fr/api/ports?param=&shortenfields=false&both_to=false&date=1787', auth=('user', 'pass'))
r.status_code
r.headers['content-type']
r.encoding
r.text
r.json()

r_dt = pd.DataFrame(r.json())
r_dt.head()
print(r_dt.columns)

print(len(pd.unique(r_dt.admiralty)))
print(len(pd.unique(r_dt.state_1789_fr)))

print(r_dt.admiralty.unique().size)


r_dt_admiralty = r_dt[pd.isna(r_dt.admiralty)==False]
r_dt.state_1789_fr
grouped_values = r_dt.groupby('admiralty')['ogc_fid'].count()

dt_lr = r_dt[r_dt.admiralty == 'La Rochelle']
dt_fr = r_dt[r_dt.state_1789_fr == 'France']
dt_autre = r_dt[r_dt.state_1789_fr != 'France']

#%% Maop LR
m = folium.Map(location=(46.16308, -1.15222))

#https://fontawesome.com/icons/anchor?f=classic&s=solid&sz=xl&pc=%23171593&sc=%23171593

svg_boat_fr = '''
<svg xmlns="http://www.w3.org/2000/svg" height="24" width="27" viewBox="0 0 576 512"><!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="#171593" d="M320 96a32 32 0 1 1 -64 0 32 32 0 1 1 64 0zm21.1 80C367 158.8 384 129.4 384 96c0-53-43-96-96-96s-96 43-96 96c0 33.4 17 62.8 42.9 80L224 176c-17.7 0-32 14.3-32 32s14.3 32 32 32l32 0 0 208-48 0c-53 0-96-43-96-96l0-6.1 7 7c9.4 9.4 24.6 9.4 33.9 0s9.4-24.6 0-33.9L97 263c-9.4-9.4-24.6-9.4-33.9 0L7 319c-9.4 9.4-9.4 24.6 0 33.9s24.6 9.4 33.9 0l7-7 0 6.1c0 88.4 71.6 160 160 160l80 0 80 0c88.4 0 160-71.6 160-160l0-6.1 7 7c9.4 9.4 24.6 9.4 33.9 0s9.4-24.6 0-33.9l-56-56c-9.4-9.4-24.6-9.4-33.9 0l-56 56c-9.4 9.4-9.4 24.6 0 33.9s24.6 9.4 33.9 0l7-7 0 6.1c0 53-43 96-96 96l-48 0 0-208 32 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-10.9 0z"/></svg>
'''

svg_boat_autre = '''
<svg xmlns="http://www.w3.org/2000/svg" height="24" width="27" viewBox="0 0 576 512"><!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="#931515" d="M320 96a32 32 0 1 1 -64 0 32 32 0 1 1 64 0zm21.1 80C367 158.8 384 129.4 384 96c0-53-43-96-96-96s-96 43-96 96c0 33.4 17 62.8 42.9 80L224 176c-17.7 0-32 14.3-32 32s14.3 32 32 32l32 0 0 208-48 0c-53 0-96-43-96-96l0-6.1 7 7c9.4 9.4 24.6 9.4 33.9 0s9.4-24.6 0-33.9L97 263c-9.4-9.4-24.6-9.4-33.9 0L7 319c-9.4 9.4-9.4 24.6 0 33.9s24.6 9.4 33.9 0l7-7 0 6.1c0 88.4 71.6 160 160 160l80 0 80 0c88.4 0 160-71.6 160-160l0-6.1 7 7c9.4 9.4 24.6 9.4 33.9 0s9.4-24.6 0-33.9l-56-56c-9.4-9.4-24.6-9.4-33.9 0l-56 56c-9.4 9.4-9.4 24.6 0 33.9s24.6 9.4 33.9 0l7-7 0 6.1c0 53-43 96-96 96l-48 0 0-208 32 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-10.9 0z"/></svg>
'''

# Ajout de marqueurs pour chaque point dans le DataFrame
for index, row in dt_lr.iterrows():  # Utilisation de iterrows pour parcourir chaque ligne du DataFrame
    folium.Marker(
        location=[row.y, row.x],  # Latitude et longitude
        tooltip=row.toponyme_standard_en,  # Tooltip affiché au survol
        popup=f"Location: {row.toponyme_standard_en}",  # Popup à afficher lorsque le marqueur est cliqué
        icon=folium.DivIcon(html=svg_boat_fr),  # Utilisation de DivIcon avec le SVG de bateau
    ).add_to(m)
    
m.save('map.html')  # Sauvegarde la carte dans un fichier HTML
# m  # Pour afficher directement la carte dans un notebook Jupyter

#%% Map europe
m = folium.Map()

for index, row in dt_fr.iterrows():  # Utilisation de iterrows pour parcourir chaque ligne du DataFrame
    folium.Marker(
        location=[row.y, row.x],  # Latitude et longitude
        tooltip=row.toponyme_standard_en,  # Tooltip affiché au survol
        popup=f"Location: {row.toponyme_standard_en}",  # Popup à afficher lorsque le marqueur est cliqué
        icon=folium.DivIcon(html=svg_boat_fr),  # Utilisation de DivIcon avec le SVG de bateau
    ).add_to(m)
    
for index, row in dt_autre.iterrows():  # Utilisation de iterrows pour parcourir chaque ligne du DataFrame
    folium.Marker(
        location=[row.y, row.x],  # Latitude et longitude
        tooltip=row.toponyme_standard_en,  # Tooltip affiché au survol
        popup=f"Location: {row.toponyme_standard_en}",  # Popup à afficher lorsque le marqueur est cliqué
        icon=folium.DivIcon(html=svg_boat_autre),  # Utilisation de DivIcon avec le SVG de bateau
    ).add_to(m)
    
m.save('map_2.html')
