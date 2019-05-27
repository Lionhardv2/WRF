import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import weibull
from scipy import stats
import seaborn as sns; sns.set(color_codes=True)
Anios = [2015, 2016, 2017, 2018]
Archivo = 'Qollpana150914-270818.csv'
df = pd.read_csv(Archivo, index_col= False)
df["Fecha"] = pd.to_datetime(df["Fecha"])
#print(df.head())
# filtrando informacion por anio
def weib(x,n,a):
    return (a / n) * (x / n)**(a - 1) * np.exp(-(x / n)**a)

mask = df.Fecha.dt.year == Anios[0]
df15 = df.loc[mask]
mask = df.Fecha.dt.year == Anios[1]
df16 = df.loc[mask]
mask = df.Fecha.dt.year == Anios[2]
df17 = df.loc[mask]
mask = df.Fecha.dt.year == Anios[3]
df18 = df.loc[mask]

mask = df15.Fecha.dt.month == 9
dfaux = df15.loc[mask]
analysis = weibull.Analysis(dfaux["Viento - Velocidad (m/s)"], unit = "m/")
analysis.fit(method='mle')
# Capturando los parametros de weibull
forma = analysis.stats[3]
escala = analysis.stats[6]
count, bins, ignored = plt.hist(dfaux["Viento - Velocidad (m/s)"],23)
#print(sum(count))
#print(dfaux["Viento - Velocidad (m/s)"].shape)
print(max(dfaux["Viento - Velocidad (m/s)"]))
x = np.linspace(min(dfaux["Viento - Velocidad (m/s)"]),max(dfaux["Viento - Velocidad (m/s)"]),sum(count))
scale = count.max()/weib(x,escala ,forma).max()
print(weib(x,escala,forma)*scale)
plt.plot(x, weib(x,escala,forma)*1)
plt.show()
# Ordenando los datos de mayor a menor
#print(bins)
#print(weib(x,escala,forma)*scale)
#print(max(weib(x,escala,forma)*scale))
# Particionando los datos de Viento de weibull en 10 partes
#print(bin_values)
scale = count.max()/weib(bins,escala ,forma).max()
#print(weib(bins,escala,forma)*scale)
print(count)
hist, bin_edges = np.histogram(weib(x,escala,forma)*scale, 23)
print(hist)
print(weib(x,escala,forma)*scale)
distribucion = weib(x,escala,forma)*scale
plt.plot( weib(x,escala,forma)*scale)
mascara1 = weib(x,escala,forma)*scale <=1
mascara2 = (weib(x,escala,forma)*scale) >1
mascara3 = (weib(x,escala,forma)*scale) >2
print(distribucion[mascara1].shape)
print(distribucion[mascara2].shape)
print(distribucion[mascara3].shape)
#r, p = stats.pearsonr(count,hist)
#print("coeficiente de correlacion ",r)
#ax = sns.regplot(x=hist, y=count, color="g")
plt.show()
#print(dfaux["Viento - Velocidad (m/s)"].shape)
