#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 13:54:17 2024

@author: tfrn
"""

import Xbeach_reader as XBr
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata
import rasterio
from rasterio.transform import from_origin
import os

dossier_test = 'Tideloc'

os.chdir(f'/home/tfrn/Documents/Stage_TDV/XBeach/Calibration/2D/2022/Test_19/{dossier_test}/')

#Load XB netcdf
XB_output = 'xboutput.nc'
XB_data = XBr.XB_Loader(XB_output)
X = np.loadtxt('x.grd')
Y = np.loadtxt('y.grd')
Z = XB_data.zs[-1,:,:].data

#%%Permet de mettre mes trois tableaux dans un fichier x,y,z 

X_flat = np.ndarray.flatten(X)
Y_flat = np.ndarray.flatten(Y)
Z_flat = np.ndarray.flatten(Z)
X_flat = 0 - X_flat  #ON remet x dans le bon sens par rapport à xb



#%% Matrice de transf

#D'abord on rotate

angle_deg = 106.1 #Jouer avec ce paramètre pour recaler le résultat par rapport à la donnée d'origine
rotated_data = XBr.rotate_z(data, angle_deg)

#Puis on translate 
#Ici indiquer la coordonnée du point d'origine (bas à gauche) du raster extrait
coordonnees_origine = [827848,
                       6251842
                       ,0]

translated_data = rotated_data + coordonnees_origine

#%%Enfin on sauvegarde
output_filename = f'output_waterlevel_{dossier_test}.xyz'
np.savetxt(output_filename, translated_data, fmt='%0.6f', delimiter='\t')