import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import weibull
from scipy import stats
from sklearn.metrics import mean_squared_error
from math import sqrt
from glob import glob           # to look for files.nc
import os
from shutil import rmtree       # to remove a Directory that contain files
import os.path as path          # to verify whether exits a Directory
import seaborn as sns 
#   Verifying whether exits this Directory
print(path.exists("AnaWei"))
if path.exists("AnaWei"):
    rmtree("AnaWei")

# Creating Directory for files.png
path_act=os.getcwd()
os.mkdir("AnaWei", 0o777)

Anios = [2015, 2016, 2017, 2018]

Archivo = 'Qollpana150914-270818.csv'
df = pd.read_csv(Archivo, index_col= False)
df["Fecha"] = pd.to_datetime(df["Fecha"])
# filtrando informacion por anio
def weib(x,n,a):
    return (a / n) * (x / n)**(a - 1) * np.exp(-(x / n)**a)
def weibull_inv(p):
    return np.log(-np.log(1.0-p))

for i in Anios:
    print(i)
    mask = df.Fecha.dt.year == i
    dfvar = df.loc[mask]

    aa =dfvar.Fecha.dt.month
    mes = range(min(aa), max(aa)+1)
    for j in mes:
        print(j)
        plt.subplots_adjust(hspace=0.8)
        plt.subplot(211)
        mask = dfvar.Fecha.dt.month == j
        dfaux = dfvar.loc[mask]
        analysis = weibull.Analysis(dfaux["Viento - Velocidad (m/s)"], unit = "m/s")
        analysis.fit(method='mle')
        # Capturando los parametros de weibull
        forma = analysis.stats[3]
        escala = analysis.stats[6]
        count, bins, ignored = plt.hist(dfaux["Viento - Velocidad (m/s)"],bins=range(0,int(dfaux["Viento - Velocidad (m/s)"].max()+2)))
       
        ab = np.arange(0,int(dfaux["Viento - Velocidad (m/s)"].max()+2))
        x = np.linspace(min(dfaux["Viento - Velocidad (m/s)"]),max(dfaux["Viento - Velocidad (m/s)"]),sum(count))
        scale = count.max()/weib(x,escala ,forma).max()
        #print(weib(x,escala,forma)*scale)
        plt.plot(x, weib(x,escala,forma)*scale)
        plt.xlabel("Vel. Viento [m/s]")
        plt.ylabel("Distribucion de frecuencia")
        plt.title("Distribucion de Weibull")
        # j = mes
        # i = anio
        #******************************************************************
        #			Generacion de Tablas de Frecuencia , PDF, y CDF
        #******************************************************************
        histo, binEdges = np.histogram(dfaux['Viento - Velocidad (m/s)'],bins=range(0,int(dfaux["Viento - Velocidad (m/s)"].max()+2)))
        print(histo)
        print(binEdges)
        probObs = histo/sum(histo)
        print(probObs)
        probWeib = ab[1:]/sum(ab[1:])
        print(probWeib)
        probAcWeib = np.cumsum(probWeib)
        print(probAcWeib)
        probAcReal = np.cumsum(probObs)
        plt.subplot(212)
        r, p = stats.pearsonr(probAcReal,probAcWeib)
        rms = sqrt(mean_squared_error(probAcReal, probAcWeib))
        StatData = {'Real': probObs,
                'Acum Real': probAcReal,
                'Weibull': probWeib,
                'Acum Weibull': probAcWeib
                }

        dfstat = pd.DataFrame(StatData,columns= ['Real', 'Acum Real','Weibull', 'Acum Weibull'])
        print (dfstat)
        print("r = ",r)
        sns.regplot(x="Acum Real", y="Acum Weibull", data=dfstat)
        plt.text(0.2,0.9,r"$r^2 =$"+"{0:.4f}".format(r),fontsize = 7)
        plt.text(0.2,0.7,r"$RMSE =$"+"{0:.4f}".format(rms),fontsize = 7)
        plt.savefig("AnaWei/WeibCorr"+str(j)+str(i)+".png")
        plt.close()

