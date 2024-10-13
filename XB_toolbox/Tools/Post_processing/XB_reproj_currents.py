#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 13:42:21 2024

@author: tfrn
"""

import Xbeach_reader as XBr
import matplotlib.pyplot as plt

XB_output = '/home/tfrn/Documents/Stage_TDV/XBeach/Calibration/2D/2022/Test_19/Tideloc/xboutput.nc'
XB_data = XBr.XB_Loader(XB_output)

U = XB_data.get_variable('u')
V = XB_data.get_variable('v')

XB_data.close()

U_point = U[:,105,165]
V_point = V[:,105,165]

plt.plot(U_point)