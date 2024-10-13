#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 10:37:05 2023

@author: tfaraon
"""
import matplotlib.pyplot as plt


def simple_plot_shore(x, var):
    
    fig,ax= plt.subplots(figsize =(12,5))
    ax.plot(x,var)
    ax.grid(True)
    ax.set_ylabel('Crossshore (m)')
    ax.set_xlabel('Lonbgshore (m)')

def double_plot_shore(x,S,S_fin):
    
    fig,ax= plt.subplots(figsize =(8,5))
    ax.plot(x,S_fin, label = 'S_fin')
    ax.plot(x,S, label='S_init')
    ax.grid(True)
    ax.set_ylabel('Crossshore (m)')
    ax.set_xlabel('Longshore (m)')
    ax.legend()
