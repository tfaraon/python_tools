#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 16:29:37 2024

@author: tfrn
"""

import numpy as np
import os 

os.chdir('/home/tfrn/Documents/Stage_TDV/Données hydro/REFMAR/Fos/2018/')
raw_data = np.loadtxt('previsions_shom_2702-0403_2018.csv',
                      delimiter=',')

slr = 0
scénario = 'noslr'

data = raw_data
data[:,1] = data[:,1]+slr

np.savetxt(f'tide_{scénario}.txt', data,
           delimiter=',')