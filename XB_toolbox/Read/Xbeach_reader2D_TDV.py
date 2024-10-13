#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 09:20:56 2024

@author: tfrn
"""

import Xbeach_reader as XBr
# import Compare_data_tools as cpd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation
#%% Load the data

#Chargement de la donnée XB brute 

XB_output = '/home/tfrn/Documents/Stage_TDV/XBeach/Calibration/2D/2022/Test_19/Tideloc/xboutput.nc'
XB_data = XBr.XB_Loader(XB_output)

X = XB_data.get_variable('globalx').data
Y = XB_data.get_variable('globaly').data
#%%
Hs = XB_data.H[3,50,:].data
zb = XB_data.zb[-1,:,:].data

fig, ax = plt.subplots()
ax.imshow(zb)

fig, ax = plt.subplots()
ax.pcolormesh(X, Y, zb)

ax.set_title("test bathy")

fig, ax = plt.subplots()
ax.plot(XB_data.H[-1,100,:].data)
ax.set_ylim(0,1)

ax.set_title("test")
ax.set_ylabel("Hs")
ax.set_xlabel("x")

diff = XB_data.zb[-1,:,:].data - XB_data.zb[0,:,:].data
fig, ax = plt.subplots()
ax.pcolormesh(X, Y, diff, cmap='BrBG')
ax.invert_xaxis()
ax.set_title("test bathy diff")

fig, ax = plt.subplots()
ax.pcolormesh(X, Y, XB_data.H[-1,:,:].data, vmin=0)
ax.set_title("test HS")

fig, ax = plt.subplots()
ax.pcolormesh(X, Y, XB_data.zs[-1,:,:].data)
ax.invert_xaxis()


#%% Animation 
transect = 100

t = XB_data.H.data

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

ax1.set_xlim(0, len(XB_data.zs[0, transect, :]))
ax2.set_xlim(0, len(XB_data.zs[0, transect, :]))
ax1.set_ylim(np.min(XB_data.zb), 6)
ax2.set_ylim(np.min(XB_data.zb), 6)

time = ax2.annotate(0, xy=(1,0.5), xytext=(1, 0.5))
line1, = ax1.plot([], [], lw=1, color='blue') 
line2, = ax1.plot([], [], lw=1, color='red')
line3, = ax2.plot([], [], lw=1, color='green')
line4, = ax2.plot([], [], lw=1, color='orange') 

ax1.plot(XB_data.zb[0, transect, :],'g--')
ax2.plot(XB_data.zb[0, transect, :],'g--')

def init():
    line1.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])
    line4.set_data([], [])
    return line1, line2, line3, line4

def animate(i):
    line1.set_data(range(len(XB_data.zs[i*1, transect, :])), XB_data.zs[i*1, transect, :])
    line2.set_data(range(len(XB_data.zb[i*1, transect, :])), XB_data.zb[i*1, transect, :])
    line3.set_data(range(len(XB_data.H[i*1, transect, :])), XB_data.H[i*1, transect, :])
    line4.set_data(range(len(XB_data.zb[i*1, transect, :])), XB_data.zb[i*1, transect, :])
    
    time.set_text(f"Step {i}/{len(XB_data.zs)//1}")
    return line1, line2, line3, line4

anim = FuncAnimation(fig, animate, init_func=init, frames=len(
    XB_data.zs)//1, interval=200, blit=False)
ax.invert_yaxis()
plt.show()

#%% 2D Hs 

fig, ax = plt.subplots()

# ax.set_xlim(0, XB_data.H.shape[2])
# ax.set_ylim(0, XB_data.H.shape[1])
im = ax.pcolormesh(X, Y, XB_data.H[0, :, :], cmap='viridis', animated=True, vmin=XB_data.H[:, :, :].min(), vmax=XB_data.H[:, :, :].max())
def init():
    im.set_array(XB_data.H[0, :, :])
    return [im]

def animate(i):
    im.set_array(XB_data.H[i, :, :])
    return [im]

anim = FuncAnimation(fig, animate, init_func=init, frames=XB_data.H.shape[0], interval=300, blit=True)
ax.invert_xaxis()
plt.show()

#%% 2D Zs
fig, ax = plt.subplots()
# ax.set_xlim(0, XB_data.zs.shape[2])
# ax.set_ylim(0, XB_data.zs.shape[1])
time = ax.annotate(0, xy=(-3200,10), xytext=(-3200, 10))
im = ax.pcolormesh(X, Y, XB_data.zs[0, :, :], cmap='viridis', animated=True, vmin=XB_data.zs[:, :, :].min(), vmax=XB_data.zs[:, :, :].max())

def init():
    im.set_array(XB_data.zs[0, :, :])
    return [im]

def animate(i):
    im.set_array(XB_data.zs[i, :, :])
    
    time.set_text(f"Step {i}/{len(XB_data.zs)//1}")
    return [im]

anim = FuncAnimation(fig, animate, init_func=init, frames=XB_data.zs.shape[0], interval=150, blit=True)
ax.invert_xaxis()
plt.show()

