import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import weibull
from scipy import stats
from sklearn.metrics import mean_squared_error
from math import sqrt


Anios = [2015, 2016, 2017, 2018]

Archivo = 'Qollpana150914-270818.csv'
df = pd.read_csv(Archivo, index_col= False)
df["Fecha"] = pd.to_datetime(df["Fecha"])
# filtrando informacion por anio
def weib(x,n,a):
    return (a / n) * (x / n)**(a - 1) * np.exp(-(x / n)**a)
def weibull_inv(p):
    return np.log(-np.log(1.0-p))

mask = df.Fecha.dt.year == Anios[0]
df15 = df.loc[mask]
mask = df.Fecha.dt.year == Anios[1]
df16 = df.loc[mask]
mask = df.Fecha.dt.year == Anios[2]
df17 = df.loc[mask]
mask = df.Fecha.dt.year == Anios[3]
df18 = df.loc[mask]
mes = range(1,13)

mask = df15.Fecha.dt.month == 10
dfaux = df15.loc[mask]
analysis = weibull.Analysis(dfaux["Viento - Velocidad (m/s)"], unit = "m/")
analysis.fit(method='mle')
# Capturando los parametros de weibull
forma = analysis.stats[3]
escala = analysis.stats[6]
count, bins, ignored = plt.hist(dfaux["Viento - Velocidad (m/s)"],23)
print(max(dfaux["Viento - Velocidad (m/s)"]))
x = np.linspace(min(dfaux["Viento - Velocidad (m/s)"]),max(dfaux["Viento - Velocidad (m/s)"]),sum(count))
scale = count.max()/weib(x,escala ,forma).max()
print(weib(x,escala,forma)*scale)
plt.plot(x, weib(x,escala,forma)*scale)
#plt.savefig("Weibpdf"+mes+Anios+".png")
plt.show()
#******************************************************************
#					Analisis de corelacion 
#******************************************************************
#Sorting the data according to stress values and re-indexing
dfaux = dfaux.sort_values(by='Viento - Velocidad (m/s)')
dfaux = dfaux.reset_index(drop=True)
dfaux['Proba'] = (dfaux.index - dfaux.index[0]+1) / (len((dfaux.index))+1)
print(dfaux)
dfaux['Weibull'] = weibull_inv(dfaux['Proba'])
w = dfaux['Weibull']
lnsw = np.log(dfaux['Viento - Velocidad (m/s)'])
m, lnsm0, *t = stats.linregress(lnsw,w)
sigma0 = np.exp(- lnsm0 / m)
print('m=', m)
print('sigma0=',sigma0)
plt.figure()
plt.plot(lnsw,w)
plt.plot(lnsw,w,'*')
x = lnsw
y = (lambda x : m * x + lnsm0)(x)
plt.plot(x, y)
plt.plot()
plt.grid()
plt.ylabel('log(-log(1 - Probability of fracture))')
plt.title("Weibull Analysis of experiment data")
#plt.savefig("WeibCorr"+mes+str(Anios)+".png")
plt.show()
r, p = stats.pearsonr(y,w)
print(y.shape)
print(w.shape)
print("coeficiente de correla10cion: ",r)
rms = sqrt(mean_squared_error(y, w))
print("RMSE :", rms)
