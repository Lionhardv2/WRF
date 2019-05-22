#******************************************************************
#					Distribucion Weibull
#******************************************************************
import weibull 
import pandas as pd
import numpy as np
#******************************************************************
#					Datos observados
#******************************************************************
archivo = "20150919-20180828.csv"   # direccion del archivo csv
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
#******************************************************************
#			filtrando los datos por fecha
#******************************************************************
df['concatenado'] = df['Date']+ " " + df["Time"]
print(df['concatenado'].head())
df["concatenado"] = pd.to_datetime(df["concatenado"])
print(df["concatenado"].head())
df.rename(columns = {'concatenado':"Fecha"}, inplace = True)
print(df.head(10))
# Filtrando Fecha cada 10 minutos
print(df.Fecha.dt.minute.head(10))
# Generando la mascara de intervalos de 10 minutos
Int_10 = df.Fecha.dt.minute % 10 == 0
print(df.loc[Int_10].reset_index().drop(['Date','Time','index'], axis=1))
df2 = df.loc[Int_10].reset_index().drop(['Date','Time','index'], axis=1)
print(df2.info())
print(df2['Fecha'].head())
#******************************************************************
#		Guardando en un Archivo.csv los datos filtrados
#******************************************************************
df2.to_csv(path_or_buf = "Qollpana150914-270818.csv")
