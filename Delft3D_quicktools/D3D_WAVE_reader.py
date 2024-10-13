#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 10:59:09 2023

@author: tfaraon
"""

import os
from netCDF4 import Dataset
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm

#%% Fonctions

class D3D_Wave_Loader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.dataset = Dataset(file_path, 'r')

        # Meshgrids : variables de structure
        self.time = self.dataset.variables["time"][:]
        self.x = self.dataset.variables["x"][:]
        self.y = self.dataset.variables["y"][:]
        
        #Variables de sortie de modèle
        # Ajouter les autres variablesquand j'en aurai besoin
        self.depth = self.dataset.variables["depth"][:]
        self.period = self.dataset.variables["period"][:]
        self.dir = self.dataset.variables["dir"][:]
        self.setup = self.dataset.variables["setup"][:]
        self.hs = self.dataset.variables["hsign"][:]
        self.wlength = self.dataset.variables["wlength"][:]
       
    def explore_data(self):
            
        """ Permet de visualiser les variables disponibles dans le NetCDF"""
        
        print("Variables disponibles :")
        print(self.dataset.variables)
        
    def close(self):
        self.dataset.close()
        
def plot_sub(var):
    """Fonction pour tracer les variables sous forme de subplots pour voir leur évolution temporelle"""
    
    num_plots = len(var)  # Nombre de plots à afficher
    num_cols = 4  # Nombre de colonnes fixé
    
    num_rows = (num_plots + num_cols - 1) // num_cols  # Calcul du nombre de lignes en fonction du nombre de plots
    
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(12, 6))  # Création de la figure avec la taille adaptée
    
    for i, j in enumerate(var):
        row = i // num_cols
        col = i % num_cols
        axs[row, col].matshow(j)
        axs[row, col].set_title(f"Time : {i+1}")  # Titre pour chaque subplot
        
    # Cacher les sous-graphiques restants s'il y en a moins que la capacité maximale
    for i in range(num_plots, num_rows * num_cols):
        axs[i // num_cols, i % num_cols].axis('off')
    
    plt.tight_layout()
    plt.show()


def map_data(X,Y, var):
    """plot la première valeur du dataset donné"""
    
    fig, ax = plt.subplots()
    surf = ax.pcolormesh(X,Y,var[0])
    fig.colorbar(surf, shrink=0.5, aspect=5)


def surf_map_data(x,y,var):
    
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    surf = ax.plot_surface(x, y, var[0], cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    ax.invert_zaxis
    fig.colorbar(surf, shrink=0.5, aspect=5)
    
def plot_profils(dataset, vartoplot):
    prof_x = dataset.depth[:, :, 0:30]
    profils = -prof_x[:, 30]
    
    if hasattr(dataset, vartoplot):
        prof_vartoplot = getattr(dataset, vartoplot)[:, :, 0:30]
        profils_vartoplot = prof_vartoplot[:, 30]
    else:
        print(f"Variable '{vartoplot}' not found in the dataset.")
        return

    fig, axs = plt.subplots(4, 2, figsize=(12, 6))
    
    num_rows = 4
    num_cols = 2
    
    for i in range(num_rows * num_cols):
        row = i // num_cols
        col = i % num_cols
        
        if i < len(profils):
            ax1 = axs[row, col]
            ax1.plot(profils[i], label='Profils')
            ax1.set_xlabel('Crossshore distance')
            ax1.set_ylabel('Profils')
            
            if i < len(profils_vartoplot):
                ax2 = ax1.twinx()
                ax2.plot(profils_vartoplot[i], color='orange', label='Profils_hs')
                ax2.set_ylabel('Profils_hs', color='orange')
                ax2.tick_params(axis='y', labelcolor='orange')
        else:
            axs[row, col].axis('off')
    
    plt.tight_layout()
    plt.show()
    
#%% Exemple d'utilisation

# Wave_file = "/home/tfaraon/Documents/Cours/delft3D/Result/Hs_1_fp_0.1_eta_0_hL_10_hR_0.1_LR_100_WC_0_NR_1_CdR_0.09_CdL_0.01/wavm-synthetic.nc"
# WAVE = D3D_Wave_Loader(Wave_file)



# Accès aux variables
# print(D3D.depth)
# print(D3D.hs)

# Fermeture du fichier à la fin
#D3D.close()

#HS0 = D3D.hs[0]