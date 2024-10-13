#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 09:22:23 2024

@author: tfrn
"""

import ADCP_tools as adcp
import Xbeach_reader as XBr
import numpy as np
import matplotlib.pyplot as plt 

Ue_mean, Un_mean = adcp.ADCP_current_from_matlab('/media/tfrn/disk2/save_hydro/save_struc/ADCP.mat')

data = np.column_stack((Ue_mean,Un_mean))

plt.figure(figsize=(10, 8))
plt.hist2d(Ue_mean, Un_mean, bins=1000, cmap='Blues')
plt.colorbar(label='Densité')
plt.title("Densité des points")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()
