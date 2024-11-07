# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 10:15:15 2024

@author: geofd
"""

from flask import Flask,  render_template, request
import requests
import pandas as pd
import json
import folium

app = Flask(__name__)

def get_data() : 
    #try to execute this function only once
    print("getting data from server")
    url = "https://psmsl.org/data/gnssir/data/sites.json"
    r = requests.get(url)
    data = r.json()
    #Convert representation of data : from json to dataframe 
    df = pd.DataFrame(data).T
    return df

def create_amap(param):
    ports_filt = ports
    if param != None:
        # Filtrer le dataframe sur le pays
        ports_filt = ports[ports.CountryCode == param]
    
    # Centrer sur 49.49437, 0.107929
    m = folium.Map(location=(49.49437, 0.107929), zoom_start=4, tiles="cartodb positron")

    ## add markers for chef-lieux 
    group_1 = folium.FeatureGroup("ports").add_to(m)

    popup_content = '<table><tr><td>Nom</td><td>{0}</td></tr><tr><td>Code</td><td>{1}</td></tr><tr><td>Pays</td><td>{2}</td></tr><tr><td>Fournisseur</td><td>{3}</td></tr></table>'

    for index, row in ports_filt.iterrows() :
        #position des markers  : [latitude, longitude]
        folium.Marker(
            location=[row.Latitude, row.Longitude], 
            tooltip=row.Name,
            popup=popup_content.format(row.Name, row.Code, row.CountryCode, row.provider),
            icon=folium.Icon(color="green"),
        ).add_to(group_1)
        
    if not ports_filt.empty:
        bounds = [[ports_filt['Latitude'].min(), ports_filt['Longitude'].min()], [ports_filt['Latitude'].max(), ports_filt['Longitude'].max()]]
        m.fit_bounds(bounds)

    folium.LayerControl().add_to(m)
    return m

@app.route('/map_template')
def toto():
    country = request.args.get("pays")
    print("parametre lu")
    print(country)
    
    unique_countries = ports['CountryCode'].unique().tolist()

    ports_filt = ports
    if country:
        # Filter the dataframe on the chosen country
        ports_filt = ports[ports.CountryCode == country]

    m = create_amap(country)
    return render_template('portic_map_2.html', msg=m.get_root()._repr_html_(), y=ports_filt.to_html(), unique_countries=unique_countries)


if __name__ == '__main__':
    ports = get_data()
    app.run(debug=True, port=5000, use_reloader=False)