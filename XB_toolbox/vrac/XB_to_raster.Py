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

# Load XB netcdf
XB_output = 'xboutput.nc'
XB_data = XBr.XB_Loader(XB_output)
X = np.loadtxt('x.grd')
Y = np.loadtxt('y.grd')
Z = XB_data.zs[-1,:,:].data

# Flatten the arrays
X_flat = np.ndarray.flatten(X)
Y_flat = np.ndarray.flatten(Y)
Z_flat = np.ndarray.flatten(Z)
X_flat = 0 - X_flat  # Flip X

# Combine X_flat, Y_flat, and Z_flat into a single array
data = np.column_stack((X_flat, Y_flat, Z_flat))

#%% Matrice de transf

# Rotate
angle_deg = 106.1  # Adjust this parameter to align the result with the original data
rotated_data = XBr.rotate_z(data, angle_deg)

# Translate 
# Specify the coordinates of the origin point (bottom left) of the extracted raster
coordonnees_origine = [827848, 6251842, 0]
translated_data = rotated_data + coordonnees_origine

#%% Save the result
output_filename = f'output_waterlevel_{dossier_test}.xyz'
np.savetxt(output_filename, translated_data, fmt='%0.6f', delimiter='\t')
