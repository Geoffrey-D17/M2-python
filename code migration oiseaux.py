# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 10:37:19 2024

@author: geofd
"""

import geopandas as gpd
import pandas as pd
from geopy.distance import geodesic
from bokeh.plotting import figure, output_notebook, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Category20
from bokeh.transform import factor_cmap
# from bokeh.tile_sources import *
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# Load and prepare data
dt_csv = pd.read_csv('C:/Users/geofd/OneDrive/Documents/Data to info M2/kap_hoegh_gls_complet.csv', sep=';', encoding='utf8')
dt_csv = dt_csv.sort_values(by=['id', 'date'])  # Replace 'date' with actual date column

# Calculate total distance traveled for each 'id'
distances = []

for id_val, group in dt_csv.groupby('id'):
    group = group.reset_index(drop=True)
    total_distance = 0
    for i in range(1, len(group)):
        coord1 = (group.loc[i-1, 'clean_lat'], group.loc[i-1, 'clean_long'])
        coord2 = (group.loc[i, 'clean_lat'], group.loc[i, 'clean_long'])
        distance = geodesic(coord1, coord2).kilometers
        total_distance += distance
    distances.append({'id': id_val, 'total_distance_km': total_distance})

# Merge distance data back into main DataFrame
distance_df = pd.DataFrame(distances)
dt_csv = dt_csv.merge(distance_df, on='id')


# Prepare color mapping for each unique 'id'
unique_ids = dt_csv['id'].unique()
num_ids = len(unique_ids)

colormap = plt.cm.seismic
color_palette = [mcolors.rgb2hex(colormap(i / num_ids)) for i in range(num_ids)]
color_map = {unique_ids[i]: color_palette[i] for i in range(num_ids)}
dt_csv['color'] = dt_csv['id'].map(color_map)


world = gpd.read_file('C:/Users/geofd/OneDrive/Documents/Data to info M2/110m_physical/ne_110m_coastline.shp')
world = world.to_crs(epsg=4326)  # Convert to Web Mercator (EPSG:3857)

# Create GeoDataFrame for your points and convert them to Web Mercator
source = gpd.GeoDataFrame(dt_csv, geometry=gpd.points_from_xy(dt_csv['clean_long'], dt_csv['clean_lat']))
# source = source.to_crs(epsg=3857)  # Convert points to Web Mercator

# Create a Bokeh figure
p = figure(title="Map of Individuals with Distance Traveled", width=800, height=600)

# Plot the world map shapefile
for _, row in world.iterrows():
    p.line(x=row['geometry'].xy[0], y=row['geometry'].xy[1], line_width=0.5, color='black')

# Create a ColumnDataSource for your points (ensure the data is in Web Mercator)
source_bokeh = ColumnDataSource(data=dict(
    lon=source.geometry.x,  # Get the x (longitude) coordinates in Web Mercator
    lat=source.geometry.y,  # Get the y (latitude) coordinates in Web Mercator
    color=source['color'],   # Assuming 'color' column exists in your source
    id=source['id'],         # Assuming 'id' column exists in your source
    distance=source['total_distance_km']  # Assuming 'total_distance_km' exists
))

# Add tooltips
hover = HoverTool(tooltips=[("ID", "@id"), ("Distance (km)", "@distance")])
p.add_tools(hover)

# Plot points for each 'id'
p.circle('lon', 'lat', source=source_bokeh, color='color', size=6, legend_field='id')

# Color map by unique id
p.legend.title = 'Individual ID'
p.legend.label_text_font_size = '8pt'
p.legend.location = 'top_left'

# Show the plot
show(p)
