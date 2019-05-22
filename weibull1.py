#******************************************************************
#					Distribucion Weibull
#******************************************************************
import weibull 
import pandas as pd
import numpy as np

#******************************************************************
#					Datos observados
#******************************************************************
archivo = "20150919-20180828.csv"
#archivo = '/home/opti3040a/Dropbox/CMSN/01WRF_Project/01_QMet/2017_2018Q_UTC.csv'
df = pd.read_csv(archivo,  sep=';')
print(df.head())
df.info()
#******************************************************************
#					Filtrando los datos
#******************************************************************
# Eliminando los datos nulos
df.replace("*", np.nan, inplace = True)
print(df.head())
missing_data = df.isnull()
for column in missing_data.columns.values.tolist():
    print(column)
    print(missing_data[column].value_counts())
    print(" ")
print(df.dtypes)