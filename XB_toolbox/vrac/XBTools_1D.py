# import default modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import sys
import os

## import xbeach tools
#sys.path.append(os.path.abspath(os.path.join('..' )))

from xbTools.grid.creation import xgrid, ygrid
from xbTools.grid.extension import seaward_extend
from xbTools.xbeachtools import XBeachModelSetup
from xbTools.general.wave_functions import offshore_depth


#%% load data
bathy = np.loadtxt('/home/tfrn/Documents/Stage_TDV/XBeach/Calibration/1D/profil_calibration.dep')

#%% cut bthy 

seuil = -9  # Seuil à partir duquel couper
bathy = bathy[bathy >= seuil]
#%%

## set bathy grid
nx = len(bathy)
ny = 0
dx = 1
dy = 0

x = np.linspace(0,(nx-1)*dx,nx)

## plot
plt.figure()
plt.plot(x,bathy)
plt.xlabel('x [m]')
plt.ylabel('z [m]')
plt.grid('on')
plt.title('bathy')

#%% Make grid

xgr,zgr = xgrid(x, bathy,dxmin=1, dxmax=15)


plt.figure(figsize=(10,6))
plt.plot(x*8,bathy,'-o')
plt.plot(xgr*8,zgr,'.-')
plt.legend(['Bathy','Grille'])
plt.xlabel('x [m]')
plt.ylabel('z [m]')
plt.grid('on')
plt.title('Bathymétrie et grille 1D')
plt.tight_layout()
plt.savefig('/home/tfrn/Documents/Stage_TDV/Mémoire/Figures/grille_1d.png')    


zgr = np.interp(xgr, x, bathy)

plt.figure()
plt.plot(x,bathy,'-o')
plt.plot(xgr,zgr,'.-')
plt.xlabel('x [m]')
plt.ylabel('x [m]')
plt.title('xb bathy')
plt.grid('on')


# d_start, slope, Hm0_shoal = offshore_depth(Hm0=2, Tp=9, depth_offshore_profile=10, depth_boundary_conditions=20)

# xgr, ygr, zgr = seaward_extend(xgr,[0],zgr,slope=1/70,depth=-20)



plt.figure()
plt.plot(xgr.T,zgr[:,:].T)
plt.xlabel('x [m]')
plt.ylabel('z [m]')
#%% structure 
# A défaut de mieux je le fais à la main. 

indice = np.where(bathy >= -1) #Permet de repérer à partir de quand la bathy est en dessous du seuil. 
ne_layer = np.zeros_like(xgr)  #copie la grille pour avoir la meme structure de donnée
ne_layer[indice] = 10             # La zone érodable est érodable sur 10 m de fond et la digue reste 0



#%% Model setup 
xb_setup = XBeachModelSetup('Test')

print(xb_setup)

xb_setup.set_grid(xgr,None,zgr)
xb_setup.set_nebed(ne_layer,struct=1)

xb_setup.set_waves('parametric',{'Hm0':2, 'Tp':5, 'mainang':270, 'gammajsp':3.3, 's' : 10000, 'fnyq':1})
#xb_setup.set_waves('jonstable',{'Hm0':[1.5, 2, 1.5],'Tp':[4, 5, 4],'gammajsp':[3.3, 3.3, 3.3], 's' : [20,20,20], 'mainang':[270,280, 290],'duration':[3600, 3600, 3600],'dtbc':[1,1,1]})

xb_setup.set_params({'Wavemodel':'surfbeat',
                     'morphology':1,
                     'befriccoef':0.01,
                     'tstop':3600,
                     'zs0':0,
                     'nglobalvar':['zb','zs','H'],
                     'npointvar':['zs','zb'],
                     'nmeanvar':['zb'],
                     'npoints':['1 0', '6 0', '10 0', '12 0']})

sim_path = '/home/tfrn/Documents/Stage_TDV/XBeach/Calibration/Data/test_grid'
if not os.path.exists(sim_path):
    os.mkdir(sim_path)
xb_setup.write_model(sim_path)
