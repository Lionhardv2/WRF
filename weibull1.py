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
#******************************************************************
#		Reemplazando los datos faltantes por el promedio 
#******************************************************************
column = "Viento - Velocidad (m/s)"
print("Datos sin reemplazar")
print(missing_data[column].value_counts())
# Calculando el promedio de la columna
avg = df[column].astype("float").mean(axis=0)
# Reemplazando los datos nan por el promedio
df[column].replace(np.nan,avg, inplace = True)
print("Reemplazando los datos nulos")
missing_data = df.isnull()
print(missing_data[column].value_counts())
#******************************************************************
#			corrigiendo el tipo de dato
#******************************************************************
print(df[column].dtype)
# cambiando el dato a tipo flotante
df[column] = df[column].astype("float")
print(df[column].dtype)
print(df[column].head())
