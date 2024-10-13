import matplotlib.pyplot as plt
import numpy as np
import os

#%% avec barre

m = 0.78 
A = 0.067 * 0.5 ** 0.44

x = np.arange(1, 1000, 1)
# x = x[::-1]
h_x = A * x ** m
h_x = 0 - h_x
pente = h_x.max() / x.max()
barre = 0.8 * np.sin(0.05 * x-25)
indices_a_modifier = range(60, 124) 
h_x[indices_a_modifier] -= barre[indices_a_modifier]
h_x = h_x[::-1]
fig, ax = plt.subplots(figsize=(10,3))
fig.suptitle('profil de plage')
ax.plot(x, h_x)
plt.show()

np.savetxt("/home/tfaraon/Bureau/exemple_bathy_1D.dat", h_x, delimiter=" ")

#%% Sans barre

m = 0.78 
A = 0.067 * 0.5 ** 0.44

x = np.arange(1, 1000, 1)
# x = x[::-1]
h_x = A * x ** m
h_x = 0 - h_x
pente = h_x.max() / x.max()
h_x = h_x[::-1]
fig, ax = plt.subplots(figsize=(10,3))
fig.suptitle('profil de plage')
ax.plot(x, h_x)
plt.show()

np.savetxt("/home/tfaraon/Documents/Cours/projet/bathy_DEAN.dat", h_x, delimiter=" ")

#%% Fond plat 

size = 1000
value = -10
h_x = [value] * size 
h_x = h_x[::-1]

np.savetxt("/home/tfaraon/Documents/Cours/projet/bathy_projet_flatDEAN.dat", h_x, delimiter=" ")

#%% 2D

size = 100
value = -10
depth = np.full((size,size),value)
np.savetxt("/home/tfaraon/Documents/Cours/projet/bathy_projet_flat_2D.dat", depth, delimiter=" ")
