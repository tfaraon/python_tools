#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 09:38:58 2024

@author: tfrn
"""

import Xbeach_reader as XBr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# File paths
XB_output = '/home/tfrn/Documents/Stage_TDV/XBeach/Calibration/2D/2022/Test_19/Tideloc/xboutput.nc'
XB_xgrid = "/home/tfrn/Documents/Stage_TDV/XBeach/Calibration/2D/2022/Test_19/Tideloc/x.grd"
transects_folder = '/home/tfrn/Documents/Stage_TDV/Terrain/Transects'

# Load XB data
XB_data = XBr.XB_Loader(XB_output)
X = pd.read_csv(XB_xgrid, delim_whitespace=True, header=None).iloc[0].values

# Transect positions 
transects_position = {
    'Transect 1': 338,
    'Transect 2': 306,
    'Transect 3': 273,
    'Transect 4': 229,
    'Transect 5': 200,
    'Transect 6': 138,
    'Transect 7': 114
}

# Initial and final bed levels from XBeach data
zb_start = XB_data.zb[0, :, :].data
zb_end = XB_data.zb[-1, :, :].data

# Number of transects
num_transects = len(transects_position)

# Create subplots for initial and final bed levels
fig1, axs1 = plt.subplots(num_transects, 1, figsize=(10, 3*num_transects), sharex=True)

# Create subplots for differential bed levels
fig2, axs2 = plt.subplots(num_transects, 1, figsize=(10, 3*num_transects), sharex=True)

# Plot data for each transect
for i, (transect_name, transect_pos) in enumerate(transects_position.items()):
    # Extract data for the specific transect position
    zb_start_transect = zb_start[transect_pos,:]
    zb_end_transect = zb_end[transect_pos,:]
    
    # Compute distances using the X variable
    distances = X[:len(zb_start_transect)]
    
    # Plot initial and final bed levels
    axs1[i].plot(distances, zb_start_transect, linestyle='-', marker='o', markersize=1, label='Start')
    axs1[i].plot(distances, zb_end_transect, linestyle='-', marker='x', markersize=1, label='End')
    axs1[i].set_ylabel(f"{transect_name}")
    axs1[i].legend()
    axs1[i].invert_xaxis()
    # Plot differential bed level
    zb_diff = zb_end_transect - zb_start_transect
    axs2[i].plot(distances, zb_diff, linestyle='-', marker='o', markersize=1, label='End - Start')
    axs2[i].set_ylabel(f"{transect_name}")
    axs2[i].invert_xaxis()
# Set common x-labels
axs1[-1].set_xlabel("Distance (m)")
axs2[-1].set_xlabel("Distance (m)")


# Add arrows and annotations
last_ax1 = axs1[-1]  # Dernier plot de la première figure
last_ax2 = axs2[-1]  # Dernier plot de la deuxième figure

arrow_props = dict(facecolor='black', arrowstyle='<|-|>', linewidth=1.5)

# Annotation pour "Mer" à droite sur la première figure
last_ax1.annotate('Mer', xy=(1, -0.25), xycoords='axes fraction', fontsize=12,
                  xytext=(1.02, -0.25), textcoords='axes fraction',
                  ha='left', va='center',
                  arrowprops=dict(arrowstyle='<|-', linewidth=1.5, color='black'))

# Annotation pour "Lagune" à gauche sur la première figure
last_ax1.annotate('Lagune', xy=(0, -0.25), xycoords='axes fraction', fontsize=12,
                  xytext=(-0.02, -0.25), textcoords='axes fraction',
                  ha='right', va='center')

# Annotation pour "Mer" à droite sur la deuxième figure
last_ax2.annotate('Mer', xy=(1, -0.25), xycoords='axes fraction', fontsize=12,
                  xytext=(1.02, -0.25), textcoords='axes fraction',
                  ha='left', va='center',
                  arrowprops=dict(arrowstyle='<|-', linewidth=1.5, color='black'))

# Annotation pour "Lagune" à gauche sur la deuxième figure
last_ax2.annotate('Lagune', xy=(0, -0.25), xycoords='axes fraction', fontsize=12,
                  xytext=(-0.02, -0.25), textcoords='axes fraction',
                  ha='right', va='center')

