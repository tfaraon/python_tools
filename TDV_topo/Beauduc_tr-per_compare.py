#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 14:54:47 2024

@author: tfrn
"""
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np


Topo_continue = ["/home/tfrn/Documents/Stage_TDV/Terrain/20240307_Beauduc/GIS/Transect_3.shp",
                 "/home/tfrn/Documents/Stage_TDV/Terrain/20240307_Beauduc/GIS/Transect_4.shp"]

Topo_perche =  ["/home/tfrn/Documents/Stage_TDV/Terrain/20240307_Beauduc/GIS/Transect_3_perche.shp",
                 "/home/tfrn/Documents/Stage_TDV/Terrain/20240307_Beauduc/GIS/Transect_4_perche.shp"]

donnees_continue = []
donnees_perche =  []
for i in Topo_continue:
    data = gpd.read_file(i)
    donnees_continue.append(data)

for i in Topo_perche:
    data = gpd.read_file(i)
    donnees_perche.append(data)

fig, axs = plt.subplots(len(Topo_continue), 2, figsize=(12, len(Topo_continue)*5), sharex=True)

for i, (data_continue, data_perche) in enumerate(zip(donnees_continue, donnees_perche)):
    # Trouver le point le plus au nord pour les données de Topo_continue
    northernmost_point_continue = data_continue.geometry.iloc[data_continue.geometry.y.idxmax()]
    x_ref_continue, y_ref_continue = northernmost_point_continue.x, northernmost_point_continue.y
    
    # Calculer la distance de chaque point par rapport au point le plus au nord pour Topo_continue
    distances_continue = np.sqrt((data_continue.geometry.x - x_ref_continue)**2 + (data_continue.geometry.y - y_ref_continue)**2)
    
    axs[i, 0].plot(distances_continue, data_continue['field_4'], linestyle='', marker='o', markersize=1)
    axs[i, 0].set_title(f"Topo_continue {i+1}")
    axs[i, 0].set_ylabel('Altitude (m)')

    # Trouver le point le plus au nord pour les données de Topo_perche
    northernmost_point_perche = data_perche.geometry.iloc[data_perche.geometry.y.idxmax()]
    x_ref_perche, y_ref_perche = northernmost_point_perche.x, northernmost_point_perche.y
    
    # Calculer la distance de chaque point par rapport au point le plus au nord pour Topo_perche
    distances_perche = np.sqrt((data_perche.geometry.x - x_ref_perche)**2 + (data_perche.geometry.y - y_ref_perche)**2)
    
    axs[i, 1].plot(distances_perche, data_perche['Z'], linestyle='', marker='o', markersize=1)
    axs[i, 1].set_title(f"Topo_perche {i+1}")
    axs[i, 1].set_ylabel('Altitude (m)')

for ax in axs.flat:
    ax.set_xlabel('Distance par rapport au point le plus au nord (m)')
plt.tight_layout()
plt.show()