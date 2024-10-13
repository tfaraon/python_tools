#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 10:02:18 2023

@author: tfaraon

Partie du futur modèle qui calculera la diffusion

"""

import numpy as np 
from tqdm import tqdm
import sys
import pandas as pd
#%% test synth shoreline
def test_rechargement(x, largeur, longueur): 
    shoreline = np.zeros(x.shape)
    
    centre = (np.max(x) + np.min(x)) / 2  # Trouver le centre de x
    
    indice1 = np.where(np.logical_and(x < centre, x > centre - largeur/2))
    shoreline[indice1] = longueur * (1 + 2*(x[indice1]-centre)/largeur)
    
    indice2 = np.where(np.logical_and(x >= centre, x < centre + largeur/2))
    shoreline[indice2] = longueur * (1 - 2*(x[indice2]-centre)/largeur)

    return shoreline

#%% fonctions basiques avec r fixe

def diff_implicite_basique(shoreline, x, r, time, CL1, CL2):
    """
    Méthode implicite de calul de la diffusion. pas sur qu'elle fonctionne correctememnt

    """
    #création d'une matrice pour les différences finies
    matr_A = np.zeros((len(x),len(x)))  
    matr_A[0,0] = 1
    matr_A[-1,-1] = 1
    for i in tqdm(np.arange(1,x.size-1))  :
        matr_A[i,i-1] = -r
        matr_A[i,i] = 1 +2*r
        matr_A[i,i+1] = -r
    A_inv = np.linalg.pinv(matr_A) #Inversion de la matrice
    #Conditions aux limites au départ de la simulation
    shoreline[0] = CL1
    shoreline[-1] = CL2
    print('STEP 1 : DONE')
    for _ in tqdm(time): #itération temporelle sans indice
        shoreline_eroded = np.matmul(A_inv,shoreline)   #calcul du tdc diffusé
        erosion = (np.sum(np.abs(shoreline)) - np.sum(np.abs(shoreline_eroded)))/len(shoreline)     #calcul de la quantité érodée (carnet jaune, p.2)
        shoreline = shoreline_eroded + erosion          #ajout de la quantité érodée au tdc pour conserver la qtt de matière
        shoreline[0] += erosion
        shoreline[-1] += erosion
    return shoreline

def diff_explicite_basique(inp_shoreline, x, r, time, CL1, CL2):
    shoreline = inp_shoreline.copy()
    shoreline[0] = CL1
    shoreline[-1] = CL2

    # Créer une variable temporaire pour stocker l'itération précédente
    shoreline_prev = shoreline.copy()
    
    for _ in tqdm(time):
        shoreline[1:-1] = r * shoreline_prev[2:] + (1-2*r) * shoreline_prev[1:-1] + r*shoreline_prev[:-2] 
        erosion = (np.sum(np.abs(shoreline_prev)) - np.sum(np.abs(shoreline)))/len(shoreline)
        shoreline += erosion
        # Mettre à jour la variable temporaire avec la nouvelle valeur de shoreline
        shoreline_prev = shoreline.copy()
        shoreline[0] += erosion
        shoreline[-1] += erosion

    return shoreline

#%% r variable 

def diff_explicite_upgrade(inp_shoreline, x, r, time, CL1, CL2):
    shoreline = inp_shoreline.copy()
    shoreline[0] = CL1
    shoreline[-1] = CL2

    # Créer une variable temporaire pour stocker l'itération précédente
    shoreline_prev = shoreline.copy()
    
    for _ in tqdm(time):
        shoreline[1:-1] = r[:2] * shoreline_prev[2:] + (1-2*r[1:-1]) * shoreline_prev[1:-1] + r[:-2]*shoreline_prev[:-2] 
        erosion = (np.sum(np.abs(shoreline_prev)) - np.sum(np.abs(shoreline)))/len(shoreline)
        shoreline += erosion
        # Mettre à jour la variable temporaire avec la nouvelle valeur de shoreline
        shoreline_prev = shoreline.copy()
        shoreline[0] += erosion
        shoreline[-1] += erosion

    return shoreline


def diff_explicite_upgrade_V2(inp_shoreline, x, r, time, CL1, CL2):
    shoreline = inp_shoreline.copy()
    shoreline[0] = CL1
    shoreline[-1] = CL2

    shoreline_prev = shoreline.copy()
    
    for _ in tqdm(time):
        for i in range(1, len(x) - 1):
            shoreline[i] = r[i-1] * shoreline_prev[i+1] + (1-2*r[i]) * shoreline_prev[i] + r[i]*shoreline_prev[i-1]

        erosion = (np.sum(np.abs(shoreline_prev)) - np.sum(np.abs(shoreline))) / len(shoreline)
        shoreline += erosion
        shoreline_prev = shoreline.copy()
        shoreline[0] += erosion
        shoreline[-1] += erosion

    return shoreline


#%% launcher 
def run_simulation(shoreline_init, x, r, time, CL1, CL2) : 
    """Fait tourner la simulation et renvoie le résultat"""
    if type(r) == np.float64:
        if r < 0.5 : 
            print('La méthode explicite est stable, début de la simulation')
            shoreline_out = diff_explicite_basique(shoreline_init, x, r, time, CL1, CL2)
            return shoreline_out
        else : 
            print("La méthode explicite n'est pas stable, la méthode implicite va être utilisée. Elle peut être plus longue à calculer.")
            continue_sim = str(input('Continuer ? [y/n] : '))
            if continue_sim == 'y' : 
                try :
                    print("Je réflechis...")
                    shoreline_out = diff_implicite_basique(shoreline_init, x, r, time, CL1, CL2)
                    return shoreline_out
                except MemoryError:
                    print('La méthode explicite est instable et la taille de la simulation est trop grande pour la méthode explicite.\n Réduisez la taille longshore ou modifiez les variable pour réduire r')
                    sys.exit()
            else : 
                print('Arrêt de la simulation')
                sys.exit()


    if type(r) == pd.Dataframe : 
        print("Attention, projet en cours d'écriture")
        