from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import rotate

# Ouvrir le fichier GeoTIFF
dataset = gdal.Open('/home/tfrn/Documents/Stage_TDV/XBeach/Validation/2016-2018/GIS/Litto3D_Beauduc_2016.tif', gdal.GA_ReadOnly)

band1 = dataset.GetRasterBand(1).ReadAsArray()

transform = dataset.GetGeoTransform()

cols, rows = dataset.RasterXSize, dataset.RasterYSize
x, y = np.meshgrid(np.arange(cols), np.arange(rows))
lon = transform[0] + x * transform[1] + y * transform[2]
lat = transform[3] + x * transform[4] + y * transform[5]

angle_degrees = -74 # rotation de x degrés dans le sens horaire
band1_rotated = rotate(band1, angle_degrees, reshape=True, order=3)

mask = band1_rotated != 0
band1_filtered = np.where(mask, band1_rotated, np.nan)

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
ax1, ax2 = axes.ravel()

img1 = ax1.imshow(band1_rotated, cmap='gray')
ax1.set_xlabel('Longitude')
ax1.set_ylabel('Latitude')
plt.colorbar(img1, ax=ax1, label='Valeur Z')

img2 = ax2.imshow(band1_filtered, cmap='gray')
ax2.set_xlabel('Longitude')
ax2.set_ylabel('Latitude')
plt.colorbar(img2, ax=ax2, label='Valeur Z')

crop_data = band1_filtered[1356:5000,2000:3550]

fig, ax = plt.subplots()
ax.imshow(crop_data, cmap='gray')

np.savetxt('/home/tfrn/Documents/Stage_TDV/XBeach/Validation/2016-2018/GIS/Litto3D_Beauduc_2016_prepared.csv', crop_data, delimiter=' ',newline='\n')