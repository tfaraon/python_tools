import numpy as np
import matplotlib.pyplot as plt

bathy_size = 100

d = 1  # Plants per m2

circle_radius = 17
center_x = 37
center_y = bathy_size // 2

x, y = np.meshgrid(np.arange(bathy_size), np.arange(bathy_size))

distance_from_center = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
plants_within_circle = distance_from_center <= circle_radius
density_grid = np.zeros((bathy_size, bathy_size))
density_grid[plants_within_circle] = d

plt.figure(figsize=(8, 6))
plt.imshow(density_grid, cmap='viridis', extent=[0, bathy_size, 0, bathy_size], origin='lower')
plt.colorbar(label='Densité (pieds/m2)')
plt.title("Distribution 2D de l'herbier de posidonie")
plt.show()

np.savetxt('mapherbier.txt', density_grid)

#%% Bathy

