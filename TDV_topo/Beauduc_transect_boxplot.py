#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 14:21:31 2024

@author: tfrn
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

chemins_transects = ["/home/tfrn/Documents/Stage_TDV/Terrain/20240321_Beauduc/GIS/Transects/20240321_Transect_1.shp",
                     "/home/tfrn/Documents/Stage_TDV/Terrain/20240321_Beauduc/GIS/Transects/20240321_Transect_2.shp",
                     "/home/tfrn/Documents/Stage_TDV/Terrain/20240321_Beauduc/GIS/Transects/20240321_Transect_3.shp",
                     "/home/tfrn/Documents/Stage_TDV/Terrain/20240321_Beauduc/GIS/Transects/20240321_Transect_4.shp",
                     "/home/tfrn/Documents/Stage_TDV/Terrain/20240321_Beauduc/GIS/Transects/20240321_Transect_5.shp",
                     "/home/tfrn/Documents/Stage_TDV/Terrain/20240321_Beauduc/GIS/Transects/20240321_Transect_6.shp",
                     "/home/tfrn/Documents/Stage_TDV/Terrain/20240321_Beauduc/GIS/Transects/20240321_Transect_7.shp"
                     ]

donnees_shapefile = []

for i in chemins_transects:
    data = gpd.read_file(i)
    donnees_shapefile.append(data)
  
#%% boxplots

fig, ax = plt.subplots(figsize=(20, 7))
data_for_boxplots = []
for data in donnees_shapefile:
    if 'field_4' in data.columns:
        data_for_boxplots.append(data['field_4'].dropna().values)
    elif 'H_corr' in data.columns:
        data_for_boxplots.append(data['H_corr'].dropna().values)
        
ax.boxplot(data_for_boxplots)
ax.set_title("Boxplots des données d'altitude")
ax.set_xlabel('Transects')
ax.set_ylabel('Z (m)')
ax.set_xticklabels([f'Transect {i+1}' for i in range(len(chemins_transects))])

#%% subplots
fig, axs = plt.subplots(len(chemins_transects), 1, figsize=(10, len(chemins_transects)*3), sharex=True)
mean_list = []
if 'field_4' in data.columns:
    for i, (data, ax) in enumerate(zip(donnees_shapefile, axs)):
        # Trouver le point le plus au nord
        northernmost_point = data.geometry.iloc[data.geometry.y.idxmax()]
        x_ref, y_ref = northernmost_point.x, northernmost_point.y
        
        # Calculer la distance de chaque point par rapport au point le plus au nord
        distances = np.sqrt((data.geometry.x - x_ref)**2 + (data.geometry.y - y_ref)**2)
        ax.plot(distances, data['field_4'], linestyle='', marker='o', markersize=1)
        ax.set_ylabel(f"Transect {i+1}")

elif 'H_corr' in data.columns:
    for i, (data, ax) in enumerate(zip(donnees_shapefile, axs)):
        # Trouver le point le plus au nord
        northernmost_point = data.geometry.iloc[data.geometry.y.idxmax()]
        x_ref, y_ref = northernmost_point.x, northernmost_point.y
        
        # Calculer la distance de chaque point par rapport au point le plus au nord
        distances = np.sqrt((data.geometry.x - x_ref)**2 + (data.geometry.y - y_ref)**2)
        ax.plot(distances, data['H_corr'], linestyle='', marker='o', markersize=1)
        ax.set_ylabel(f"Transect {i+1}")
        mean_list.append(data['H_corr'].mean())
        print(np.mean(mean_list))

plt.xlabel('Distance par rapport au point le plus au nord (en unités de coordonnées)')
plt.tight_layout()
plt.show()

