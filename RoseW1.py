import numpy as np
from windrose import WindAxes
import pandas as pd
from windrose import WindroseAxes
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
# Leer datos de dataframe
Archivo = 'Qollpana150914-270818.csv'
df = pd.read_csv(Archivo, index_col=False)
# print(df.columns)
# Create wind speed and direction 
ws = df['Viento - Velocidad (m/s)']
wd = df['Viento - Direccion (°)']
ax = WindroseAxes.from_ax()
ax.bar(wd,ws, bins= np.arange(0,23), opening = 0.8, edgecolor = 'white')
ax.set_legend()
plt.savefig("WindRose.jpg", dpi=300)
