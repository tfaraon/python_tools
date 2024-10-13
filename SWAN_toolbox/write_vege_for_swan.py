#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 15:17:54 2023

@author: tfaraon
"""

import numpy as np
import os

# On ouvre la bathy pour avoir le même nombre de points de grid

file = '/home/tfaraon/Bureau/exemple_bathy_1D.dat'
data_str = np.loadtxt(file, dtype=str, delimiter=' ')
bathy_size = len(data_str)

# densité de mes herbiers avec une densité cnstante sur le profil

d =   #plants par m2

x_start = 250 
x_end = 600 
x = np.zeros(bathy_size)
x[x_start:x_end] = d

#les valeurs de densité de l'herbier sont de d entre les deux indices. 
#maintenant on sauvegarde

np.savetxt(f"herbier_d{d}_SWAN1D.dat", x, delimiter=" ")
