import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import weibull
from scipy import stats
from sklearn.metrics import mean_squared_error
from math import sqrt
import seaborn as sns; sns.set(color_codes=True)
from scipy.stats import norm,rayleigh
Anios = [2015, 2016, 2017, 2018]

Archivo = 'Qollpana150914-270818.csv'
df = pd.read_csv(Archivo, index_col= False)
df["Fecha"] = pd.to_datetime(df["Fecha"])
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
mes = range(1,13)
#plt.subplots_adjust(hspace=0.8)
mask = df17.Fecha.dt.month == 4
dfaux = df17.loc[mask]
analysis = weibull.Analysis(dfaux["Viento - Velocidad (m/s)"], unit = "m/")
analysis.fit(method='mle')
# Capturando los parametros de weibull
forma = analysis.stats[3]
escala = analysis.stats[6]
#plt.subplot(211)
count, bins, ignored = plt.hist(dfaux["Viento - Velocidad (m/s)"],bins=range(0,int(dfaux["Viento - Velocidad (m/s)"].max()+2)))
x = np.linspace(min(dfaux["Viento - Velocidad (m/s)"]),max(dfaux["Viento - Velocidad (m/s)"]),sum(count))
# Parametros Rayleigh
# Añadiendo la distribucion de Rayleigh
param = rayleigh.fit(dfaux["Viento - Velocidad (m/s)"]) # distribution fitting
pdf_fitted = rayleigh.pdf(x,loc=param[0],scale=param[1])
scale = count.max()/weib(x,escala ,forma).max()
ab = np.arange(0,int(dfaux["Viento - Velocidad (m/s)"].max()+2))
plt.plot(ab, weib(ab,escala,forma)*scale)
plt.plot(x,pdf_fitted*scale,'*')    # incorporando RAyleigh
plt.xlabel("Vel. Viento [m/s]")
plt.ylabel("Probabilidad")
plt.title("Distribucion de Weibull")
#******************************************************************
#			Generacion de Tablas de Frecuencia , PDF, y CDF
#******************************************************************
histo, binEdges = np.histogram(dfaux['Viento - Velocidad (m/s)'],bins=range(0,int(dfaux["Viento - Velocidad (m/s)"].max()+2)))
print(histo)
print(binEdges)
print(weib(ab[1:],escala,forma)*scale)
probObs = histo/sum(histo)
print(probObs)
probWeib = weib(ab[1:],escala,forma)*scale/sum(weib(ab[1:],escala,forma)*scale)
print(probWeib)
probAcWeib = np.cumsum(probWeib)
print(probAcWeib)
probAcReal = np.cumsum(probObs)
# Añadiendo la distribucion de Rayleigh
param = rayleigh.fit(dfaux["Viento - Velocidad (m/s)"]) # distribution fitting
pdf_fitted = rayleigh.pdf(ab[1:],loc=param[0],scale=param[1])
probRay = pdf_fitted*scale/sum(pdf_fitted*scale)
print(probRay)
probAcRay = np.cumsum(probRay)

plt.show()
plt.close()
r, p = stats.pearsonr(probAcReal,probAcWeib)
rms = sqrt(mean_squared_error(probAcReal, probAcWeib))
StatData = {'Real': probObs,
        'Acum Real': probAcReal,
        'Weibull': probWeib,
        'Acum Weibull': probAcWeib,
        'Rayleigh': probRay,
        'Acum Rayleigh': probAcRay
        }

dfstat = pd.DataFrame(StatData,columns= ['Real', 'Acum Real','Weibull', 'Acum Weibull','Rayleigh', 'Acum Rayleigh'])
print (dfstat)
print("r = ",r)
sns.regplot(x="Acum Real", y="Acum Weibull", data=dfstat)
plt.text(0,0.9,r"$r^2 =$"+"{0:.4f}".format(r))
plt.text(0,0.8,r"$RMSE =$"+"{0:.4f}".format(rms))
plt.hist(dfaux["Viento - Velocidad (m/s)"],bins=range(0,int(dfaux["Viento - Velocidad (m/s)"].max()+2)))
r, p = stats.pearsonr(probAcReal,probAcRay)
print("Rayleigh r = ",r)
plt.show()
plt.close()

#******************************************************************
#					Distribucion de Rayleigh
#******************************************************************
param = rayleigh.fit(dfaux["Viento - Velocidad (m/s)"]) # distribution fitting
pdf_fitted = rayleigh.pdf(x,loc=param[0],scale=param[1])
plt.plot(x,pdf_fitted*scale)
plt.hist(dfaux["Viento - Velocidad (m/s)"],bins=range(0,int(dfaux["Viento - Velocidad (m/s)"].max()+2)))
plt.show()

