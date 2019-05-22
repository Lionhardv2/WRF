library(dplyr)
library(EnvStats)
library(stats)
direccion <-getwd()
setwd("/home/opti3040a/Documentos/WRF")
# Leer los datos CSV
Datos_CSV <- "2017_2018Q_UTC.csv"         # Datos Observados Qollpana
df <- read.csv(file=Datos_CSV,header=TRUE,
               stringsAsFactors=FALSE,sep=",")
head(df)
# Seleccionar el metodo para obtener los parametro de weibull
parametros <- eweibull(df$W10o, method = "mle")
# Graficar las salidas de la distribucion de Weibull
pdfPlot(distribution = "weibull", param.list = list(shape = 1.845, scale= 9.164), curve.fill.col = "cyan",main = "")
cdfPlot(distribution = "weibull", param.list = list(shape = 1.845, scale= 9.164), curve.fill.col = "cyan",main = "")
