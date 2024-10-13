
import gnat as g
import os as os
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np
from scipy import signal
 

# Chemin d'accès
os.chdir('C:/Users/farao/OneDrive/Cours/master/MASTER GCL/M2/Hydro python/')

rbr = g.GnatEquipment()
rbr_file = "206010_20221124_1248.txt"
rbr.autoloadflux(rbr_file)

rbr_name = rbr_file[:6]

#%%

fa = 8 #fréquence d'aquisition (Hz)

Tstart = dt.datetime(year=2022,month=9,day=29,hour=13,minute=54)
Tend =  dt.datetime(year=2022,month=10,day=6,hour=4,minute=34)
deltaT = Tend - Tstart


P_slice = rbr.P[Tstart:Tend]

# On retire la pression atm (hypthèse qu'elle est constante)
atm_P = 1015
P_corr = P_slice-atm_P

#On retire la tendance linéaire du signal total avant découpage
P_corr=signal.detrend(P_corr)

h_timeseries = P_corr / (1015 * 9.81)


#%%  découpage

burst_time = dt.timedelta(hours = 30)

num_points = int(burst_time.total_seconds() * fa)
burst = np.linspace(0, burst_time.total_seconds(), num_points)

num_segments = int(deltaT.total_seconds() / burst_time.total_seconds())

P_burst = []

for i in range(num_segments):
    start_index = i * num_points
    end_index = (i + 1) * num_points
    burst_data = P_corr[start_index:end_index]
    P_burst.append(burst_data)

H_burst = []

for burst_data in P_burst :
    h_timeseries = burst_data / (1015 * 9.81)
    H_burst.append(h_timeseries)

fourier_results_F = []
fourier_results_Y = []

for burst_data in H_burst :    

    N=len(burst_data)
    Y=np.abs(np.fft.rfft(burst_data,N)/N)
    F=np.linspace(0,fa/2,len(Y))
    df=F[1]-F[0]
    
    fourier_results_F.append(F)
    fourier_results_Y.append(Y)
    
#%%


num_subplots_hauteur = len(H_burst)
plt.figure(figsize=(20, 4 * num_subplots_hauteur))

for i, h_series in enumerate(H_burst, start=1):
    plt.subplot(num_subplots_hauteur, 1, i)
    plt.plot(burst, h_series)
    plt.title(f"Série de Hauteur - Série {i}")
    plt.xlabel('Temps (s)')
    plt.ylabel('Hauteur (m)')
    plt.grid()
    plt.tight_layout()


num_subplots_fft = len(fourier_results_F)
plt.figure(figsize=(20, 4 * num_subplots_fft))

for i, (F, Y) in enumerate(zip(fourier_results_F, fourier_results_Y), start=1):
    plt.subplot(num_subplots_fft, 1, i)
    plt.plot(F, Y)
    plt.title(f"Transformée de Fourier - Série {i}")
    plt.xlim(0, 0.8)
    plt.ylim(0, 1E-2)
    plt.xlabel('f (Hz)')
    plt.ylabel('SDE (m^2/Hz)')
    plt.grid()

    plt.tight_layout()
plt.show()

#%% Périodogramme

freq_min = 0
freq_max = 0.4

time_min = 0
time_max = deltaT.total_seconds()

freq_grid, time_grid = np.meshgrid(fourier_results_F, deltaT.total_seconds())

plt.imshow(fourier_results_Y,vmax =5E-3, extent=(freq_min, freq_max, time_min, time_max),
           aspect='auto', cmap='viridis')

plt.xlabel('Fréquences (Hz)')
plt.ylabel('Temps (s)')
plt.colorbar(label='Densité Spectrale d\'Énergie')
plt.show()

#%%

# Calculer le périodogramme
freq_min = 0
freq_max = 0.05

time_min = 0
time_max = deltaT.total_seconds()


plt.pcolormesh(freq_grid, time_grid, Y, cmap='viridis', shading='auto', vmin=0, vmax=5E-5)
plt.colorbar(label='Densité Spectrale d\'Énergie')

plt.xlabel('Fréquences (Hz)')
plt.ylabel('Temps (s)')

plt.show()