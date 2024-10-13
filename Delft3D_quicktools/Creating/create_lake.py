import numpy as np
import os
from os import path, pardir
from datetime import datetime


"""

Script qui permet de créer une bathymétrie, le fichier enc et la grille pour delft3D'


"""

# Répertoire de sauvegarde
savepath = '/home/tfrn/Documents/PhD/D3D/Tests_closed_lake_wind_wave/Test_1/'  # Remplace par ton chemin

# Taille de la grille
bathy_size = 500

# Taille et position du lac
circle_radius = 200
max_depth = -10
shore_max_height = 2
center_x = bathy_size // 2
center_y = bathy_size // 2

#%% 

x, y = np.meshgrid(np.arange(bathy_size), np.arange(bathy_size))
distance_from_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)

# Initialiser la grille
depth = np.zeros((bathy_size, bathy_size))

# Appliquer la profondeur maximale au centre et diminuer vers le bord du cercle
inside_circle = distance_from_center <= circle_radius
depth[inside_circle] = max_depth * np.sqrt(1 - (distance_from_center[inside_circle] / circle_radius)**2)

# Transition vers les bords de la grille
outside_circle = distance_from_center > circle_radius
distance_from_edge = distance_from_center[outside_circle] - circle_radius
max_distance_from_edge = np.sqrt(2) * (bathy_size - circle_radius)
depth[outside_circle] = shore_max_height * (distance_from_edge / max_distance_from_edge)

# Fonction pour écrire le fichier .dep
def write_dep_file(filepath,Z):
    to_save = np.nan*np.zeros((Z.shape[0]+1, Z.shape[1]+1))
    to_save[0:-1, 0:-1] = Z
    to_save[np.isnan(to_save)] = -999
    
    np.savetxt(filepath, to_save, fmt='%16.7E')

def saveas_grd(savepath, name, X, Y):
    
    # missing_value_grid=0.0 # value given as position for missing grid points.
    Coord_System='Cartesian'
    Current_Time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Header for document description
    Parameter_String = """*  
* Deltares, Delft3D-RGFGRID Version 4.16.01.4531, Sep 30 2008, 23:32:27   
* File creation date: {}  
*    """.format(Current_Time)
    
    # Specify the coordinate system used
    Parameter_String += "\nCoordinate System = {}".format(Coord_System)
    
    # Give the value used to represent grid points not to be used
    Parameter_String += "\nMissing Value     =          0.000"
    
    # Specify the number of grid points
    Parameter_String += "\n {} {}".format(X.shape[1], Y.shape[0])
    
    # Add 3 real values that aren't used
    Parameter_String += "\n 0 0 0"
        
    # Create and write the header and parameters to a file
    with open(path.join(savepath, name+".grd"),"w") as gridfile:
        gridfile.write(Parameter_String)
    
    
    gridfile = open(path.join(savepath, name+".grd"),"a")
    np.set_printoptions(threshold=np.inf) 
    
    Format_option = {'float_kind':'{:0.17E}'.format}
    Eta_line_base = "            " # 12 spaces
    
    # getting line limits
    cut_to = range(0, X.shape[1],5)
    
    # assign array blocks to list 5 values by 5 values
    listex = []
    listey = []
    lignex = []
    ligney = []
    for j in range(X.shape[0]):
        lignex = []
        ligney = []
        for i in range(len(cut_to)):
            if i != len(cut_to)-1:
                lignex += [X[j, cut_to[i]:cut_to[i+1]]]
                ligney += [Y[j, cut_to[i]:cut_to[i+1]]]
            else:
                lignex += [X[j, cut_to[i]:]]
                ligney += [Y[j, cut_to[i]:]]
        listex += [lignex]
        listey += [ligney]
    
    towrite = ''
    for i_ligne in range(len(listex)):
        for i_block in range(len(listex[i_ligne])):
            block_text_x = np.array2string(listex[i_ligne][i_block].astype('float64'), formatter=Format_option, max_line_width=500)[1:-1]
            if i_block==0:
                towrite += "\n Eta={:>5}  ".format(i_ligne + 1) + block_text_x
            else:
                towrite += "\n" + Eta_line_base + block_text_x
    for i_ligne in range(len(listey)):
        for i_block in range(len(listey[i_ligne])):
            block_text_y = np.array2string(listey[i_ligne][i_block].astype('float64'), formatter=Format_option, max_line_width=500)[1:-1]
            if i_block==0:
                towrite += "\n Eta={:>5}  ".format(i_ligne + 1) + block_text_y
            else:
                towrite += "\n" + Eta_line_base + block_text_y
    
    gridfile.write(towrite)
    gridfile.close()



# Fonction pour écrire le fichier .enc
def write_enc_file(filepath, X, Y):
    try:
        with open(filepath, 'w') as f:
            f.write(f"     1      1\n")
            f.write(f"   {bathy_size}      1\n")
            f.write(f"   {bathy_size}    {bathy_size}\n")
            f.write(f"     1    {bathy_size}\n")
            f.write(f"     1      1\n")
        print(f"Fichier {filepath} enregistré avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'écriture du fichier {filepath}: {e}")

# Générer les fichiers
write_dep_file(os.path.join(savepath, 'bathy.dep'), depth)
saveas_grd(savepath, 'bathy', x, y)
write_enc_file(os.path.join(savepath, 'bathy.enc'), x, y)

print("Fichiers .dep, .grd, et .enc générés et enregistrés avec succès.")
