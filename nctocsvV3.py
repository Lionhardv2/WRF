import numpy as np
import pandas as pd
import netCDF4 as nt
import matplotlib.pyplot as plt

ncfile = 'wrfout_d03_2018_02-01.nc'
rootgroup = nt.Dataset(ncfile,'r', format='NETCDF3_64BIT_OFFSET')
index = rootgroup.variables["LU_INDEX"]
time1 = rootgroup.variables["Times"][:] # read time in format byte
y = rootgroup.variables['XLAT'][:]      # read latitutde variable
x = rootgroup.variables['XLONG'][:]     # read longitude variable
temp2 = rootgroup.variables['T2'][:]    # read temperature at 2m
v10 = rootgroup.variables["V10"][:]     # read wind velocity at 10m
print(rootgroup.variables["V10"])
rootgroup.close()
dt = np.dtype('b')                       # byte, native byte order
#********************************************************************************
#                   convert  byte to string
#                   ***********************
strs = ["" for x in range(0,24)]
for i in range(1,25):
    strs[i-1] = str(time1[i,:], "utf-8")
#print(strs)
#********************************************************************************
#               looking for latitude near to Weather Station from Qollana
#               *********************************************************
idx_lat = (y[1,:,1]>=-17.63)*(y[1,:,1]<=-17.62)
idxlat=np.nonzero(idx_lat)[0]
#print(y[1,idxlat,1])
lat_near = y[1,idxlat,1].min()  
idx_latf = y[1,:,1]==lat_near
idxlat=np.nonzero(idx_latf)[0]
print(idxlat) 
#print(lat_near)   
#********************************************************************************
#               looking for longitude near to the Weather Station from Qollana
#               **************************************************************
idx_lon = (x[1,1,:]>=-65.29)*(x[1,1,:]<=-65.20)
idxlon=np.nonzero(idx_lon)[0]
#print(x[1,1,idx_lon])
lon_near = x[1,1,idx_lon].min()
idx_lonf = x[1,1,:]==lon_near
idxlon=np.nonzero(idx_lonf)[0]
print(idxlon)
print(lon_near,lat_near)


print(idxlon)
print(idxlat)
print(x[1,idxlat,idxlon])
print(y[1,idxlat,idxlon])
#********************************************************************************
#               Extract Data T2 at 2m
#               *********************
print((temp2[1,idxlat,idxlon]))
temp2m = np.zeros(24,dtype="f")
for i in range(1,25):
    temp2m[i-1] = float(temp2[i,idxlat,idxlon])

print(temp2m-273)

#********************************************************************************
#               Extract Data V10 at 10m
#               ***********************
print((v10[1,idxlat,idxlon]))

v10m = np.zeros(24,dtype="f")
for i in range(1,25):
    v10m[i-1] = float(v10[i,idxlat,idxlon])

print(v10m)

#********************************************************************************
#               Exporting Data to CSV format
#               ****************************

df2 = pd.DataFrame({'Time': strs,
                    'T3s': temp2m,
                    'W10s2': v10m
                    })
# save dataframe dataframe.to_csv()
df2 = df2[['Time', 'T3s','W10s2']]       #set order of columns

print(df2)

df2.to_csv(path_or_buf="df010218.csv")
