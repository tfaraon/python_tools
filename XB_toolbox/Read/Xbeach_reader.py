import os
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import re
import matplotlib.patches as patches
from datetime import datetime, timedelta
import pandas as pd


#%% usefull functions 
class XB_Loader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.dataset = Dataset(file_path, 'r')

        # Meshgrids : variables de structure
        self.time = self.get_variable("globaltime")
        self.x = self.get_variable("globalx")
        self.y = self.get_variable("globaly")
        self.zb = self.get_variable("zb")
        self.zs = self.get_variable("zs")
        self.H = self.get_variable("H")

    def get_variable(self, var_name):
        """ Retrieve a variable if it exists, otherwise return None """
        if var_name in self.dataset.variables:
            return self.dataset.variables[var_name][:]
        else:
            print(f"Variable '{var_name}' not found in the dataset.")
            return None

    def explore_data(self):
        """ Permet de visualiser les variables disponibles dans le NetCDF"""
        print("Variables disponibles :")
        print(self.dataset.variables)

    def close(self):
        self.dataset.close()


def rotate_z(points, angle_deg, z = True):
    """
    Matrice de rotation qui permet de tourner des coordonnées x,y selon un angle.
    Le z permet de d'utiliser un fichier xyz, le désactiver permet de faire tourner juste des données x,y
    

    """
    
    angle_rad = np.radians(angle_deg)
    if z == True: 
        rotation_matrix = np.array([[np.cos(angle_rad), -np.sin(angle_rad), 0],
                                    [np.sin(angle_rad), np.cos(angle_rad), 0],
                                    [0, 0, 1]])
    if z == False:
        rotation_matrix = np.array([[np.cos(angle_rad), -np.sin(angle_rad), 0],
                                    [np.sin(angle_rad), np.cos(angle_rad), 0]])
    return np.dot(points, rotation_matrix)


#%% extractors 


#Remplacé par cdt extract hs 
# def extract_multi_data(file_list, point_coord, data):
#     """ Extraction de plusieurs données de hs dans des réultats 1D pour un point de coordonnée données 
    
#     - file_list = (list) liste de fichier .nc
#     - point_coord = (int) point 
#     - data = (str) nom de la data
    
#     """
#     stock_data = []
#     for dataset in file_list : 
#         xb_data = XB_Loader(dataset)
#         coord_hs = xb_data.get_variable(data)[:,0,point_coord].data
        
#         stock_data.append(coord_hs)

#     return stock_data

#%% plots
def title(filepath):
    title = re.search(r'H(\d+)P(\d+)', filepath)
    if title:
        title_h = int(title.group(1))
        title_p = int(title.group(2))
        print('------------ Lecture des résultats pour : ------------')
        print("H = ", title_h)
        print("Densité = ", title_p)
    else:
        print("Erreur")

    return title_h, title_p


def plot_simple_map(XB_data, varname, moyenne=True, time=None):
    #title_h, title_p = title(filepath)
    title_h, title_p = ('test', 'test')
    if moyenne:
        fig, ax = plt.subplots()
        pcm = ax.pcolormesh(XB_data.x, XB_data.y, np.mean(
            getattr(XB_data, varname), axis=0))
        cbar = plt.colorbar(pcm, ax=ax)
        ax.set_title(
            f'{varname} moyenne sur la simulation pour H = {title_h} et P = {title_p}')

    else:
        fig, ax = plt.subplots()
        pcm = ax.pcolormesh(XB_data.x, XB_data.y,
                            getattr(XB_data, varname)[time])
        cbar = plt.colorbar(pcm, ax=ax)
        ax.set_title(
            f'{varname} à t = {time} sur la simulation pour H = {title_h} et P = {title_p}')


