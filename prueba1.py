import pandas as pd
import numpy as np
from glob import glob           # to look for files.nc
import os
from shutil import rmtree       # to remove a Directory that contain files
import os.path as path          # to verify whether exits a Directory
# Usamos rpy2 para interactuar con R
import rpy2 as ro
#rpy2.robjects.numpy2ri.activate()

months =["00","01","02","03","04","05","06","07","08","09","10","11","12"]
years = ["17","18"]
path_6k = '/home/opti3040a/Dropbox/CMSN/01WRF_Project/05_csvData/Analisis/6km/' 


def ls(expr = '/home/opti3040a/Dropbox/CMSN/01WRF_Project/05_csvData/Analisis/6km/*6k.csv*'):
    return glob(expr)
Archivos6km = ls()
File_name = Archivos6km[0].split("/")
print((Archivos6km[0]))
print(File_name[-1][4:6])   # month
print(File_name[-1][6:8])   # year


file_6k = "df"+"01"+months[4]+years[1]+"6k.csv"

print(file_6k)
df1 = pd.read_csv("df0102181k.csv")      # Reading Dataframe of 1km
df2 = pd.read_csv("df0102181k.csv")      # Reading Dataframe of 2km
df2.columns = ["Time","T2o","T2s_2k","W10o","W10s_2k","Wdo","Wds_2k"]
df6 = pd.read_csv("df0102181k.csv")      # Reading Dataframe of 6km

df_com = df1.merge(df2,on= ["Time","T2o","W10o","Wdo"])
#print(df_com.head())
m="07"
if m==months[7]:
    #print("Reset month")
    m="00"
#print(months[7])
#print(m)

#******************************************************************
#					Interaction with R
#******************************************************************


