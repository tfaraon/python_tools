# Importation des modules nécessaires
import numpy as np
from scipy import interpolate, ndimage
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
from matplotlib import cm
import sys
import os
import pandas as pd
from matplotlib.widgets import PolygonSelector
from matplotlib.patches import Polygon
from matplotlib.path import Path

# Importation des outils spécifiques de xbTools
from xbTools.grid.creation import xgrid, ygrid
from xbTools.grid.extension import seaward_extend, lateral_extend
from xbTools.xbeachtools import XBeachModelSetup
from xbTools.general import wave_functions, visualize_mesh

def interpolate_nan(array):
    mask = np.isnan(array)
    array[mask] = np.interp(np.flatnonzero(mask), np.flatnonzero(~mask), array[~mask])
    return array

class AreaSelector:
    def __init__(self, image):
        self.image = image
        self.fig, self.ax = plt.subplots()
        self.ax.imshow(self.image)
        self.selected_areas = []
        self.selector = PolygonSelector(self.ax, self.onselect)
        self.fig.canvas.mpl_connect('key_press_event', self.toggle_selector)

    def onselect(self, verts):
        self.selected_areas.append(verts)
        poly = Polygon(verts, facecolor='None', edgecolor='red')
        self.ax.add_patch(poly)
        plt.draw()

    def toggle_selector(self, event):
        if event.key == 't':
            if self.selector.active:
                self.selector.set_active(False)
            else:
                self.selector.set_active(True)

    def show(self):
        plt.show()

    def get_selected_areas(self):
        return self.selected_areas

def generate_coordinates_inside_polygon(verts, image_shape):
    path = Path(verts)
    x, y = np.meshgrid(np.arange(image_shape[1]), np.arange(image_shape[0]))
    x, y = x.flatten(), y.flatten()
    points = np.vstack((x, y)).T
    mask = path.contains_points(points)
    return points[mask]

def smooth_region(bathy, mask, sigma=2):
    smoothed_bathy = ndimage.gaussian_filter(bathy, sigma=sigma)
    bathy[mask] = smoothed_bathy[mask]
    return bathy

#%% Initialisation avec la bathy 

# Chargement des données
filepath = '/home/tfrn/Documents/Stage_TDV/XBeach/Calibration/Calibration morpho/GIS/Bathy_2022.csv'
bathy = np.loadtxt(filepath)

# Configuration de la grille bathymétrique
nx = 1610
ny = 3680
dx = 1
dy = 1

# La bathy de cécile est inversée sur y 
# bathy = np.flip(bathy, axis=0)

x = np.linspace(0, (nx-1)*dx, nx)
y = np.linspace(0, (ny-1)*dy, ny)

X, Y = np.meshgrid(x, y)

# Affichage de la bathymétrie
plt.figure()
plt.imshow(bathy, vmax=4)
plt.colorbar()
plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.title('Bathymétrie')
plt.axis('scaled')
plt.tight_layout()

#%% création des grilles 
X, Y = np.meshgrid(x, y)
coords = np.column_stack((Y.ravel(), X.ravel())) 
values = bathy.ravel()

# Création de l'interpolateur
interp_func = interpolate.LinearNDInterpolator(coords, values)

# Création des nouvelles grilles xgr et ygr
xgr, zgr = xgrid(x, bathy[300,:], dxmin=5, dxmax=20)
ygr = ygrid(y, dymin=10, dymax=10)

Xgr, Ygr = np.meshgrid(xgr, ygr)
new_coords = np.column_stack((Ygr.ravel(), Xgr.ravel()))  # Mise en forme des nouvelles coordonnées

# Interpolation des données bathymétriques sur les nouvelles grilles
zgr = interp_func(new_coords).reshape(Xgr.shape)
zgr = interpolate_nan(zgr)

# Affichage des résultats
plt.figure(figsize=(10,6))
plt.plot(xgr[:-1], np.diff(xgr), '.-')
plt.xlabel('x [m]')
plt.ylabel('dx [m]')
plt.grid('on')
plt.title('Résolution cross-shore')
plt.tight_layout()
plt.savefig('/home/tfrn/Documents/Stage_TDV/XBeach/scenarios_restcoast/no_digue/data/grille_2d.png')    

plt.figure(figsize=(10,6))
plt.imshow(zgr)
plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.axis('scaled')
plt.title('xgr, ygr bathy')
plt.colorbar()
plt.show()

#%% Sélection de zone à lisser 

if __name__ == "__main__":
    image = zgr

    area_selector = AreaSelector(image)
    area_selector.show()
    selected_areas = area_selector.get_selected_areas()
#%% Création d'un masque pour les zones sélectionnées
    mask = np.zeros_like(image, dtype=bool)

    for verts in selected_areas:
        poly_coords = generate_coordinates_inside_polygon(verts, image.shape)
        mask[poly_coords[:, 1], poly_coords[:, 0]] = True

    # Lissage de la zone sélectionnée
    zgr_smoothed = smooth_region(zgr.copy(), mask, sigma=5)

    # Affichage de la bathymétrie lissée
    plt.figure()
    plt.subplot(1, 2, 1)
    plt.imshow(zgr, vmax=4)
    plt.colorbar()
    plt.title('Bathymétrie Originale')

    plt.subplot(1, 2, 2)
    plt.imshow(zgr_smoothed, vmax=4)
    plt.colorbar()
    plt.title('Bathymétrie Lissée')

    plt.show()

#%% nebed
zgr[:,0] = zgr[:,2]
zgr[:,-1] = zgr[:,-2]

zgr[0,:] = zgr[1,:]
zgr[-1,:] = zgr[-3,:]
zgr[-2,:] = zgr[-3,:]
zgr = interpolate_nan(zgr)

# Configuration et écriture du modèle XBeach
xb_setup = XBeachModelSetup('Test simulation')

xb_setup.set_grid(Xgr, Ygr, zgr_smoothed, posdwn=1, alfa=270)
xb_setup.set_nebed(zgr, struct=1)
xb_setup.set_friction(np.ones_like(zgr_smoothed))
xb_setup.set_waves('parametric', {'Hm0': [1],
                                  'Tp': [8],
                                  'gammajsp': [3.3],
                                  's': [20],
                                  'mainang': [270],
                                  'fnyq': [0.3]})

xb_setup.set_params({'Wavemodel': 'surfbeat',
                     'morphology': 0,
                     'befriccoef': 0.02,
                     'tstop': 10000,
                     'zs0': 0,
                     'nglobalvar': ['zb', 'zs', 'H'],
                     'npointvar': ['zs', 'H'],
                     'nmeanvar': ['zb'],
                     'npoints': ['1 0', '6 0', '10 0', '12 0']})

sim_path = '/home/tfrn/Documents/Stage_TDV/XBeach/scenarios_restcoast/no_digue/data'
if not os.path.exists(sim_path):
    os.mkdir(sim_path)
xb_setup.write_model(os.path.join(sim_path))