def plot_simple_profil(XB_data, varname, filepath, moyenne=True, time=None):
    # title_h, title_p = title(filepath)
    title_h, title_p = ('test', 'test')
    if moyenne:
        val_moyen = np.mean(getattr(XB_data, varname), axis=0)
        profil = val_moyen[XB_data.y.shape[0] // 2, :]  # Correction ici
        fig, ax = plt.subplots()
        ax.plot(profil)
        ax.set_xlabel('Distance')
        ax.set_ylabel('Valeurs')
        ax.set_title(
            f'{varname} moyenne en profil sur la simulation pour H = {title_h} et P = {title_p}')

    else:
        profil = getattr(XB_data, varname)[
            time, XB_data.y.shape[0] // 2, :]  # Correction ici
        fig, ax = plt.subplots()
        ax.plot(profil)
        ax.set_xlabel('Distance')
        ax.set_ylabel('Valeurs')
        ax.set_title(
            f'{varname} à t = {time} sur la simulation pour H = {title_h} et P = {title_p}')


def xb_multi_loader(filelist):
    dataset_list = []
    for i in filelist:
        dataset_list.append(XB_Loader(i))

    return dataset_list


def xb_subplots(output_list, labels, variable1, variable2, save_title=None):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 9), dpi=200)
    D_out = []
    # Pas sur que ça marche avec des netcdf
    for idx, dataset in enumerate(output_list):
        values_var1 = getattr(dataset, variable1)[
            0, dataset.y.shape[0] // 2, :]
        values_var2 = getattr(dataset, variable2)[
            0, dataset.y.shape[0] // 2, :]
        bot = np.mean(dataset.z, axis=0)
        x_values = dataset.x

        ax1.plot(values_var1, label=labels[idx])
        ax1.set_ylabel(variable1)

        ax2.plot(values_var2, label=labels[idx])
        ax2.set_ylabel(variable2)

        ax2.yaxis.tick_right()
        ax2.yaxis.set_label_position("left")
        ax1.set_ylim(min(values_var1), max(values_var1) + 1)
        ax2.set_ylim(min(values_var2), max(values_var2) + 1)

        D_out.append(values_var2.max())

    ax1_twin = ax1.twinx()
    ax1_twin.plot(bot, color='b')
    ax1_twin.set_ylabel('Profondeur')
    ax1_twin.set_ylim(-10, 10)
    ax2_twin = ax2.twinx()
    ax2_twin.plot(bot, color='b')
    ax2_twin.set_ylabel('Profondeur')
    ax2_twin.set_ylim(-10, 10)
    rect = patches.Rectangle((250, -10), 350, 1, linewidth=1,
                             edgecolor='green', label='Herbier', facecolor='None', hatch='.')
    ax1_twin.add_patch(rect)
    rect1 = patches.Rectangle((250, -10), 350, 1, linewidth=1,
                              edgecolor='green', label='Herbier', facecolor='None', hatch='.')
    ax2_twin.add_patch(rect1)

    if save_title != None:

        fig.savefig(f'dissipation_{save_title}.png')

    plt.tight_layout()
    plt.show()

    return D_out


def xb_subplots_map(output_list, labels, variable1, variable2, save_title=None):
    var_tuple = (variable1, variable2)

    num_rows, num_cols = 5, 2
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(8, 16), dpi=200)

    for idx, col in enumerate(var_tuple):
        label_idx = 0
        for dataset, ax in zip(output_list, axs):
            values_var = getattr(dataset, col).data
            img = ax[idx].imshow(values_var[0, :, :])
            ax[idx].set_title(f'{col} - {labels[label_idx]}')

            # Ajouter une colorbar à chaque graphique
            cbar = plt.colorbar(img, ax=ax[idx])

            label_idx += 1


def xb_damping(superdossier, hs, tp, densite):
    kd_list = []
    for doss in superdossier:
        kd_cas = []
        for cas in doss:
            XB_data = XB_Loader(cas)
            H_off = XB_data.Hrms[:, XB_data.y.shape[0]//2, 1].data
            H_fin = XB_data.Hrms[:, XB_data.y.shape[0]//2, 60].data
            Kd = H_off/H_fin
            kd_cas.append(Kd)
        kd_list.append(kd_cas)

    fig, ax = plt.subplots(figsize=(7, 7), dpi=200)
    for idx, cas in enumerate(kd_list):

        ax.plot(densite, cas,
                label=f'Scénario {idx+1} : Hs = {hs[idx]}, Tp = {tp[idx]}')
        ax.legend(loc='upper left')
        ax.set_xlabel("Densité de l'herbier (Pieds/m2)")
        ax.set_ylabel("Coefficient d'atténuation")
        ax.grid(True)

    return kd_list

def secondes_vers_temps(series_secondes, date_specifiee, format_date):
    date_debut = datetime.strptime(date_specifiee, format_date)
    temps_final = date_debut + pd.to_timedelta(series_secondes, unit='s')
    return temps_final  
#%%

    #bricoles

# for i in range(Dveg_moyen.shape[0]//2):
#     plt.plot(Dveg_moyen[i, :], label=f'Ligne y={i}')

# plt.xlabel('Index temporel (t)')
# plt.ylabel('Valeurs de la ligne à y/2')
# plt.title('Ligne à la moitié de l\'axe y pour chaque ligne y')

# plt.show()

# for i in range(Hrms_moyen.shape[0]//2):
#     plt.plot(Hrms_moyen[i, :], label=f'Ligne y={i}')

# plt.xlabel('Index temporel (t)')
# plt.ylabel('Valeurs de la ligne à y/2')
# plt.title('Ligne à la moitié de l\'axe y pour chaque ligne y')

# plt.show()
