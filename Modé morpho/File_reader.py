#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 09:42:15 2023

@author: tfaraon
"""

import os
import pandas as pd
import numpy as np
import Diffusion_TDC as calc


os.chdir('synthetics')

#%%======================= Chargement du fichier maître =======================



#%%======================Chargement du fichier shoreline=======================
def load_computegrid(grid_filename = 'grid.txt'):
    if os.path.exists(grid_filename): 
        grid = np.loadtxt(grid_filename, delimiter=',')
        dx = grid[1] - grid[0]
    else: print(f'{grid_filename}: nom de fichier invalide ou fichier manquant. Réessayer.')    
    return grid, dx

def load_shoreline(shoreline_filename = 'shoreline.txt') :
    """
    Charge un fichier shoreline
    """
    if os.path.exists(shoreline_filename): 
        shoreline = np.loadtxt(shoreline_filename, delimiter=',')
    else: print(f'{shoreline_filename} : Nom de fichier invalide ou fichier manquant. Réessayer.')
    return shoreline

#%%======================Chargement du fichier de houle========================

def load_waveheight(waveheight_filename = 'offshore_hs.txt'): 
    if os.path.exists(waveheight_filename): 
        Hs = pd.read_csv(waveheight_filename, sep =',', index_col=0, header=None)

    else: print(f'{waveheight_filename}: nom de fichier invalide ou fichier manquant. Réessayer.')    
    
    return Hs

def load_wavelength(wavelength_filename = 'offshore_tp.txt'): 
    if os.path.exists(wavelength_filename): 
        Tp = pd.read_csv(wavelength_filename, sep =',', index_col=0, header=None)

    else: print(f'{wavelength_filename}: nom de fichier invalide ou fichier manquant. Réessayer.')    
    
    return Tp


