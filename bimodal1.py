from pylab import *
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd
Archivo = 'Qollpana150914-270818.csv'
df = pd.read_csv(Archivo, index_col= False)
df["Fecha"] = pd.to_datetime(df["Fecha"])
# generando la mascara
# for i in range(1,13):
    

mask = df.Fecha.dt.year == 2017
dfaux = df.loc[mask]

data=dfaux["Viento - Velocidad (m/s)"]
y,x,_=hist(data,23,label='data')

x=(x[1:]+x[:-1])/2 # for len(x)==len(y)


def gauss(x,mu,sigma,A):
    return A*exp(-(x-mu)**2/2/sigma**2)

def bimodal(x,mu1,sigma1,A1,mu2,sigma2,A2):
    return gauss(x,mu1,sigma1,A1)+gauss(x,mu2,sigma2,A2)

#expected=(1,.2,250,2,.2,125)
params,cov=curve_fit(bimodal,x,y)
sigma=sqrt(diag(cov))
plot(x,bimodal(x,*params),color='red',lw=3,label='model')
legend()
print(params,'\n',sigma)
plt.savefig("Distribucion Bimodal")
plt.show() 

