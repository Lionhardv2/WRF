#************************************************************************************************
#                       Convert Data nc to csv V3.0
#************************************************************************************************
# name: Jose Feliciano Ibañez Quiroz
#************************************************************************************************
 
import matplotlib.pyplot as plt
import netCDF4
import numpy as np
import pandas as pd
from netCDF4 import MFDataset
from glob import glob           # to look for files.nc
import os
from shutil import rmtree       # to remove a Directory that contain files
import os.path as path          # to verify whether exits a Directory
 
 
# choosing every file.nc 
def ls(expr = 'wrfout_d03*'):
    return glob(expr)
# Importing every file.nc
 
Files = ls()
print(len(Files))
 
ncfile = 'wrfout_d03_2018-05-31_18:00:00'     # el programa debe estar en la misma carpeta de las extensiones .nc
rootgroup = netCDF4.Dataset(ncfile,'r', format='NETCDF3') # import data extension nc
y = rootgroup.variables['XLAT'][:]      # read latitutde variable
x = rootgroup.variables['XLONG'][:]     # read longitude variable
alt = rootgroup.variables["HGT"][:]     # read hight variables
rootgroup.close()
#********************************************************************************
#                   convert  byte to string
#                   ***********************
#strs = ["" for x in range(0,24)]
#for i in range(1,25):
#    strs[i-1] = str(time1[i,:], "utf-8")
#print(strs)
#********************************************************************************
#               looking for latitude near to Weather Station from Qollana
#               *********************************************************
 
#df2 = df2[['Time', 'T2s2','W10s2','Wds2']]          # set order of columns
 
#********************************************************************************
#               looking for latitude near to Weather Station from Qollana
#               *********************************************************
idx_lat = (y[0,:,1]>=-17.63)*(y[0,:,1]<=-17.62) # comparison of domains in each grid of 1000m2
idxlat=np.nonzero(idx_lat)[0]                   # excluding domains out of range
lat_near = y[0,idxlat,1].min()                  # excluding only one latitude
idx_latf = y[0,:,1]==lat_near                   # getting the index of latitude
idxlat=np.nonzero(idx_latf)[0]                  # ...........
idxlat=idxlat+1
print(idxlat) 
#print(lat_near)   
#********************************************************************************
#               looking for longitude near to the Weather Station from Qollana
#               **************************************************************
idx_lon = (x[0,1,:]>=-65.29)*(x[0,1,:]<=-65.20) # comparison of domains in each grid of 1000m2
idxlon=np.nonzero(idx_lon)[0]                   # excluding domains out of range
#print(x[1,1,idx_lon])
lon_near = x[0,1,idx_lon].min()                 # excluding only one latitude
idx_lonf = x[0,1,:]==lon_near                   # getting the index of latitude
idxlon=np.nonzero(idx_lonf)[0]                  # ...........
idxlon = idxlon+1
print(idxlon)       
print(lon_near,lat_near)
 
print(idxlon)
print(idxlat)
print(x[0,idxlat,idxlon])
print(y[0,idxlat,idxlon])
 
resolucion = x[0,0,1]-x[0,0,2]
print(resolucion)
print(alt.shape)
 
 
#******************************************************************
#           Capturando todas las variables con MFDATATEST
#******************************************************************
 
f = MFDataset("wrfout*00")
time1 = f.variables["Times"][:]             # read time in format byte
temp2 = f.variables['T2'][:]        # read temperature at 2m
v10 = f.variables["V10"][:]                 # read wind velocity component at 10m
u10 = f.variables["U10"][:]                 # read wind velocity component at 10m
 
#********************************************************************************
#                   convert  byte to string
#                   ***********************
strs = ["" for x in range(0,len(Files))]
for i in range(0,len(Files)):
    strs[i] = str(time1[i,:], "utf-8")
print(strs)
 
#********************************************************************************
#               Extract Data T2 at 2m
#               *********************
print((temp2[0,idxlat,idxlon]))
temp2m = np.zeros(len(Files),dtype="f")   # generating space for temp2 of 24 spaces
for i in range(0,len(Files)):
    temp2m[i] = float(temp2[i,idxlat,idxlon]) #saving each temperature by date
 
temp2m = temp2m-273.15           # converter Kelvin degree to celsius degree
print(temp2m)
 
#********************************************************************************
#               Extract Data V10 at 10m
#               ***********************
print((v10[0,idxlat,idxlon]))   
 
v10m = np.zeros(len(Files),dtype="f")    # generating a vector of zeros of 24 spaces
for i in range(0,len(Files)):
    v10m[i] = float(v10[i,idxlat,idxlon]) # saving each component of velocity by date
 
print(v10m)
 
#********************************************************************************
#               Extract Data U10 at 10m
#               ***********************
print((u10[0,idxlat,idxlon]))   
 
u10m = np.zeros(len(Files),dtype="f")    # generating a vector of zeros of 24 spaces
for i in range(0,len(Files)):
    u10m[i] = float(u10[i,idxlat,idxlon]) # saving each component of velocity by date
 
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
     
# to convert tetha in positive degrees
for i,tetha_i in enumerate(tetha):
    if tetha_i<0.0:
        tetha[i] = tetha[i] + 360                 # Positive degrees
print(tetha)
 
print(len(tetha))
 
#********************************************************************************
#               Exporting Data to CSV format
#               ****************************
 
df2 = pd.DataFrame({'Time': strs,
                    'T2s_1s': temp2m,
                    'W10s_1s': R,
                    'Wds_1s': tetha
                    })
 
df2 = df2[['Time', 'T2s_1s','W10s_1s','Wds_1s']]          # set order of columns
 
print(df2)
print(df2.dtypes)
 
# generating date for file.csv
 
 
 
#file_csv_name = "df"+file_sep[0] + ".csv"   # generating the name for csv file
 
print("df_1s.csv")                        # name of the extension csv
df2.to_csv(path_or_buf="df_1s.csv")       # save dataframe dataframe.to_csv()
