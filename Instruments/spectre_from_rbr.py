
import gnat as g
import os as os
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np
from scipy import signal
# Chemin d'accès
os.chdir('C:/Users/farao/OneDrive/Cours/master/MASTER GCL/M2/Terrain Stmand/RBR/')
#----------#
# Access files with GNAT
#----------#


rbr = g.GnatEquipment()

rbr_file = "200380_20230920_1035.txt"

rbr_name = rbr_file[:6]

rbr.autoloadflux(rbr_file)

fa = 8 #fréquence d'aquisition (Hz)

"""
print(testrbr) => afficher le format de fichier
print(testrbr.P) => pour affihcer les données de pression
"""

Tstart = dt.datetime(year=2023,month=9,day=19,hour=13,minute=17)
deltaT = dt.timedelta(minutes = 52)
Tend = Tstart + deltaT

rbr_slice = rbr.P[Tstart:Tend]


atm_P = 1015
rbr_corr = rbr_slice-atm_P

rbr_corr=signal.detrend(rbr_corr)


# h_timeseries = pd.DataFrame()
# h_timeseries["Hauteur"] = rbr_corr/(9.81*1015)
h_timeseries = rbr_corr/(9.81*1015)



H=np.nanmean(rbr_corr)


N=len(h_timeseries)
Y=np.abs(np.fft.rfft(h_timeseries,N)/N)
F=np.linspace(0,fa/2,len(Y))
df=F[1]-F[0]




#­spectre moche sans correction
plt.figure(1)
plt.plot(F,Y)
plt.title( f"Densité spectrale d'énergie par transformée de Fourier - RBR n°{rbr_name}")
plt.xlim(0,0.4)
plt.ylim(1E-10,5E-3)
plt.xlabel('F (Hz)')
plt.ylabel('SDE (m^2/Hz)')
plt.grid()
plt.legend()

