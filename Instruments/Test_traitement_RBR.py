import pandas as pd
import matplotlib.pyplot as plt
import gnat as g
import datetime as dt
import numpy as np

#Chargement de la donnée
rbr_file = "C:/Users/farao/OneDrive/Cours/master/MASTER GCL/M1/Déploiement Banyuls/Analyse/Data/Jour2/RBR/BASE/209738_base.txt"
rbr_name = rbr_file[:6]

baro_file = "C:/Users/farao/OneDrive/Cours/master/MASTER GCL/M1/Déploiement Banyuls/Baro/Barolog_secu2126673_14022023(1).csv"

rbr = g.GnatEquipment()
rbr.autoloadflux(rbr_file)

baro = pd.read_csv(baro_file,
            sep = ";",
            decimal=",",
            header=(9),
            encoding=("latin-1")
            )

#Index à changer, propre au rbr
rbr_P  = rbr.data[327680]

#Mise en forme de la donnée baro en remplaçant la colonne Date et Time par un index DateTime
baro['datetime'] = pd.to_datetime(baro['Date']+' '+baro['Time'])
baro = baro.set_index(baro['datetime'])

baro = baro.drop(columns = ['Date','Time','datetime'])

#%% Vérification de la donnée - petit plot 

fig, ax1 = plt.subplots()
ax1.plot(rbr.P)

ax2 = ax1.twinx()
ax2.sharex(ax1)
ax2.plot(baro['LEVEL'])

#%%Découpage et paramètres 

# Définir le temps de la mesure
Tstart = dt.datetime(year=2023,month=2,day=14,hour=11,minute=15)
Tend = dt.datetime(year=2023,month=2,day=15,hour=13,minute=50)
deltaT = Tend - Tstart

#Découpage du jeu de donnée
rbr_P_slice = rbr_P[Tstart:Tend]

#Conversion pression en hauteur par hydrostatique
h_timeseries = pd.DataFrame()
h_timeseries['H'] = rbr_P_slice/(9.81*1024)

fa = 2
#%% Traitements 

h4window = int((dt.timedelta(hours = 4).total_seconds()*fa))
h_timeseries["roll4"]= h_timeseries['H'].rolling(window = h4window).mean()

h6window = int((dt.timedelta(hours = 6).total_seconds()*fa))
h_timeseries["roll6"]= h_timeseries['H'].rolling(window = h6window).mean()


h_timeseries['H_corr4'] = h_timeseries['H'] - h_timeseries['roll4']
h_timeseries['H_corr6'] = h_timeseries['H'] - h_timeseries['roll6']


# ==========================Si besoin d'afficher===============================
#
# fig, ax1 = plt.subplots()
# ax1.plot(h_timeseries.index, h_timeseries['H'])

# ax2 = ax1.twinx()
# ax2.plot(h_timeseries['roll4'], c='g')

plt.figure(2)
ax3 = plt.subplot(211)
ax3.plot(h_timeseries['H_corr4'], c='r')

ax4 = plt.subplot(212)
ax4.plot(h_timeseries['H_corr6'], c='r')
# 
# =============================================================================

H_swl = h_timeseries['H_corr4'].mean() 

#On remplace les nan par 0 pour la transformée de fourier
h_timeseries = h_timeseries.fillna(0)

#%% Transformée de Fourier et spectre entier

""" Le spectre est calculé avec le H_corr6 pour masquer les oscillations >6h """

N=len(h_timeseries["H_corr6"])
Y=np.abs(np.fft.rfft(h_timeseries["H_corr6"],N)/N)
F=np.linspace(0,fa/2,len(Y))
df=F[1]-F[0]

plt.figure(figsize=(10,4))
plt.plot(F,Y)
plt.title( f"Densité spectrale d'énergie par transformée de Fourier - RBR n°{rbr_name}")
plt.xlim(0,0.05)
plt.ylim(1E-10,5E-3)
plt.xlabel('F (Hz)')
plt.ylabel('SDE (m^2/Hz)')
plt.grid()
plt.legend()

#%% Calculs 

Hrms = 1/8 * np.sqrt(sum(Y))

# Calcul du HS pour les VLF
borne_vlf = np.where(F <= 0.00055)
Y_VLF = Y[borne_vlf]

m0_VLF = sum(Y_VLF)
Hs_VLF = 4*np.sqrt(m0_VLF)

# Calcul du HS pour LF-IG
borne_LF = np.where((F > 0.00055) & (F <= 0.03))
Y_LF = Y[borne_LF]

m0_LF = sum(Y_LF)
Hs_LF = 4*np.sqrt(m0_LF)




