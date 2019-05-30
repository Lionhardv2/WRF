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
from scipy.stats import norm,rayleigh
#   Verifying whether exits this Directory
print(path.exists("AnaWei"))
if path.exists("AnaWei"):
    rmtree("AnaWei")

# Creating Directory for files.png
path_act=os.getcwd()
os.mkdir("AnaWei", 0o777)

#   Verifying whether exits this Directory
print(path.exists("TablasEs"))
if path.exists("TablasEs"):
    rmtree("TablasEs")

# Creating Directory for files.png
path_act=os.getcwd()
os.mkdir("TablasEs", 0o777)

#   Verifying whether exits this Directory
print(path.exists("Stat"))
if path.exists("Stat"):
    rmtree("Stat")

# Creating Directory for files.png
path_act=os.getcwd()
os.mkdir("Stat", 0o777)

Anios = [2015, 2016, 2017, 2018]
indice = 0
fechasM = ["" for x in range(0,36)]
CorrM = np.zeros(36)
corrW = np.zeros(36)
WeibForm = np.zeros(36)
WeibEscal = np.zeros(36)
c = np.zeros(36)
d = np.zeros(36)
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
        # Capturando Parametros de Rayleigh
        param = rayleigh.fit(dfaux["Viento - Velocidad (m/s)"]) # distribution fitting
        pdf_fitted = rayleigh.pdf(x,loc=param[0],scale=param[1])
        plt.plot(x, weib(x,escala,forma)*scale,'-b', label = 'Weibull')
        plt.plot(x,pdf_fitted*scale,'-r', label = 'Rayleigh')    # incorporando RAyleigh
        plt.xlabel("Vel. Viento [m/s]")
        plt.ylabel("Distribucion de frecuencia")
        plt.title("Distribucion de Weibull")
        plt.legend(loc = 'upper right')
        # j = mes
        # i = anio
        #******************************************************************
        #			Generacion de Tablas de Frecuencia , PDF, y CDF
        #******************************************************************
        histo, binEdges = np.histogram(dfaux['Viento - Velocidad (m/s)'],bins=range(0,int(dfaux["Viento - Velocidad (m/s)"].max()+2)))
        plt.text(0.2,max(histo)-10,r"$forma =$"+"{0:.4f}".format(forma),fontsize = 8)
        plt.text(0.2,max(histo)-50,r"$escala =$"+"{0:.4f}".format(escala),fontsize =8)
        print(histo)
        print(binEdges)
        probObs = histo/sum(histo)
        print(probObs)
        probWeib = weib(ab[1:],escala,forma)*scale/sum(weib(ab[1:],escala,forma)*scale)
        print(probWeib)
        probAcWeib = np.cumsum(probWeib)
        print(probAcWeib)
        probAcReal = np.cumsum(probObs)
        # Añadiendo la distribucion de Rayleigh
        pdf_fitted = rayleigh.pdf(ab[1:],loc=param[0],scale=param[1])
        probRay = pdf_fitted*scale/sum(pdf_fitted*scale)
        print(probRay)
        probAcRay = np.cumsum(probRay)
        print(probAcRay)
        # Generacion del intervalo de velocidades
        Intervalo = ["0-1","1-2", "2-3", "3-4", "4-5", "5-6","6-7", "7-8", "8-9", "9-10", 
                     "10-11","11-12", "12-13", "13-14", "14-15", "15-16","16-17", "17-18",
                     "18-19", "19-20", "20-21",'21-22','22-23']
                     #'Intervalo de Velocidades': Intervalo[:len(probObs)],
        print('intervalo es :',len(Intervalo))
        plt.subplot(212)
        r, p = stats.pearsonr(probAcReal,probAcWeib)
        rR, pR = stats.pearsonr(probAcReal,probAcWeib)
        rms = sqrt(mean_squared_error(probAcReal, probAcWeib))
        StatData = { 'Intervalo V [m/s]': Intervalo[:len(probObs)],
                'Real': probObs,
                'Acum Real': probAcReal,
                'Weibull': probWeib,
                'Acum Weibull': probAcWeib,
                'Rayleigh': probRay,
                'Acum Rayleigh': probAcRay
                }

        dfstat = pd.DataFrame(StatData,columns= ['Intervalo V [m/s]','Real', 'Acum Real','Weibull', 'Acum Weibull','Rayleigh', 'Acum Rayleigh'])
        #print (dfstat)
        print("r = ",r)
        sns.regplot(x="Acum Real", y="Acum Weibull", data=dfstat)
        plt.text(0.2,0.9,r"$r^2 =$"+"{0:.4f}".format(r),fontsize = 7)
        plt.text(0.2,0.7,r"$RMSE =$"+"{0:.4f}".format(rms),fontsize = 7)
        #plt.savefig("AnaWei/WeibCorr"+str(j)+str(i)+".png",dpi = 300)
        #dfstat.to_csv(path_or_buf = "Stat/Stat"+str(j)+str(i) +".csv")
        plt.close()
        
        # Lista Por Fechas Datos 

        print(dfaux.iloc[1,-1])
        #print(dfaux[0,1])
        # Lista Por coeficiente de correlacion
        corrW[indice] = r
        CorrM[indice] = rR
        print(CorrM[indice])
        fechasM[indice] =str(dfaux.iloc[1,-1])  
        #print('fechaa: ',fechasM[indice])
        a,b,c[indice],d[indice],e,f = stats.describe(dfaux['Viento - Velocidad (m/s)'])
        #print(stats.describe(dfaux['Viento - Velocidad (m/s)']))
        # Guardar Parametros de weibull
        WeibForm[indice] = forma
        WeibEscal[indice] = escala
        indice = indice +1 

#******************************************************************
#   Valores de Estadisticos de Viento a Diferentes meses
#******************************************************************
print(CorrM)
print(fechasM)
print(c)
print(d)
print(WeibEscal)
print(WeibForm)
print(corrW)
StatData = {    'Fecha': fechasM,
                'V mean': c,
                'V std': d,
                'c': WeibForm,
                'k': WeibEscal,
                'RWeibull': corrW,
                'RRayleigh': CorrM
                }
dfstat = pd.DataFrame(StatData,columns= ['Fecha','V mean', 'V std','c', 'k','RWeibull', 'RRayleigh'])
print(dfstat.head())
dfstat.to_csv(path_or_buf = "TablasEs/StatResumen.csv")