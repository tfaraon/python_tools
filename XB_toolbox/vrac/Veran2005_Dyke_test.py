
# import default modules
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
from matplotlib import cm
import sys
import os

## import specific tools from xbTools
from xbTools.grid.creation import xgrid, ygrid
from xbTools.grid.extension import seaward_extend, lateral_extend
from xbTools.xbeachtools import XBeachModelSetup
from xbTools.general import wave_functions, visualize_mesh

def interpolate_nan(array):
    mask = np.isnan(array)
    array[mask] = np.interp(np.flatnonzero(mask), np.flatnonzero(~mask), array[~mask])
    return array



#%% Initialisation avec la bathy 

## load data
bathy = np.loadtxt('/media/tfrn/easystore/copie_7avril2023/XBEACH/2006/gille_bathy_dep/XBEACH_bathy_2006_linearMethod.dep')

## set bathy grid
nx = 400
ny = 730
dx = 5
dy = 5

#La bathy de cécile est inversée sur y 
bathy = np.flip(bathy, axis=0)
bathy = bathy[:,400:]

x = np.linspace(0,(nx-1)*dx,nx)
y = np.linspace(0,(ny-1)*dy,ny)

X, Y = np.meshgrid(x,y)

## plot
plt.figure()
plt.imshow(bathy)
plt.colorbar()
plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.title('flat bathy')
plt.axis('scaled')

#%% Séléctionde la zone

zone_mask = np.ones_like(bathy, dtype=np.float64) * 10
ne_zone = np.where(bathy[:,253:290] > 0.3)
ne_zone = (ne_zone[0], ne_zone[1] + 253)
zone_mask[ne_zone] = 0
plt.figure()
plt.imshow(zone_mask, cmap='binary')
plt.title('NE zone')
plt.show()

