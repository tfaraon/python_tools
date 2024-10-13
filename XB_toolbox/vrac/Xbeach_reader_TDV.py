#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 15:37:10 2024

@author: tfrn
"""

import Xbeach_reader as XBr
import Compare_data_tools as cpd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation
#%% Load the data

#Charmeent de la donnée XB brute 
XB_output = '/home/tfrn/Documents/Stage_TDV/XBeach/Calibration/1D/Tests et autres/Test_23e/xboutput.nc'
XB_data = XBr.XB_Loader(XB_output)

chemin_ADV = '/home/tfrn/Documents/Stage_TDV/Données hydro/Thomas_workspace/ADV_spectrum_analysis.csv'
chemin_S4 = '/home/tfrn/Documents/Stage_TDV/Données hydro/Thomas_workspace/S4_spectrum_analysis.csv'

start_date = '2005-11-24 00:00'
SAMAT_data_ADV= cpd.read_SAMAT_data(chemin_ADV)
SAMAT_data_S4 = cpd.read_SAMAT_data(chemin_S4)

#%% Test animation

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

ax1.set_xlim(0, len(XB_data.zs[0, 0, :]))
ax2.set_xlim(0, len(XB_data.zs[0, 0, :]))
ax1.set_ylim(np.min(XB_data.zb), 6)
ax2.set_ylim(np.min(XB_data.zb), 6)

time = ax2.annotate(0, xy=(1,0.5), xytext=(1, 0.5))
line1, = ax1.plot([], [], lw=1, color='blue') 
line2, = ax1.plot([], [], lw=1, color='red')
line3, = ax2.plot([], [], lw=1, color='green')
line4, = ax2.plot([], [], lw=1, color='orange') 

ax1.plot(XB_data.zb[0, 0, :],'g--')
ax2.plot(XB_data.zb[0, 0, :],'g--')

def init():
    line1.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])
    line4.set_data([], [])
    return line1, line2, line3, line4

def animate(i):
    line1.set_data(range(len(XB_data.zs[i*100, 0, :])), XB_data.zs[i*100, 0, :])
    line2.set_data(range(len(XB_data.zb[i*100, 0, :])), XB_data.zb[i*100, 0, :])
    line3.set_data(range(len(XB_data.H[i*100, 0, :])), XB_data.H[i*100, 0, :])
    line4.set_data(range(len(XB_data.zb[i*100, 0, :])), XB_data.zb[i*100, 0, :])
    
    time.set_text(f"Step {i}/{len(XB_data.zs)//100}")
    return line1, line2, line3, line4

anim = FuncAnimation(fig, animate, init_func=init, frames=len(
    XB_data.zs)//100, interval=100, blit=False)

plt.show()
# anim.save('/home/tfrn/Documents/Stage_TDV/XBeach/output/animation.gif', writer='imagemagick')
#%% Plot Hs au point tstop               = 129600


point_Hs_ADV = 10 #On suppose que le point qui se rapproche le plus de la position de l'adv est le 60

XB_Hs = cpd.extract_var_point(XB_data, 'H' ,point_Hs_ADV, start_date)
#PLot des données
fig, ax = plt.subplots(figsize=(15,7))
#Plot les résiltats de XB
ax.plot(XB_Hs.DateTime, XB_Hs.Hs)
ax.set_title(f"Hs au point x = {point_Hs_ADV}")
ax.set_ylabel("Hs")
ax.set_xlabel("Time")

#Plot les différents jeux de données de SAMAT
ax.plot(SAMAT_data_ADV.Date, SAMAT_data_ADV.Hs_uh, label='Hs_uh')
ax.plot(SAMAT_data_ADV.Date, SAMAT_data_ADV.Hs_p, label='Hs_p')
ax.plot(SAMAT_data_ADV.Date, SAMAT_data_ADV.Hs_inc_uhp, label='Hs_inc_uhp')
ax.plot(SAMAT_data_ADV.Date, SAMAT_data_ADV.Hs_r_uhp, label='Hs_r_uhp')

ax.legend()


#%% Compare Hs points S4 ADV

point_hs_S4 = 16
point_hs_ADV = 10 #On suppose que le point qui se rapproche le plus de la position de l'adv est le 60

XB_Hs_ADV= cpd.extract_var_point(XB_data,'H', point_hs_ADV, start_date)
XB_Hs_S4 = cpd.extract_var_point(XB_data,'H', point_hs_S4, start_date)

#PLot des données
fig,(ax1, ax2) = plt.subplots(2,1, figsize=(15,7))
#Plot les résiltats de XB
ax1.plot(XB_Hs_ADV.DateTime, XB_Hs_ADV.Hs.rolling(window=60).mean())
ax1.set_title(f"Hs au point x = {point_hs_ADV}")
ax1.set_ylabel("Hs")
ax1.set_xlabel("Time")

#Plot les différents jeux de données de SAMAT
ax1.plot(SAMAT_data_ADV.Date, SAMAT_data_ADV.Hs_uh, label='Hs_uh')
ax1.plot(SAMAT_data_ADV.Date, SAMAT_data_ADV.Hs_p, label='Hs_p')
ax1.plot(SAMAT_data_ADV.Date, SAMAT_data_ADV.Hs_inc_uhp, label='Hs_inc_uhp')
ax1.plot(SAMAT_data_ADV.Date, SAMAT_data_ADV.Hs_r_uhp, label='Hs_r_uhp')

#S4
ax2.plot(XB_Hs_S4.DateTime, XB_Hs_S4.Hs.rolling(window=60).mean())
ax2.set_title(f"Hs au point x = {point_hs_S4}")
ax2.set_ylabel("Hs")
ax2.set_xlabel("Time")

#Plot les différents jeux de données de SAMAT
ax2.plot(SAMAT_data_S4.Date, SAMAT_data_S4.Hs_uh, label='Hs_uh')
ax2.plot(SAMAT_data_S4.Date, SAMAT_data_S4.Hs_p, label='Hs_p')
ax2.plot(SAMAT_data_S4.Date, SAMAT_data_S4.Hs_inc, label='Hs_inc')
ax2.plot(SAMAT_data_S4.Date, SAMAT_data_S4.Hs_r, label='Hs_r')

ax2.legend()


