# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 14:14:36 2024

@author: geofd
"""

import requests
import os

chapters_end = 10

# Créer un dossier pour enregistrer les images
os.makedirs('One_Piece_Images', exist_ok=True)

chapter = 1
page = 1

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

while chapter != chapters_end+1:
    page_num = f'{page:02d}'  # Assure que le numéro de page a deux chiffres
    if page<10:
        pic_url = f'https://www.scan-vf.net/uploads/manga/one_piece/chapters/chapitre-{chapter}/0{page}.webp'
        response = requests.get(pic_url, headers=headers)
    else:
        pic_url = f'https://www.scan-vf.net/uploads/manga/one_piece/chapters/chapitre-{chapter}/{page}.webp'
        response = requests.get(pic_url, headers=headers)
    if response.ok:
        image_path = os.path.join('One_Piece_Images', f'One_Piece_chap_{chapter}_page_{page}.webp')
        with open(image_path, 'wb') as file:
            file.write(response.content)
            print(f"L'image a été enregistrée sous le nom '{image_path}'.")
            page += 1
    else:
        chapter+=1
        page = 1
        
            
