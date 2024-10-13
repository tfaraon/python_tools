#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 11:39:21 2024

@author: tfrn
"""

import os 
import numpy as np
import ADCP_tools as adcp 
import matplotlib.pyplot as plt 

filepath = '/media/tfrn/disk1/Pandora/pandoraB0_1.csv'

raw_data = adcp.ADCP_loader(filepath)

E,N,U1,U2 = adcp.extract_axis(raw_data)

plt.plot(E.iloc[:,1],N.iloc[:,1],'.')
plt.show()
