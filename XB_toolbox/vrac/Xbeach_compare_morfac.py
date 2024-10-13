#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 09:51:32 2024

@author: tfrn
"""

import Xbeach_reader as XBr
import Compare_data_tools as cpd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

XB_files = ['/home/tfrn/Documents/Stage_TDV/XBeach/Calibration/2D/2022/Test_9/xboutput.nc',
            '/home/tfrn/Documents/Stage_TDV/XBeach/Calibration/2D/2022/Test_9b/xboutput.nc',
            '/home/tfrn/Documents/Stage_TDV/XBeach/Calibration/2D/2022/Test_9c/xboutput.nc']

XB_data = []
for i in XB_files:
    XB = XBr.XB_Loader(i)
    XB_data.append(XB)

# %%

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

ax1.imshow(XB_data[0].zb[-1, :, :].data -
           XB_data[0].zb[0, :, :].data, cmap='viridis')
ax1.set_title('Résultat Morfac = 1')

ax2.imshow(XB_data[1].zb[-1, :, :].data -
           XB_data[1].zb[0, :, :].data, cmap='viridis')
ax2.set_title('Résultat Morfac = 2')

ax3.imshow(XB_data[2].zb[-1, :, :].data -
           XB_data[2].zb[0, :, :].data, cmap='viridis')
ax3.set_title('Résultat Morfac = 10')

# %% Différence
diff_2 = np.abs(XB_data[1].zb[-1, :, :].data - \
    XB_data[0].zb[-1, :, :].data)  # Différence entre morfac 1 et 2
diff_10 = np.abs(XB_data[2].zb[-1, :, :].data - XB_data[0].zb[-1,
                                                       :, :].data) # DIfférence entre morfac 1 et 10
diff_2_10 = np.abs(XB_data[2].zb[-1, :, :].data - XB_data[1].zb[-1,
                                                         :, :].data)  # DIfférence entre morfac 2 et 10

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

ax1.imshow(diff_2, cmap='bwr')
ax1.set_title('Différence Morfac = 2')

ax2.imshow(diff_10, cmap='bwr')
ax2.set_title('Différence Morfac = 10')

ax3.imshow(diff_2_10, cmap='bwr')
ax3.set_title('Différence Morfac = 2/10')

# %%profils


# Emplacements des différents transects
transects = [60, 75, 100, 125]

fig, axes = plt.subplots(4, 1, figsize=(8, 15))

for i, transect in enumerate(transects):
    profil_1 = XB_data[0].zb[100, transect, :].data
    profil_2 = XB_data[1].zb[100, transect, :].data
    profil_10 = XB_data[2].zb[100, transect, :].data

    ax = axes[i]

    ax.plot(profil_1, label='morfac = 1')
    ax.plot(profil_2, label='morfac = 2')
    ax.plot(profil_10, label='morfac = 10')
    ax.set_title(f'Transect {transect}')

    ax.set_ylabel('z (m)')
    ax.legend()

plt.suptitle('Comparaison des résultats')
plt.tight_layout()

# COmme la simulation du morfac 1 était trop longue, elle s'est arrétée. Comme je n'ai pas la fin je ne plot que morfac 2 et 10

fig, axes = plt.subplots(4, 1, figsize=(8, 15))

for i, transect in enumerate(transects):
    end_profil_2 = XB_data[1].zb[-1, transect, :].data
    end_profil_10 = XB_data[2].zb[-1, transect, :].data

    ax = axes[i]

    ax.plot(end_profil_2, label='morfac = 2')
    ax.plot(end_profil_10, label='morfac = 10')
    ax.set_title(f'Transect {transect}')

    ax.set_ylabel('z (m)')
    ax.legend()

plt.suptitle('Comparaison des résultats')
plt.tight_layout()


# %% erreur morfac
# ne tourne pas en cellule seule !!!

for i, transect in enumerate(transects):
    end_profil_2 = XB_data[1].zb[-1, transect, :].data
    end_profil_10 = XB_data[2].zb[-1, transect, :].data

    print(
        f'Pour le transect {transect}, std = {np.std(end_profil_10 - end_profil_2)}')


print(f'Pour la totalité, std = {np.std(diff_2_10)}')
