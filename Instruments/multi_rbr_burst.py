import pandas as pd
import matplotlib.pyplot as plt
import gnat as g
import datetime as dt
import numpy as np


rbr_paths = ["C:/Users/farao/OneDrive/Cours/master/MASTER GCL/M1/Déploiement Banyuls/Analyse/Data/Jour2/RBR/Seiche/203441_Balise13.txt",
             "C:/Users/farao/OneDrive/Cours/master/MASTER GCL/M1/Déploiement Banyuls/Analyse/Data/Jour2/RBR/Seiche/206011_Balise14.txt",
             "C:/Users/farao/OneDrive/Cours/master/MASTER GCL/M1/Déploiement Banyuls/Analyse/Data/Jour2/RBR/BASE/209738_base.txt"]


P_data = pd.DataFrame()
i = 0

for rbr_file in rbr_paths:
    rbr = g.GnatEquipment()
    
    try:
        rbr.autoloadflux(rbr_file)
        P_data[i] = rbr.data[327680]
        i += 1
        
    except Exception as e:
        print(f"Erreur lors du chargement du fichier {rbr_file}: {e}")

#%% Mise en forme et correction des données

# =============================================================================
#         
# plt.plot(P_data.index, P_data.iloc[:,0])
# plt.plot(P_data.index, P_data.iloc[:,1], 'r')
# plt.plot(P_data.index, P_data.iloc[:,2], 'g')
# 
# =============================================================================

# Définir le temps de la mesure
Tstart = dt.datetime(year=2023,month=2,day=14,hour=11,minute=30)
Tend = dt.datetime(year=2023,month=2,day=15,hour=13,minute=50)
deltaT = Tend - Tstart

#Découpage du jeu de donnée
rbr_P_slice = P_data[Tstart:Tend]

#Conversion pression en hauteur par hydrostatique
h_timeseries = pd.DataFrame()
h_timeseries = rbr_P_slice/(9.81*1024)

fa = 2

h4window = int((dt.timedelta(hours = 4).total_seconds()*fa))

H_corrected_roll4 = pd.DataFrame()

H_corrected_roll4 = h_timeseries - h_timeseries.rolling(window = h4window).mean()

# =============================================================================
        
# plt.plot(H_corrected_roll4.index, H_corrected_roll4.iloc[:,0])
# plt.plot(H_corrected_roll4.index, H_corrected_roll4.iloc[:,1], 'r')
# plt.plot(H_corrected_roll4.index, H_corrected_roll4.iloc[:,2], 'g')

# =============================================================================

H_corrected_roll4 = H_corrected_roll4.fillna(0)
#%%

burst_time = dt.timedelta(hours = 1)

num_points = int(burst_time.total_seconds() * fa)
burst = np.linspace(0, burst_time.total_seconds(), num_points)

num_segments = int(deltaT.total_seconds() / burst_time.total_seconds())

H_burst = []

for i in range(num_segments):
    start_index = i * num_points
    end_index = (i + 1) * num_points
    burst_data = h_timeseries[start_index:end_index]
    burst_data = burst_data / (1015 * 9.81)
    H_burst.append(burst_data)
    
#%% FFT
fourier_liste = []

for i in range(num_segments):
    fourier_results = {}  # Initialiser un dictionnaire pour stocker les résultats
    
    for column in H_corrected_roll4.columns:
        N = len(H_burst[i])
        
        # Utilisez H_burst[i] pour créer le DataFrame
        new_df = pd.DataFrame({'Amplitude': np.abs(np.fft.rfft(H_burst[i], N) / N), 'Frequency': np.linspace(0, fa/2, N)})
        
        fourier_results[column] = new_df
    
    fourier_liste.append(fourier_results)  # Ajouter les résultats à la liste

# =============================================================================
# for column, df in fourier_results.items():
#     plt.figure(figsize=(10, 6))  
#     plt.plot(df['Frequency'], df['Amplitude'])
#     plt.title(f'FFT Result for {column}')
#     plt.xlabel('Frequency')
#     plt.ylabel('Amplitude')
#     plt.grid(True)
#     plt.show()
# =============================================================================
