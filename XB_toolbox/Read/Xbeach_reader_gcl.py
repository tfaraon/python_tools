#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 17:42:25 2024

@author: tfaraon
"""

import Xbeach_reader as XBr
#%% Pour une seule 

XB_output = '/home/tfrn/Documents/Stage_TDV/XBeach/Calibration/Test_1.5/xboutput.nc'
XB_data = XBr.XB_Loader(XB_output)
XBr.plot_simple_profil(XB_data, 'Hrms', XB_output, moyenne=False, time=1000)

#%% Pour les subplots

#    Attention : 
#    Peut être long

H = 1
chemin ='/home/tfaraon/Documents/Cours/projet/XBeach/test7/'

dossier = [f'{chemin}H{H}P0/xboutput.nc',
            f'{chemin}H{H}P150/xboutput.nc',
            f'{chemin}H{H}P300/xboutput.nc',
            f'{chemin}H{H}P500/xboutput.nc',
            f'{chemin}H{H}P1000/xboutput.nc']


output_list = XBr.xb_multi_loader(dossier)

D = XBr.xb_subplots_map(output_list, [0,150,300,500,1000], 'zmin', 'zmax', f'H{H}')

#%% 
chemin ='/home/tfaraon/Documents/Cours/projet/XBeach/test7/'

dossier1 = [f'{chemin}H1P0/xboutput.nc',
            f'{chemin}H1P150/xboutput.nc',
            f'{chemin}H1P300/xboutput.nc',
            f'{chemin}H1P500/xboutput.nc',
            f'{chemin}H1P1000/xboutput.nc']

dossier2 = [f'{chemin}H2P0/xboutput.nc',
            f'{chemin}H2P150/xboutput.nc',
            f'{chemin}H2P300/xboutput.nc',
            f'{chemin}H2P500/xboutput.nc',
            f'{chemin}H2P1000/xboutput.nc']

dossier3 = [f'{chemin}H3P0/xboutput.nc',
            f'{chemin}H3P150/xboutput.nc',
            f'{chemin}H3P300/xboutput.nc',
            f'{chemin}H3P500/xboutput.nc',
            f'{chemin}H3P1000/xboutput.nc']

superdossier = [dossier1, dossier2, dossier3]

hs = [1,2,3]
tp = [8,10,12]
densite = [0,150,300,500,1000]

XBr.xb_damping(superdossier, hs, tp, densite)

        
    