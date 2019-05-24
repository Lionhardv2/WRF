#******************************************************************
#		Funcion de Ditribucion de Probabilidades de Weibull
#******************************************************************
import weibull
import pandas as pd
import numpy as np
#******************************************************************
#				Filtrando los Datos por Mes
#******************************************************************
# Capturando los datos filtrados
Anios = [2015, 2016, 2017, 2018]
Archivo = 'Qollpana150914-270818.csv'
df = pd.read_csv(Archivo, index_col= False)
df["Fecha"] = pd.to_datetime(df["Fecha"])
#print(df.head())
# filtrando informacion por anio
mask = df.Fecha.dt.year == Anios[0]
df15 = df.loc[mask]
mask = df.Fecha.dt.year == Anios[1]
df16 = df.loc[mask]
mask = df.Fecha.dt.year == Anios[2]
df17 = df.loc[mask]
mask = df.Fecha.dt.year == Anios[3]
df18 = df.loc[mask]

#******************************************************************
#					Distribucion Weibull
#******************************************************************
# Distribucion de Weibull del anio 2015
# Del mes de septiembre 2015
# Aplicando el filtro para el mes de septiembre
mask = df15.Fecha.dt.month == 11
print(mask)
dfaux = df15.loc[mask]
print(max(df['Viento - Velocidad (m/s)']))
analysis = weibull.Analysis(dfaux["Viento - Velocidad (m/s)"], unit = "m/")
analysis.fit(method='mle')
analysis.probplot(file_name="Comparativa.png")
analysis.pdf(file_name="WeibulPDF.png")
analysis.cdf(file_name="WeibulCDF.png")

mask = df16.Fecha.dt.month == 11
print(mask)
dfaux = df16.loc[mask]
print(max(df15['Viento - Velocidad (m/s)']))
analysis = weibull.Analysis(dfaux["Viento - Velocidad (m/s)"], unit = "m/")
analysis.fit(method='mle')
analysis.probplot(file_name="Comparativa1.png")
analysis.pdf(file_name="WeibulPDF1.png")
analysis.cdf(file_name="WeibulCDF1.png")