#python script
import numpy as np
import pandas as pd
import netCDF4 as nt
import matplotlib.pyplot as plt

ncfile = 'wrfout_d03_2018_02-01.nc'
rootgroup = nt.Dataset(ncfile,'r', format='NETCDF3_64BIT_OFFSET')
index = rootgroup.variables["LU_INDEX"]
time1 = rootgroup.variables["Times"][:]
y = rootgroup.variables['XLAT'][:] # read latitutde variable
x = rootgroup.variables['XLONG'][:] # read longitude variable
temp2 = rootgroup.variables['T2'][:] # read temperature at 2m
v10 = rootgroup.variables["V10"][:]
#time_unit = rootgroup.history
#print("Latitude: ",y[2,119,154], "Longitude:",x[2,119,154]) # print latitutde, longitude
rootgroup.close()
dt = np.dtype('b')  # byte, native byte order
#********************************************************************************
#                   convert  byte to string
#                   ***********************
strs = ["" for x in range(0,25)]
for i in range(1,25):
    strs[i-1] = str(time1[i,:], "utf-8")
#print(strs)
#********************************************************************************
#               looking for latitude near to Weather Station from Qollana
#               *********************************************************
idx_lat = (y[1,:,:]>=-17.6291)*(y[1,:,:]<=-17.6290)
idxlat=np.nonzero(idx_lat)[0]
idx_fin= (y[1,idxlat.min(),:]>=-17.6291)*(y[1,idxlat.min(),:]<=-17.6290)
idxlat2=np.nonzero(idx_fin)[0]
lat_near=y[1,idxlat.min(),idxlat2].min()        # latitude near to Qollana
print(y[1,idxlat.min(),idxlat2].min())          
#********************************************************************************
#               looking for longitude near to the Weather Station from Qollana
#               **************************************************************
idx_lon = (x[1,:,:]>=-66.0)&(x[1,:,:]<=-65.00)
idxlon=np.nonzero(idx_lon)[0]
print(idxlon)
print(x[1,idxlon.min(),:])
idx_fin2= (x[1,idxlon.max(),:]>=-66.0)*(x[1,idxlon.max(),:]<=-65.00)
idxlon2=np.nonzero(idx_fin2)[0]
lon_near=x[1,idxlon.min(),idxlon2].max()        # longitude near to Qollana
print(lon_near)          



