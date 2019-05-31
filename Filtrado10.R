#******************************************************
# Version 2.0 Filtrado de Datos Observados cada 10 min
#******************************************************

# Declarando las librerias a utilizar
# -----------------------------------
library(stats)
library(dplyr)

# Capturando los datos en bruto
# -----------------------------
Datos_CSV <- "/home/opti3040a/Dropbox/CMSN/01WRF_Project/01_QMet/20150919-20180828.csv"         # Datos Observados Qollpana
df <- read.csv(file=Datos_CSV)
