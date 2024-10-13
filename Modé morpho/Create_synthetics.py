#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 14:41:18 2023

@author: tfaraon
"""
#------------------------------------------------------------------------------
#
#Création de synthétiques de conditions au large pour créer le lecteur de fichiers du futur modèle
#
# -synthé Shoreline
# - Synthé Hs 
# - synthé Tp
#
#------------------------------------------------------------------------------
import numpy as np
import os

if not os.path.exists('synthetics'):
    # S'il n'existe pas, le créer
    os.makedirs('synthetics')
    print("Le dossier synthetics a été créé.")
else:
    os.chdir('synthetics')

#%% Grid creation
length_of_xgrid = 1e5
dx = 1000
x = np.arange(0,  length_of_xgrid, step = dx)
np.savetxt('grid.txt', x, delimiter=',')

#%% Shoreline creation 
simple_oscillating_shoreline = np.cos(1e-4*x) #Un trait de côte basique oscillant
np.savetxt('shoreline.txt', simple_oscillating_shoreline, delimiter= ',')


#%% Hs creation
offshore_wave_height_t0 = np.cos(0.01*x)+1 
# offshore_wave_height_t100 = np.cos(0.01*x)+2
# offshore_wave_height_t450 = np.cos(0.008*x)+1

outtable_index = ["0"]
# outtable_index = ["0","100","450"]
data = np.array([offshore_wave_height_t0])
# data = np.array([offshore_wave_height_t0, offshore_wave_height_t100, offshore_wave_height_t450])

with open('offshore_hs.txt', 'w') as file:
    for i, row in enumerate(data):
        row_values = [outtable_index[i]] + [str(val) for val in row]
        file.write(','.join(row_values) + '\n')

#%% Tp creation

offshore_wave_length_t0 = np.cos(0.01*x)+6 
# offshore_wave_length_t100 = np.cos(0.01*x)+8
# offshore_wave_length_t450 = np.cos(0.008*x)+6

outtable_index = ["0"]
# outtable_index = ["0","100","450"]
data = np.array([offshore_wave_length_t0])
# data = np.array([offshore_wave_length_t0, offshore_wave_length_t100, offshore_wave_length_t450])
with open('offshore_tp.txt', 'w') as file:
    for i, row in enumerate(data):
        row_values = [outtable_index[i]] + [str(val) for val in row]
        file.write(','.join(row_values) + '\n')

