#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 12:15:03 2023

@author: tfaraon

ALlows to read data from Delft3D netcdf using a class and functions to plot
"""

import os
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

class D3D_Flow_Loader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.dataset = Dataset(file_path, 'r')

        # Meshgrids : variables de structure
        self.time = self.dataset.variables["time"][:]
        self.x = self.dataset.variables["XCOR"][:]
        self.y = self.dataset.variables["YCOR"][:]
        
        #Variables de sortie de modèle
        # Ajouter les autres variablesquand j'en aurai besoin
        self.S1 = self.dataset.variables["S1"][:] #Water-level in zeta point
        self.U1 = self.dataset.variables["U1"][:] #U-velocity per layer in U-point (Eulerian)
        self.V1 = self.dataset.variables["V1"][:]
        self.UPRESS = self.dataset.variables["MOM_UPRESSURE"][:] #Pressure term (u point)
        self.VPRESS = self.dataset.variables["MOM_VPRESSURE"][:]
        self.UBEDSHEAR = self.dataset.variables["MOM_UBEDSHEAR"][:] #Bed shear term (u point)
        self.VBEDSHEAR = self.dataset.variables["MOM_VBEDSHEAR"][:]
        self.UWAVES = self.dataset.variables["MOM_UWAVES"][:] #Wave forces term (u point)
        self.VWAVES = self.dataset.variables["MOM_VWAVES"][:]
        self.TAUSKI = self.dataset.variables["TAUKSI"][:] #Bottom stress in U-point
        self.TAUETA = self.dataset.variables["TAUETA"][:]
        self.TAUMAX = self.dataset.variables["TAUMAX"][:]
        
    def explore_data(self):
        
        """ Permet de visualiser les variables disponibles dans le NetCDF"""
        
        print("Variables disponibles :")
        print(self.dataset.variables)

    def close(self):
        self.dataset.close()
        
        

def map_data(FLOW,var,time=0):
    """plot la valeur time du dataset donné"""
    
    if np.ndim(var) == 3:
        fig, ax = plt.subplots()
        surf = ax.pcolormesh(FLOW.x,FLOW.y,var[time,:,:])
        fig.colorbar(surf, shrink=0.5, aspect=5)
        
    elif np.ndim(var) == 4:
        fig, ax = plt.subplots()
        surf = ax.pcolormesh(FLOW.x,FLOW.y,var[time,0,:,:])
        fig.colorbar(surf, shrink=0.5, aspect=5)
        
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
        axs[row, col].set_title(f"Plot {i+1}")  # Titre pour chaque subplot
        
    # Cacher les sous-graphiques restants s'il y en a moins que la capacité maximale
    for i in range(num_plots, num_rows * num_cols):
        axs[i // num_cols, i % num_cols].axis('off')
    
    plt.tight_layout()
    plt.show()
#%% Exemple

# Flow_file = '/home/tfaraon/Documents/Cours/delft3D/Result/Hs_1_fp_0.1_eta_0_hL_10_hR_0.1_LR_100_WC_0_NR_1_CdR_0.09_CdL_0.01/trim-synthetic.nc'
# FLOW = D3D_Flow_Loader(Flow_file)
