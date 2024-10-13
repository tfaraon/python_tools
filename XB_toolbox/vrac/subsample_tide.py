import pandas as pd
import matplotlib.pyplot as plt

# Charger le fichier CSV
df = pd.read_csv(
    "/home/tfrn/Documents/Stage_TDV/Données hydro/Data_niveau_lagunes/tide_BDC_2018_10min.csv",
    sep=",",
    decimal=".",
    names=['temps', 'hauteur'])

intervalle_initial = 10*60  # en secondes

nouvel_intervalle = 3600  # en secondes

facteur_subsampling = nouvel_intervalle / intervalle_initial

df_subsamp = df.iloc[::int(facteur_subsampling)]



#%%Marseille uniquement !  IGN 69 
# df_subsamp["hauteur"] =  df_subsamp["hauteur"] - 0.33

#%%

fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
axs[0].plot(df['temps'], df['hauteur'],
            label='Données originales', color='blue')
axs[0].set_title('Données originales')
axs[0].set_ylabel('Hauteur d\'eau')
axs[1].plot(df_subsamp['temps'], df_subsamp['hauteur'],
            label='Données sous-échantillonnées', color='red')
axs[1].set_title('Données sous-échantillonnées')
axs[1].set_xlabel('Temps')
axs[1].set_ylabel('Hauteur d\'eau')
axs[0].legend()
axs[1].legend()



df_subsamp.to_csv("/home/tfrn/Documents/Stage_TDV/Données hydro/Data_niveau_lagunes/tide_BDC_2018.txt", index=False, header= False, decimal='.', sep=' ')
