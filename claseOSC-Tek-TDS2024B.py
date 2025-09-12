# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import os
import pandas as pd
import sys




np.array(range(1, 11))
np.array([3] * 4, dtype="int32")


4*np.array([3], dtype="int32")
type([3])


np.array(range(1, 11))[:5]


os.listdir(r"D:\6,7Li+197Au\analisis TOMAS\16O+197Au elasticos\analisis_SE")
moni_folder= (r"D:\6,7Li+197Au\analisis TOMAS\16O+197Au elasticos\analisis_SE\ejectomas\moni")
moni_folder= (r"D:\6,7Li+197Au\Experimento\2025_06tom\monitores maestro\20250602-6,7Li+197Au\specon-conversion")

for f in os.listdir(moni_folder):
    print(f.endswith('detector1.AS1'))
    print(f[-13:-4])
    ultimo = f

arc=_(moni_folder+'\\'+ultimo)
arc.tell()
arc.seekline(7)

arc.readlines()[7:-1]
.replace('          ',',')
parte=arc.readlines()[7:10]
parte2=arc.readlines()[-7:-1]
parte[1].split()
parte2[2].split()

tabla=pd.read_csv(moni_folder +"\\"+ ultimo, delim_whitespace=True, 
                               header=None, skiprows=4).replace('              ',',').iloc[:, 1]

pd.read_csv(moni_folder+'\\'+ultimo,skiprows=3,sep='\s+',names=['chn','cts'])

pd.read_csv(moni_folder+'\\'+ultimo,skiprows=3,delim_whitespace=True,header=None)



dates = pd.date_range("20130101", periods=6)
 df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))


archivos = [f for f in os.listdir(moni_folder) if (
            f.endswith('detector1.AS1') or f.endswith('detector0.AS1'))]

for archivo in archivos:
            path = os.path.join(moni_folder, archivo)
            moni = pd.read_csv(path, delim_whitespace=True, 
                               header=None, skiprows=3).iloc[:, 1]#TOMAS DICE: al final use lo mismo que el prog original. pero acá tenemos que especificar "skiprows" para que el programa ignore el encabezado de la tabla de datos del espectro monitor, delimiter_whitespace saca separadores de espacio y hace el csv automaticamente, cambiar segun sea el caso
            #moni.name = f'Monitor {archivo[:3]}'  #TOMAS DICE: acá tenemos 2 opciones para dar el nombre del monitor segun sea el caso
            moni.name = f'Monitor {archivo[-13:-4]}'

datos = pd.DataFrame(
            index=['cuentas_el', 'mu', 'sigma', 'cuentas_pulser'])

datos[archivo[:3]] =(1,2,3,4)
datos[archivo[:3]]
datos['run2']=(1,2,3)+(4,)

dates=pd.date_range("20130101", periods=6)
dates
dates[0]
df=pd.DataFrame(np.random.randn(1, 2), index=list("e"), columns=list("AB"))
df
df.loc['f']=[14,4]
