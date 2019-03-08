#************************************************************************************************
#                       Convert Data nc to csv V1.0
#************************************************************************************************
# name: Jose Feliciano Ibañez Quiroz
#************************************************************************************************

import matplotlib.pyplot as plt
import netCDF4
import numpy as np
import pandas as pd

ncfile = 'wrfout_d03_2018_03-01.nc'     # el programa debe estar en la misma carpeta de las extensiones .nc
rootgroup = netCDF4.Dataset(ncfile,'r', format='NETCDF3_64BIT_OFFSET') # import data extension nc
index = rootgroup.variables["LU_INDEX"]
time1 = rootgroup.variables["Times"][:] # read time in format byte
y = rootgroup.variables['XLAT'][:]      # read latitutde variable
x = rootgroup.variables['XLONG'][:]     # read longitude variable
temp2 = rootgroup.variables['T2'][:]    # read temperature at 2m
v10 = rootgroup.variables["V10"][:]     # read wind velocity component at 10m
u10 = rootgroup.variables["U10"][:]     # read wind velocity component at 10m
#print(rootgroup.variables)
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
idx_lat = (y[1,:,1]>=-17.63)*(y[1,:,1]<=-17.62) # comparison of domains in each grid of 1000m2
idxlat=np.nonzero(idx_lat)[0]                   # excluding domains out of range
lat_near = y[1,idxlat,1].min()                  # excluding only one latitude
idx_latf = y[1,:,1]==lat_near                   # getting the index of latitude
idxlat=np.nonzero(idx_latf)[0]                  # ...........
idxlat=idxlat+1
print(idxlat) 
#print(lat_near)   
#********************************************************************************
#               looking for longitude near to the Weather Station from Qollana
#               **************************************************************
idx_lon = (x[1,1,:]>=-65.29)*(x[1,1,:]<=-65.20) # comparison of domains in each grid of 1000m2
idxlon=np.nonzero(idx_lon)[0]                   # excluding domains out of range
#print(x[1,1,idx_lon])
lon_near = x[1,1,idx_lon].min()                 # excluding only one latitude
idx_lonf = x[1,1,:]==lon_near                   # getting the index of latitude
idxlon=np.nonzero(idx_lonf)[0]                  # ...........
idxlon = idxlon+1
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
temp2m = np.zeros(24,dtype="f")   # generating space for temp2 of 24 spaces
for i in range(1,25):
    temp2m[i-1] = float(temp2[i,idxlat,idxlon]) #saving each temperature by date

temp2m = temp2m-273.15           # converter Kelvin degree to celsius degree
print(temp2m)

#********************************************************************************
#               Extract Data V10 at 10m
#               ***********************
print((v10[1,idxlat,idxlon]))   

v10m = np.zeros(24,dtype="f")    # generating a vector of zeros of 24 spaces
for i in range(1,25):
    v10m[i-1] = float(v10[i,idxlat,idxlon]) # saving each component of velocity by date

print(v10m)

#********************************************************************************
#               Extract Data U10 at 10m
#               ***********************
print((u10[1,idxlat,idxlon]))   

u10m = np.zeros(24,dtype="f")    # generating a vector of zeros of 24 spaces
for i in range(1,25):
    u10m[i-1] = float(u10[i,idxlat,idxlon]) # saving each component of velocity by date

print(u10m)

#********************************************************************************
#               Calculating the wind resultant
#               ******************************
#   both components generated the resultant R <- sqrt(U²+V²)
# V ^   
#   |  / R=sqrt(U²+V²)
#   | /
#   |/)  tetha= arctg(V/U)
#   +---------->
#               U
R = np.sqrt((u10m*u10m) + (v10m*v10m))
print("\n Resultant of the velocity of the wind in m/s")
print(R)                                # Print the resultant

#  generating the direction of the resultant
tetha = np.arctan((v10m/u10m))          # tetha in radians
tetha = tetha * 180/np.pi               # Converting to degrees
print("\n Direccion of the velocity in degrees")
print(tetha)
#********************************************************************************
#               Exporting Data to CSV format
#               ****************************

df2 = pd.DataFrame({'Time': strs,
                    'T2s2': temp2m,
                    'W10s2': R,
                    'Wds2': tetha
                    })

df2 = df2[['Time', 'T2s2','W10s2','Wds2']]          # set order of columns

print(df2)
print(df2.dtypes)

# generating date for file.csv

file_csv = strs[1]
file_sep = file_csv.split('_')              # function to separate strings in vectors


file_csv_name = "df"+file_sep[0] + ".csv"   # generating the name for csv file

print(file_csv_name)                        # name of the extension csv
df2.to_csv(path_or_buf=file_csv_name)       # save dataframe dataframe.to_csv()


