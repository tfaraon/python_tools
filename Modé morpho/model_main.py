#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 10:29:33 2023

@author: tfaraon
"""

import numpy as np
import Diffusion_TDC as calc
import File_reader as reader
import model_ploter as ploter

#variables pour le modèle
# ==============================fixes==========================================
# stockage des variables par défaut au cas où 
#
# dx = 1000
# x = np.arange(0,1e5,dx)
#shoreline_init = np.sin(x * 1e-4)
# =============================================================================#

#Comme il est lourd d'utiliser des secondes directement, on indique un nombre d'années qu'on converti discretement en seconde
YEAR_TO_SECONDS = 365.25*24*3600

#Valeurs constantes par défaut
dt = 0.1
Hs = 0.5
Tp = 4 
rho_eau = 1024
rho_sed = 2700
porosite = 0.3
g = 9.81
K = 0.77
profondeur_fermeture = 10
hauteur_berme = 1

#Calculs des grandeurs 
Cl = (K * rho_eau * g * Hs**2 * Tp)/(64*np.pi*(rho_sed-rho_eau)*(1-porosite))
G0 = Cl / (profondeur_fermeture + hauteur_berme)                                                              

#Chargement des variables des fichiers
shoreline_init = reader.load_shoreline()
x, dx = reader.load_computegrid()

#Autres variables
r = (G0 * dt * YEAR_TO_SECONDS)/(dx**2)
time = np.arange(0, 10000, dt)
CL1 = 0
CL2 = 0

#%% Calcul 
sim_out = calc.run_simulation(shoreline_init, x, r, time, CL1, CL2)
ploter.double_plot_shore(x, shoreline_init, sim_out)

# out_1 = diff_explicite(shoreline_init, x, r, time, CL1, CL2)
# out_2 = diff_implicite(shoreline_init, x, r, time, CL1, CL2)
# double_plot_shore(x, out_1, out_2)
