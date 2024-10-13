import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Compare_data_tools as cpd

def calculate_brier_score(y_true, y_pred):
    """
    Calcule le Brier score entre deux jeux de données.

    Parameters:
    y_true (array-like): Valeurs réelles
    y_pred (array-like): Valeurs prédites par le modèle

    Returns:
    float: Le Brier score
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    return np.mean((y_true - y_pred)**2)

# %% Load the data

# Chargement de la donnée
chemin_adv = '/home/tfrn/Documents/Stage_TDV/Données hydro/Thomas_workspace/ADV_spectrum_analysis.csv'
chemin_s4 = '/home/tfrn/Documents/Stage_TDV/Données hydro/Thomas_workspace/S4_spectrum_analysis.csv'

start_date = '2005-11-24 00:00'
end_date = '2005-11-27 00:00'
SAMAT_data_adv = cpd.read_SAMAT_data(chemin_adv, start_date, end_date)
SAMAT_data_s4 = cpd.read_SAMAT_data(chemin_s4, start_date, end_date)

# Charmeent de la donnée XB brute
XB_output = ('/home/tfrn/Documents/Stage_TDV/XBeach/Calibration/1D/Tests et autres/Test_16/d/xboutput.nc',
             '/home/tfrn/Documents/Stage_TDV/XBeach/Calibration/1D/Tests et autres/Test_16/b/xboutput.nc')

# Entrer les valeurs de calib
labels = ('roelvink 1','roelvink 2'
          )

# Paramètre modélisé (pour le titre)
paramètre = 'roelvink'

# %% fait l'extraction des données dans une liste pour chaque point correspondant à un appareil

point_adv = 10
point_s4 = 16

adv_stock = []
for i in XB_output:
    data = cpd.extract_var_point(i,'H', point_adv, start_date)
    data.set_index('DateTime', inplace=True)
    adv_stock.append(data)

s4_stock = []
for i in XB_output:
    data = cpd.extract_var_point(i,'H', point_s4, start_date)
    data.set_index('DateTime', inplace=True)
    s4_stock.append(data)

# %% Brier Score

# brier_adv = []
# for i in adv_stock:
#     resampled_data = i.resample('H').mean()
#     resampled_data = resampled_data.iloc[:-1]  # Remove the last value
#     resampled_samat_data = SAMAT_data_adv.set_index('Date').resample('H').mean()
#     brier_adv.append(calculate_brier_score(resampled_samat_data.Hs_p, resampled_data.H))

# brier_s4 = []
# for i in adv_stock:
#     resampled_data = i.resample('H').mean()
#     resampled_data = resampled_data.iloc[:-1]  # Remove the last value
#     resampled_samat_data = SAMAT_data_s4.set_index('Date').resample('H').mean()
#     brier_s4.append(calculate_brier_score(resampled_samat_data.Hs_p, resampled_data.H))
    


# %% plot pour mémoire
fig, axs = plt.subplots(2, 1, sharex=True, figsize=(13, 6))

# Axis 0 = adv
for simu in range(len(adv_stock)):
    axs[0].plot(adv_stock[simu].index, adv_stock[simu].H.rolling(window=60).mean(), label=labels[simu])
axs[0].set_ylabel('Hs (m)')
axs[0].plot(SAMAT_data_adv.Date, SAMAT_data_adv.Hs_p, 'm',label='Hs in-situ')
axs[0].grid('on')

# Axis 1 = s4
for simu in range(len(s4_stock)):
    axs[1].plot(s4_stock[simu].index, s4_stock[simu].H.rolling(window=60).mean())
axs[1].set_ylabel('Hs (m)')
axs[1].plot(SAMAT_data_s4.Date, SAMAT_data_s4.Hs_p, 'm')
axs[1].grid('on')
fig.tight_layout()
fig.legend(title=f'{paramètre}', loc=7)
fig.savefig(f'/home/tfrn/Documents/Stage_TDV/Mémoire/Figures/Comparaison_{paramètre}.png')
