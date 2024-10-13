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

XB_files = ['/home/tfrn/Documents/Stage_TDV/XBeach/Calibration/2D/2022/Dilatancy/Test_11_1/xboutput.nc',
            '/home/tfrn/Documents/Stage_TDV/XBeach/Calibration/2D/2022/Dilatancy/Test_11_2/xboutput.nc',
            '/home/tfrn/Documents/Stage_TDV/XBeach/Calibration/2D/2022/Dilatancy/Test_11_3/xboutput.nc',
            '/home/tfrn/Documents/Stage_TDV/XBeach/Calibration/2D/2022/Dilatancy/Test_11_4/xboutput.nc']

XB_data = []
for i in XB_files:
    XB = XBr.XB_Loader(i)
    XB_data.append(XB)


#%% 

transect = 125

initial_bed = XB_data[0].zb[0,transect,:].data

bottom_data = []
waterlevel_data = []
wave_data = []
for dataset in XB_data : 
    bottom_data.append(dataset.zb[-1,transect,:].data)
    waterlevel_data.append(dataset.zs[-1,transect,:].data)
    wave_data.append(dataset.H[-1,transect,:].data)
    
#%%

fig, ax = plt.subplots(figsize=(12,6))

label = ['a','b','c','d']
for i,n in enumerate(bottom_data) : 
    ax.plot(n, label = label[i])
ax.plot(initial_bed, '--g')

ax.legend()