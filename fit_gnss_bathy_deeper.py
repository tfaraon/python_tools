#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 15:14:43 2024

@author: tfrn
"""

import pandas as pd

#-----------------------------------------------------------------------------------------------
#
#Script pour faire coller les données de bathy acquises avec le sondeur deeper chirp 2 et le gnss
#
# Pour fonctionner il faut : 
#   - Un fichier bathy au format csv après traitement dans le script deeper_chirp_bathy.py
#   - le fichier topo final après traitement, au format csv avec heure, E, N 
#
#-----------------------------------------------------------------------------------------------

#Fichier de données bathy : 
    
bathy_file = '/home/tfrn/Documents/Stage_TDV/Terrain/20240524_Beauduc/Bathy/20240524_Beauduc_Bathy_filt.txt'

#Fichier GNSS 

gnss_file = '/home/tfrn/Documents/Stage_TDV/Terrain/20240524_Beauduc/Kayak/20240524_Beauduc_kayak_corr.txt'

#Destination 

destination = '/home/tfrn/Documents/Stage_TDV/Terrain/20240524_Beauduc/Bathy/20240524_georef_bathy.csv'
#%% Chargement des données

bathy_raw = pd.read_csv(bathy_file, sep=",", decimal='.', index_col=0, header=0)
bathy_raw.DateTime = pd.to_datetime(bathy_raw.DateTime)
bathy_raw['Time']= bathy_raw.DateTime.dt.strftime('%H:%M:%S') #On ne garde que l'heure pour faire fiter
bathy_data = bathy_raw.drop(columns=['latitude', 'longtitude', 'temperature', 'DateTime'])
del bathy_raw
#Les données propres sont stockées dans un nouveau df et l'ancien est supprimé

gnss_raw = pd.read_csv(gnss_file, sep="\t", decimal='.', header=0, names = ['Time', 'E', 'N','H'])
gnss_raw.Time = pd.to_datetime(gnss_raw.Time, origin='unix')
gnss_raw['Time']= gnss_raw.Time.dt.strftime('%H:%M:%S')

merged_data = pd.merge(bathy_data, gnss_raw, on='Time', how='inner')
final_data = merged_data[['Time','E','N','depth']]

final_data.to_csv(destination, decimal='.', sep =',',index= False)