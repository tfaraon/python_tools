#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 11:40:18 2024

@author: tfrn
"""

import pandas as pd
import numpy as np
import mat73 


def ADCP_loader(filepath):
    
    raw_data = pd.read_csv(filepath,
                delimiter=';',
                decimal='.',
                header=0,
                usecols=np.arange(0,204,1)
                )
    
    return raw_data

def depth_integration(ax1,ax2,ax3,ax4):
    
    ax1_mean = ax1.mean(axis=1)
    ax2_mean = ax2.mean(axis=1)
    ax3_mean = ax3.mean(axis=1)
    ax4_mean = ax4.mean(axis=1)

    return ax1_mean,ax2_mean,ax3_mean,ax4_mean

def extract_axis(raw_data): 
    dates = raw_data['DateTime']
    df_E = raw_data.filter(regex='^Eas')
    df_N = raw_data.filter(regex='^Nor')
    df_U1 = raw_data.filter(regex='^Up1')
    df_U2 = raw_data.filter(regex='^Up2')
    
    df_E,df_N,df_U1,df_U2 = depth_integration(df_E,df_N,df_U1,df_U2)
    
    df_E = pd.concat([dates, df_E], axis=1)
    df_N = pd.concat([dates, df_N], axis=1)
    df_U1 = pd.concat([dates, df_E], axis=1)
    df_U2 = pd.concat([dates, df_N], axis=1)


    return df_E, df_N, df_U1, df_U2

def ADCP_current_from_matlab(filepath, appareil='Poudlard'):
    
    data = mat73.loadmat(filepath)
    adcp_data = data[appareil]

    del data

    Ue = adcp_data['Ue']
    Ue_mean = Ue.mean(axis=1)
    
    Un = adcp_data['Un']
    Un_mean = Un.mean(axis=1)

    return np.column_stack((Ue_mean , Un_mean))

    