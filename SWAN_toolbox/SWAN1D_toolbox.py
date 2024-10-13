#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 13:21:24 2023

@author: tfaraon
"""

import matplotlib.pyplot as plt
import numpy as np
import sys
import pandas as pd
from scipy import interpolate
from math import log,pi,sqrt,tanh,cosh,sinh
import matplotlib as mpl
import matplotlib.patches as patches
from matplotlib import cm
from mpl_axes_aligner import align  # to install this one, go into conda environment and use pip install 
from cycler import cycler
import os  


def read_swan_profil(myfile):
    
    profil=pd.read_csv(myfile , header=6, sep='\s+', names=['x','botlev','hsig','tm01','Diss','steepn','qb','urms'])
    profil['botlev'] = -profil['botlev']
        
    return profil


def read_spectrum_file(myfile):
    file = open(myfile, "r")
    mypdf=None
    flag_READ_NBR_FREQS = False
    flag_READ_FREQS = False
    for myline in file:
        if myline.find('AFREQ') >= 0 :
            flag_READ_NBR_FREQS = True
            continue
        if flag_READ_NBR_FREQS  :
            flag_READ_NBR_FREQS = False
            nbr_freqs=int(myline.split()[0])
            freqtbl=np.arange(nbr_freqs)
            mypd=pd.DataFrame(index=freqtbl,columns=['f','P'])
            for ifreq in freqtbl: 
                freqstr=file.readline()
                mypd.iloc[ifreq,0]=np.float64(freqstr)
            continue
        if myline.find('LOCATION     1') >= 0 :
            for ifreq in freqtbl: 
                energystr=file.readline()
                mypd.iloc[ifreq,1]=np.float64(energystr.split()[0])
            break
    mypd.replace(-99,np.nan,inplace=True)
    file.close()
    return mypd

def load_SWAN_outputs(dossier):
    # Chemin du dossier contenant les fichiers
    
    if os.path.isdir(dossier):
        fichiers = os.listdir(dossier)
        filelist = []  
        for nom_fichier in fichiers:
            chemin_fichier = os.path.join(dossier, nom_fichier)
            if os.path.isfile(chemin_fichier):
                filelist.append(chemin_fichier)
                    
    else: print('Le dossier n existe pas')
    
    data = {}#Le dictionnaire data contient mes données pour m'y retrouver
    
    for file in filelist:
        nom_fichier, extension = os.path.splitext(file)
        basename= os.path.basename(nom_fichier)
        
        if extension == '.profile':
            profil = read_swan_profil(file)
            data['profil'] = profil
            
        elif extension == '.spectrum':
            nom_variable = basename  
            
            spectre = read_spectrum_file(file) 
            data[nom_variable] = spectre
            
        else:
            print("Extension non gérée :", extension)
    
    return data    

def load_multi(dossiers): 
    
    data = []  
    for i in dossiers :        
        val = load_SWAN_outputs(i)
        data.append(val)
        
    return data

def plot_profil(profil,points):
    
    """Input : profil dataframe 
    points : dict{name:x_coord}"""
    
    fig, ax1 = plt.subplots(figsize=(11,5))
    
    ax1.plot(profil.get('x', []), profil.get('botlev', []), label='Profondeur', color='blue')
    ax1.set_ylabel('Profondeur', color='blue')  
    ax1.tick_params(axis='y', labelcolor='blue') 
    ax1.set_ylim(profil['botlev'].min(),-profil['botlev'].min())
    ax1.set_xlim(profil['x'].min(),profil['x'].max())
    ax1.grid(True)
    # ax1.invert_yaxis()
    
    ax2 = ax1.twinx()
    
    ax2.plot(profil.get('x', []), profil.get('hsig', []), label='Hs', color='red')
    ax2.set_ylabel('Hs', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.set_ylim(0,profil['hsig'].max()+1)
    
    
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    lines = lines_1 + lines_2
    labels = labels_1 + labels_2
    ax1.legend(lines, labels, loc='upper right')
    
    plt.title('Profil issu de SWAN')
    
    # Plot des points 
    for nom, x_coord in points.items():
        ax1.scatter(x_coord, 0, label=nom, s =20, marker ='^', color='r')
        ax1.text(x_coord, 0, nom, ha='right', va='bottom')
    
    plt.show()
    
def plot_spectrum(data):
    
    nb_elements = len(data) - 1  # Nombre total d'éléments dans le dictionnaire, moins l'élément 'profil'
    
    fig, axes = plt.subplots(nb_elements, 1, figsize=(8, 6 * nb_elements))
    
    # Parcours du dictionnaire et tracé des sous-graphiques pour chaque élément (sauf 'profil')
    index = 0
    for cle, spectre in data.items():
        if cle != 'profil':
            axes[index].semilogy(spectre.f,spectre.P,color='r',label = cle, lw = 3)
            axes[index].set_ylabel('SDE (Hz/m2)')
            axes[index].set_xlabel('Fréquence (Hz)')
            axes[index].tick_params(axis='both', which='major', labelsize=8, pad=1)
            axes[index].grid(which='major',color='grey',linestyle='--',linewidth=0.4)
            axes[index].grid(which='minor',color='grey',linestyle=':',linewidth=0.4)
            axes[index].set_ylim(bottom=1,top=1E7)

            axes[index].legend()
            index += 1

def plot_multi_profils(data,points):
    
    """Input : profil dataframe 
    points : dict{name:x_coord}"""
  

        
    for i in data : 
        profil = i.get('profil')
        
        fig, ax1 = plt.subplots(figsize=(11,5))
        
        ax1.plot(profil.get('x', []), profil.get('botlev', []), label='Profondeur', color='blue')
        ax1.set_ylabel('Profondeur', color='blue')  
        ax1.tick_params(axis='y', labelcolor='blue') 
        ax1.set_ylim(profil['botlev'].min(),-profil['botlev'].min())
        ax1.set_xlim(profil['x'].min(),profil['x'].max())
        ax1.grid(True)
        # ax1.invert_yaxis()
        ax2 = ax1.twinx()
        
        ax2.plot(profil.get('x', []), profil.get('hsig', []), label='Hs', color='red')
        
        ax2.set_ylabel('Hs', color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        ax2.set_ylim(0,profil['hsig'].max()+1)
        
        
        lines_1, labels_1 = ax1.get_legend_handles_labels()
        lines_2, labels_2 = ax2.get_legend_handles_labels()
        lines = lines_1 + lines_2
        labels = labels_1 + labels_2
        ax1.legend(lines, labels, loc='upper right')
        
        plt.title('Profil issu de SWAN')
    
    # Plot des points 
    for nom, x_coord in points.items():
        ax1.scatter(x_coord, 0, label=nom, s =20, marker ='^', color='r')
        ax1.text(x_coord, 0, nom, ha='right', va='bottom')
    
    plt.show()
    
    
def plot_multi_hs(data,labels, points):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for idx, dataset in enumerate(data):
        profil = dataset.get('profil')
        hs_values = profil.get('hsig')
        bot = profil.get('botlev')
        x_values = profil.get('x')
        
        ax.plot(x_values, hs_values, label=labels[idx])
        
        ax2 = ax.twinx()
        ax2.plot(x_values, bot, color='b')
    
        ax2.set_ylabel('Profondeur')
        ax2.set_ylim(-10,10)
        ax.set_ylim(0,hs_values.max()+1)
        
    ax.set_xlabel('Distance cross-shore')
    ax.set_ylabel('Hs')
    legend = ax.legend()
    legend.set_title("Densité de l'herbier \n (plants/m2)")
    ax.grid(True)
    plt.title('Comparaison des Hs selon les scénarios')
    rect = patches.Rectangle((250, -10), 350, 1, linewidth=1, edgecolor='green', facecolor='None', hatch='.')
    ax2.add_patch(rect)
    
    # Plot des points 
    for nom, x_coord in points.items():
        ax.scatter(x_coord, 0, label=nom, s =20, marker ='^', color='r')
        ax.text(x_coord, 0, nom, ha='right', va='bottom')
    
    plt.show()

def plot_multi_diss(data,labels,points):
    fig, ax = plt.subplots(figsize=(10, 6))
    val_max = []
    for idx, dataset in enumerate(data):
        profil = dataset.get('profil')
        diss_values = profil.get('Diss')
        bot = profil.get('botlev')
        x_values = profil.get('x')
        
        ax.plot(x_values, diss_values, label=labels[idx])
        
        ax2 = ax.twinx()
        ax2.plot(x_values, bot, color='b')
    
        ax2.set_ylabel('Profondeur')
        ax2.set_ylim(-10,10)
        ax.set_ylim(0,diss_values.max()+1)
        
        val_max.append(diss_values.max())
        
    ax.set_xlabel('Distance cross-shore')
    ax.set_ylabel('Dissipation W/m2')
    rect = patches.Rectangle((250, -10), 350, 1, linewidth=1, edgecolor='green',label='Herbier', facecolor='None', hatch='.')
    ax2.add_patch(rect)
    legend = ax.legend()
    legend.set_title("Densité de l'herbier \n (plants/m2)")
    ax.grid(True)
    plt.title('Comparaison de la dissipation selon les scénarios')

    
    # Plot des points 
    for nom, x_coord in points.items():
        ax.scatter(x_coord, 0, label=nom, s =20, marker ='^', color='r')
        ax.text(x_coord, 0, nom, ha='right', va='bottom')
    
    plt.show()
    
    return val_max

def swan_subplots(data, labels, variable1, variable2, points, save_title = None):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 9), dpi = 200)  
    
    for idx, dataset in enumerate(data):
        profil = dataset.get('profil')
        values_var1 = profil.get(variable1)
        values_var2 = profil.get(variable2)
        bot = profil.get('botlev')
        x_values = profil.get('x')
        
        ax1.plot(x_values, values_var1, label=labels[idx])  
        ax1.set_ylabel(variable1)
        
        ax2.plot(x_values, values_var2, label=labels[idx])  
        ax2.set_ylabel(variable2)
        
        ax2.yaxis.tick_right()
        ax2.yaxis.set_label_position("left")
        
        ax1.legend()
        ax2.legend()
        
        ax1.grid(True)
        ax2.grid(True)
        
        ax1.set_ylim(0, max(values_var1) + 1)
        ax2.set_ylim(0, max(values_var2) + 1)

    ax1_twin = ax1.twinx()
    ax1_twin.plot(x_values, bot, color='b')
    ax1_twin.set_ylabel('Profondeur')
    ax1_twin.set_ylim(-10, 10)
    ax2_twin = ax2.twinx()
    ax2_twin.plot(x_values, bot, color='b')
    ax2_twin.set_ylabel('Profondeur')
    ax2_twin.set_ylim(-10, 10)
    rect = patches.Rectangle((250, -10), 350, 1, linewidth=1, edgecolor='green',label='Herbier', facecolor='None', hatch='.')
    ax1_twin.add_patch(rect)
    rect1 = patches.Rectangle((250, -10), 350, 1, linewidth=1, edgecolor='green',label='Herbier', facecolor='None', hatch='.')
    ax2_twin.add_patch(rect1)

    for nom, x_coord in points.items():
        ax1.scatter(x_coord, 0, label=nom, s=20, marker='^', color='r')
        ax1.text(x_coord, 0, nom, ha='right', va='bottom')
        ax2.scatter(x_coord, 0, label=nom, s=20, marker='^', color='r')
        ax2.text(x_coord, 0, nom, ha='right', va='bottom')
    
    if save_title != None : 
        
        fig.savefig(f'dissipation_{save_title}.png')
    
    plt.tight_layout()
    plt.show()


def damping(data):
    """ 
    Permet de calculer la dissipation au point offshore et au dernier point. Doit être utilisée pour pplusieurs scénarios
    afin d'illuster la dissipation selon les différents scénarios de densité .
    
    """
    
    for cle, spectre in data.items():
        if cle.startswith('OFFSHORE'):
            mask = spectre['P'].notna()  # Utilisation de notna() pour filtrer les NaN
            clean_freq = spectre['f'][mask]  
            clean_sde = spectre['P'][mask] 
            hsig_off  = 4 * np.sqrt(np.trapz(clean_sde, clean_freq))
        
        elif cle.startswith('P4'):
            mask = spectre['P'].notna()  # Utilisation de notna() pour filtrer les NaN
            clean_freq = spectre['f'][mask]  
            clean_sde = spectre['P'][mask] 
            hsig_4 = 4 * np.sqrt(np.trapz(clean_sde, clean_freq))

    Kd = hsig_off/hsig_4 
        
    return Kd 
    
def multi_damping(data):
    kd = []
    for scenarios in data : 
        kd.append(damping(scenarios))
        
    return kd

def plot_damping(kd,densite): 
    """ permet de plotter les résultats de la fonction damping. 
    
    kd est issu de la fonction,
    densité est une liste des densité de points 
    """
    fig,ax = plt.subplots()
    ax.scatter(densite, kd)
    ax.set_xlabel("Densité de l'herbier (Pieds/m2)")
    ax.set_ylabel("Coefficient d'atténuation")
    ax.grid(True)    
    
def large_handler(large_data,hs,tp,densite):
    
    fig,ax = plt.subplots( figsize=(7,7), dpi = 200)
    for idx,dossiers in enumerate(large_data): 
        data = load_multi(dossiers)
        kd = multi_damping(data)
        
        ax.plot(densite, kd, label = f'Scénario {idx+1} : Hs = {hs[idx]}, Tp = {tp[idx]}')
        ax.legend(loc = 'upper left')
        ax.set_xlabel("Densité de l'herbier (Pieds/m2)")
        ax.set_ylabel("Coefficient d'atténuation")
        ax.grid(True)
    
