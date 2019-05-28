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
        mask = dfvar.Fecha.dt.month == j
        dfaux = dfvar.loc[mask]
        analysis = weibull.Analysis(dfaux["Viento - Velocidad (m/s)"], unit = "m/s")
        analysis.fit(method='mle')
        # Capturando los parametros de weibull
        forma = analysis.stats[3]
        escala = analysis.stats[6]
        count, bins, ignored = plt.hist(dfaux["Viento - Velocidad (m/s)"],23)
        #print(max(dfaux["Viento - Velocidad (m/s)"]))
        x = np.linspace(min(dfaux["Viento - Velocidad (m/s)"]),max(dfaux["Viento - Velocidad (m/s)"]),sum(count))
        scale = count.max()/weib(x,escala ,forma).max()
        #print(weib(x,escala,forma)*scale)
        plt.plot(x, weib(x,escala,forma)*scale)
        # j = mes
        # i = anio
        plt.savefig("AnaWei/Weibpdf"+str(j)+str(i)+".png")
        plt.close()
        #plt.show()
        #******************************************************************
        #					Analisis de corelacion 
        #******************************************************************
        #Sorting the data according to stress values and re-indexing
        dfaux = dfaux.sort_values(by='Viento - Velocidad (m/s)')
        dfaux = dfaux.reset_index(drop=True)
        dfaux['Proba'] = (dfaux.index - dfaux.index[0]+1) / (len((dfaux.index))+1)
        #print(dfaux)
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
        r, p = stats.pearsonr(y,w)
        print(y.shape)
        print(w.shape)
        print("coeficiente de correlacion: ",r)
        rms = sqrt(mean_squared_error(y, w))
        print("RMSE :", rms)
        plt.grid()
        plt.ylabel('log(-log(1 - Probability of fracture))')
        plt.title("Weibull Analysis of experiment data")
        plt.text(0,1,r"$r^2 =$"+"{0:.4f}".format(r))
        plt.text(0,2,r"$RMSE =$"+"{0:.4f}".format(rms))
        plt.savefig("AnaWei/WeibCorr"+str(j)+str(i)+".png")
        plt.close()
        #plt.show()
