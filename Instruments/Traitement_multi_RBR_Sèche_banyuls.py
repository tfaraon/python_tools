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

#%% FFT

fourier_results = {}

for column in H_corrected_roll4.columns:
    N = len(H_corrected_roll4[column])
    
    fft_result = np.fft.rfft(H_corrected_roll4[column], N) / N
    
    new_df = pd.DataFrame({'Amplitude': np.abs(fft_result), 'Frequency': np.linspace(0, fa/2, len(fft_result))})
    
    fourier_results[column] = new_df
    
plt.figure(figsize=(10, 6))

for column, df in fourier_results.items():
    plt.plot(df['Frequency'], df['Amplitude'], label=column)

plt.title('FFT Results for All Columns')
plt.xlabel('Frequency')
plt.ylabel('Amplitude')
plt.xlim(0, 0.5)
plt.ylim(0,0.002)
plt.grid(True)
plt.legend()
plt.show()