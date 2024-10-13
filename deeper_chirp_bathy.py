#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 09:21:47 2024

@author: tfrn
"""
#%% Fonctions

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata
import matplotlib.colors as mcolors
import os


def read_bathy_csv(csv_bathy_path):
    return pd.read_csv(csv_bathy_path, delimiter=',', decimal='.', header=0)


def correct_time(filtered_bathy_data):
    filtered_bathy_data['DateTime'] = pd.to_datetime(
        filtered_bathy_data['time'], unit='ms')
    filtered_bathy_data.drop(columns=['time'], inplace=True)
    filtered_bathy_data.DateTime = filtered_bathy_data.DateTime.dt.strftime('%Y-%m-%d %H:%M:%S')
    return filtered_bathy_data


def clean_chirp_bathy(csv_bathy_path, convert_time=True,correct_tide = False,tidefile= None,deeper_start_time=None,deeper_end=None,controle_1=None, controle_2=None , plot=True):
    raw_bathy_data = read_bathy_csv(csv_bathy_path)
    filtered_bathy_data = raw_bathy_data.dropna(
        subset=["latitude", "longtitude", "depth"])
    

    if convert_time == True:

        filtered_bathy_data = correct_time(filtered_bathy_data)

    if correct_tide == True: 
        
        filtered_bathy_data = correct_tide_func(filtered_bathy_data, tidefile, deeper_start_time,deeper_end, controle_1, controle_2)
        
    if plot:
        X = filtered_bathy_data['longtitude'].values
        Y = filtered_bathy_data['latitude'].values
        Z = filtered_bathy_data['depth'].values
        xi = np.linspace(X.min(), X.max(), 100)
        yi = np.linspace(Y.min(), Y.max(), 100)
        zi = griddata((X, Y), Z, (xi[None, :], yi[:, None]), method='linear')
        plt.contour(xi, yi, zi, levels=8, colors='k')
        plt.contourf(xi, yi, zi, levels=8, cmap='jet')
        plt.colorbar()
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Depth Contours with Color Map')
        plt.show()
    
    filtered_bathy_data['depth'] = -filtered_bathy_data['depth']
    return filtered_bathy_data

def correct_tide_func(filtered_bathy_data, tidefile, deeper_start_time, deeper_end, controle_1, controle_2):
    tide = pd.read_csv(tidefile, header=None, names=['Date', 'Valeur', 'Source'], skiprows=14, sep=';', decimal='.', parse_dates=True)
    tide['Date'] = pd.to_datetime(tide['Date'], dayfirst=True)  # Ajoutez dayfirst=True ici
    tide.set_index('Date', inplace=True)
    tide = tide.resample('S').interpolate()

    filtered_bathy_data.set_index('DateTime', inplace=True)
    filtered_bathy_data.index = pd.to_datetime(filtered_bathy_data.index)
    filtered_bathy_data = filtered_bathy_data[~filtered_bathy_data.index.duplicated()]
    filtered_bathy_data = filtered_bathy_data.resample('S').interpolate()

    htopo = (controle_1 + controle_2) / 2
    tide_corr = tide.copy()
    tide_corr = tide_corr.loc[deeper_start_time:deeper_end]
    tide_corr['Valeur'] = tide_corr['Valeur'] - htopo

    corr_bathy_data = filtered_bathy_data.copy()
    corr_bathy_data['depth'] = filtered_bathy_data['depth'] - tide_corr['Valeur']

    return corr_bathy_data

    

#%%

print('Filtrage des données sur les coordonnées mesurées par le téléphone')
csv_bathy_path = '/home/tfrn/Documents/Stage_TDV/Terrain/20240524_Beauduc/Raw/Bathy/20240524_Beauduc_bathy.csv'
tidefile = '/home/tfrn/Documents/Stage_TDV/Données hydro/REFMAR/Port_de_bouc/05/720_2024.txt'

path_to_save = '/home/tfrn/Documents/Stage_TDV/Terrain/20240524_Beauduc/Bathy/20240524_Beauduc_Bathy_filt.txt'

data = clean_chirp_bathy(csv_bathy_path, correct_tide=False, tidefile=tidefile, deeper_start_time='2024-05-24 10:40:00', deeper_end='2024-03-19 13:40:00', controle_1=0.209, controle_2=0.174)

try:
    os.makedirs(os.path.dirname(path_to_save), exist_ok=True)
    data.to_csv(path_to_save, sep=',', decimal='.')
    print('\nData saved successfully.')
except FileNotFoundError as e:
    print(
        f'\nError: {e}. Please check if the directory exists and you have the necessary permissions.')
