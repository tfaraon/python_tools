#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 09:20:56 2024

@author: tfrn
"""

import Xbeach_reader as XBr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.colorbar import ColorbarBase
import matplotlib.colors as mcolors
from tqdm import tqdm

# =============================================================================
# 
# Script pour la lecture du netcdf et le plot des graphs
# 
# Les fonctions de lecture sont dans le script XB_reader
# 
#   Ce script comprend : 
#    
#    - Une animation des transects
#    - Une animation de la hauteur de vagues
#    - Une animation du niveau d'eau
#    - Figures pour le plot 
#
# =============================================================================

#%% Functions

def animate_transects(XB_data, transect, output_path):
    t = XB_data.H.data
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    ax1.set_xlim(0, len(XB_data.zs[0, transect, :]))
    ax2.set_xlim(0, len(XB_data.zs[0, transect, :]))
    ax1.set_ylim(np.min(XB_data.zb), 6)
    ax2.set_ylim(np.min(XB_data.zb), 6)

    time = ax2.annotate(0, xy=(1, 0.5), xytext=(1, 0.5))
    line1, = ax1.plot([], [], lw=1, color='blue') 
    line2, = ax1.plot([], [], lw=1, color='red')
    line3, = ax2.plot([], [], lw=1, color='blue')
    line4, = ax2.plot([], [], lw=1, color='red', label='Bathymétrie instantanée') 

    ax1.plot(XB_data.zb[0, transect, :], 'g--', label='Bathymétrie initiale')
    ax2.plot(XB_data.zb[0, transect, :], 'g--')
    ax2.set_xlabel('Distance (m)')
    ax1.set_ylabel("Niveau d'eau (m)")
    ax2.set_ylabel("Hauteur significative (m)")

    fig.suptitle('Hydrodynamique et variation morphologique')
    fig.legend()
    fig.tight_layout()

    def init():
        line1.set_data([], [])
        line2.set_data([], [])
        line3.set_data([], [])
        line4.set_data([], [])
        return line1, line2, line3, line4

    def animate(i):
        line1.set_data(range(len(XB_data.zs[i, transect, :])), XB_data.zs[i, transect, :])
        line2.set_data(range(len(XB_data.zb[i, transect, :])), XB_data.zb[i, transect, :])
        line3.set_data(range(len(XB_data.H[i, transect, :])), XB_data.H[i, transect, :])
        line4.set_data(range(len(XB_data.zb[i, transect, :])), XB_data.zb[i, transect, :])
        time.set_text(f"Step {i}/{len(XB_data.zs)}")
        return line1, line2, line3, line4

    anim = FuncAnimation(fig, animate, init_func=init, frames=len(XB_data.zs), interval=200, blit=False)
    anim.save(os.path.join(output_path, f'animation_transects_{transect}.gif'), writer='imagemagick')

def plot_2D_variable(X, Y, data, variable_name, cmap='viridis', interval=300, output_path=None):
    fig, ax = plt.subplots()
    im = ax.pcolormesh(X, Y, data[0, :, :], cmap=cmap, animated=True, vmin=data.min(), vmax=data.max())

    def init():
        im.set_array(data[0, :, :])
        return [im]

    def animate(i):
        im.set_array(data[i, :, :])
        return [im]

    anim = FuncAnimation(fig, animate, init_func=init, frames=data.shape[0], interval=interval, blit=True)
    fig.tight_layout()
    if output_path:
        anim.save(output_path, writer='imagemagick')
       
        
def plot_comparison(X, Y, start_bottom, end_bottom, sim_name, output_path, do_zooms=False):
    diff = end_bottom - start_bottom
    colors = [(1, 0, 0), (1, 1, 1), (0, 1, 0)]  # Red -> White -> Green
    nodes = [-5, 0, 5]
    norm_nodes = [(n - min(nodes)) / (max(nodes) - min(nodes)) for n in nodes]
    cmap = LinearSegmentedColormap.from_list('custom_cmap', list(zip(norm_nodes, colors)))
    norm = Normalize(vmin=-2, vmax=2)

    fig, ax = plt.subplots(figsize=(9, 5))
    c = ax.pcolormesh(X, Y, diff, cmap=cmap, norm=norm)
    fig.colorbar(c, ax=ax, label='Différentiel (m)')
    ax.set_xlabel('Distance x (m)')
    ax.set_ylabel('Distance y (m)')

    if do_zooms:
        x1, x2, y1, y2 = 550, 1450, 900, 1300
        axins = ax.inset_axes([0.5, 0.05, 0.47, 0.47], xlim=(x1, x2), ylim=(y1, y2), xticklabels=[], yticklabels=[])
        axins.pcolormesh(X, Y, diff, cmap=cmap, norm=norm)
        axins.set_xlim(x1, x2)
        axins.set_ylim(y1, y2)
        ax.indicate_inset_zoom(axins, edgecolor='black')

    fig.tight_layout()
    fig.savefig(os.path.join(output_path, f'différentiel_bathy_{sim_name}.png'))

    colors_undersea = plt.cm.terrain(np.linspace(0, 0.17, 256))
    colors_land = plt.cm.terrain(np.linspace(0.25, 1, 256))
    all_colors = np.vstack((colors_undersea, colors_land))
    terrain_map = mcolors.LinearSegmentedColormap.from_list('terrain_map', all_colors)
    divnorm = mcolors.TwoSlopeNorm(vmin=-10., vcenter=0.3, vmax=4)

    for bottom, label in zip([start_bottom, end_bottom], ['start', 'end']):
        fig, ax = plt.subplots(figsize=(9, 5))
        c = ax.pcolormesh(X, Y, bottom, cmap=terrain_map, norm=divnorm)
        fig.colorbar(c, ax=ax, label='Altitude')
        ax.set_xlabel('Distance x (m)')
        ax.set_ylabel('Distance y (m)')

        if do_zooms:
            x1, x2, y1, y2 = 550, 1450, 900, 1300
            axins = ax.inset_axes([0.5, 0.05, 0.47, 0.47], xlim=(x1, x2), ylim=(y1, y2), xticklabels=[], yticklabels=[])
            axins.pcolormesh(X, Y, bottom, cmap=terrain_map, norm=divnorm)
            axins.set_xlim(x1, x2)
            axins.set_ylim(y1, y2)
            ax.indicate_inset_zoom(axins, edgecolor='black')

        fig.tight_layout()
        fig.savefig(os.path.join(output_path, f'{label}_bathy_{sim_name}.png'))
        

#%% Run Functions
# Parcourir les sous-dossiers dans le superdossier
superfolder = '/home/tfrn/Documents/Stage_TDV/XBeach/Calibration/2D/2022/Test_19/'


subfolders = [f.path for f in os.scandir(superfolder) if f.is_dir()]

for subfolder in tqdm(subfolders):
    sim_name = os.path.basename(subfolder)
    XB_output = os.path.join(subfolder, 'xboutput.nc')
    if os.path.exists(XB_output):
        # Chargement de la donnée XB brute 
        XB_data = XBr.XB_Loader(XB_output)

        X_grd = pd.read_csv(os.path.join(subfolder, 'x.grd'), delim_whitespace=True).iloc[0,:].to_numpy()
        Y_grd = pd.read_csv(os.path.join(subfolder, 'y.grd'), delim_whitespace=True).iloc[:,1].to_numpy()
        X = 0 - XB_data.get_variable('globalx').data
        Y = XB_data.get_variable('globaly').data

        # Animation transects
        # animate_transects(XB_data, transect=100, output_path=subfolder)

        # # # Plot 2D Hs
        plot_2D_variable(X, Y, XB_data.H, 'Hs', cmap='viridis', interval=300, output_path=os.path.join(subfolder, 'animation_Hs.gif'))

        # # # Plot 2D Zs
        plot_2D_variable(X, Y, XB_data.zs, 'Zs', cmap='viridis', interval=300, output_path=os.path.join(subfolder, 'animation_zs.gif'))

        # Plot comparison
        plot_comparison(X, Y, XB_data.zb[0,:,:].data, XB_data.zb[-1,:,:].data, sim_name, subfolder)

        plt.close('all')
        XB_data.close()
