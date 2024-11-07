# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 10:15:15 2024

@author: geofd
"""

from flask import Flask, render_template, request, jsonify
import requests
import pandas as pd
import folium
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import INLINE

app = Flask(__name__)

def get_data(): 
    print("Fetching data from server...")
    url = "https://psmsl.org/data/gnssir/data/sites.json"
    r = requests.get(url)
    data = r.json()
    
    # Convertir le JSON en DataFrame
    df = pd.DataFrame(data).T
    grouped_values = df.groupby('CountryCode')['Name'].count()
    grouped_values.sort_values(ascending=True, inplace=True)
    grouped_values = grouped_values.reset_index()
    
    return df, grouped_values

def create_amap(country_code=None):
    ports_filt = ports if country_code is None else ports[ports.CountryCode == country_code]
    
    # Centrer sur une localisation générale
    m = folium.Map(location=(49.49437, 0.107929), zoom_start=4, tiles="cartodb positron")

    group_1 = folium.FeatureGroup("Ports").add_to(m)
    popup_content = '<table><tr><td>Nom</td><td>{0}</td></tr><tr><td>Code</td><td>{1}</td></tr><tr><td>Pays</td><td>{2}</td></tr><tr><td>Fournisseur</td><td>{3}</td></tr></table>'

    for _, row in ports_filt.iterrows():
        folium.Marker(
            location=[row.Latitude, row.Longitude],
            tooltip=row.Name,
            popup=popup_content.format(row.Name, row.Code, row.CountryCode, row.provider),
            icon=folium.Icon(color="green"),
        ).add_to(group_1)
    
    if not ports_filt.empty:
        bounds = [[ports_filt['Latitude'].min(), ports_filt['Longitude'].min()],
                  [ports_filt['Latitude'].max(), ports_filt['Longitude'].max()]]
        m.fit_bounds(bounds)

    folium.LayerControl().add_to(m)
    return m

@app.route('/map_template', methods=["GET"])
def toto():
    country = request.args.get("pays")
    unique_countries = sorted(ports['CountryCode'].unique().tolist())
    
    ports_filt = ports if not country else ports[ports.CountryCode == country]
    
    # Création de la carte
    m = create_amap(country)
    
    # Création du graphique Bokeh
    fig = figure(
        y_range=grouped_values['CountryCode'].values,
        x_range=(0, round(max(grouped_values.Name.values) * 1.1)),
        height=600, width=900, title="Nombre de stations GNSS par pays",
        toolbar_location=None, tools=""
    )
    fig.hbar(y=grouped_values['CountryCode'].values, right=grouped_values.Name.values, height=0.5, width=0.5)
    fig.ygrid.grid_line_color = None
    fig.xgrid.grid_line_dash = [6, 4]
    fig.xaxis.axis_label = "Total Count"
    fig.yaxis.axis_label_text_font_size = "10pt"
    fig.xaxis.axis_label_text_font_size = "12pt"
    fig.title.text_font_size = "14pt"
    
    script, div = components(fig)
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
    
    return render_template(
        'portic_map_3.html',
        msg=m.get_root()._repr_html_(),
        y=ports_filt.to_html(),
        unique_countries=unique_countries,
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )

@app.route('/update_map', methods=["GET"])
def update_map():
    country = request.args.get('pays')
    m = create_amap(country)
    html_map = m.get_root()._repr_html_()
    html_data = ports[ports.CountryCode == country].to_html() if country else ports.to_html()

    return jsonify(html_map=html_map, html_data=html_data)

if __name__ == '__main__':
    ports, grouped_values = get_data()
    app.run(debug=True, port=5000, use_reloader=False)
