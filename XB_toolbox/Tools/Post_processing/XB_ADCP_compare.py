import ADCP_tools as adcp
import Xbeach_reader as XBr
import numpy as np
import matplotlib.pyplot as plt 

adcp_data = adcp.ADCP_current_from_matlab('/media/tfrn/disk2/save_hydro/save_struc/ADCP.mat')
XB_data = XBr.XB_Loader('/home/tfrn/Documents/Stage_TDV/XBeach/Calibration/2D/2022/Test_19/Tideloc/xboutput.nc')

XB_U= XB_data.get_variable('u').data
XB_V= XB_data.get_variable('v').data
XB_X= XB_data.get_variable('globalx').data
XB_Y= XB_data.get_variable('globaly').data

XB_U[XB_U < -10] = np.nan
XB_V[XB_U < -10] = np.nan

XB_curr = np.column_stack((XB_U[:,94,128],XB_V[:,94,128]))

XB_curr_rot = XBr.rotate_z(XB_curr, 106.1, z = False) 

#%%

fig, (ax1,ax2) = plt.subplots(1,2)
ax1.hist2d(adcp_data[:,0],adcp_data[:,1] ,bins=500, cmap='Blues')
ax1.set_title("ADCP")
ax1.set_xlim(-1,1)
ax1.set_ylim(-1,1)
ax1.set_xlabel("X")
ax1.set_ylabel("Y")

ax2.hist2d(XB_curr_rot[:,0], XB_curr_rot[:,1], bins=100, cmap='Blues')
ax2.set_title("XBeach")
ax2.set_xlim(-1,1)
ax2.set_ylim(-1,1)
ax2.set_xlabel("X")
ax2.set_ylabel("Y")
fig.suptitle('Densité des points - courants')

fig3, ax3 = plt.subplots()
ax3.quiver(XB_X,XB_Y, XB_U.mean(axis=0), XB_V.mean(axis=0))
ax3.invert_xaxis()

