# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 05:45:23 2019

@author: KBZ
"""


from scipy.optimize import curve_fit

import numpy as np
import scipy as sp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import cv2
print (cv2.__version__)

foto=cv2.imread('foto.png')

foto=np.array(foto)
fotoPROM=np.sum(foto,axis=2)/3


#plt.figure()
#plt.imshow(fotoPROM)
#plt.colorbar()
#plt.show()


lim=np.mean(fotoPROM) #Umbral de intensidad para binarizado

val,binary=cv2.threshold(fotoPROM,lim,255,cv2.THRESH_BINARY)

#plt.figure(1)    
#plt.imshow(binary)

y,x=np.nonzero(binary) #posiciones de los puntos iluminados
y=480-y #redefinición de origen

#plt.figure(2)    
#plt.plot(x,y,'.')
#plt.xlim(0,640)
#plt.ylim(0,480)


def func(x, m, x0, y0): #funcion lineal para cuadrados minimos
    return m*(x-x0)+y0

params,covar=curve_fit(func,x,y,p0=(0.3,0,200)) #cuadrados minimos


xx=np.linspace(0,639,640)
fvals=func(xx,params[0],params[1],params[2]) #calculo la recta de mejor ajuste


fvals=fvals.astype(int) #redondeo valores


plt.figure(1)    
plt.plot(x,y,'.')
plt.plot(xx,fvals,'.')
plt.xlim(0,640)
plt.ylim(0,480)


fvals2=480-fvals #revierto el origen donde estaba...las matrices se indizan de arriba hacia abajo y de izq a der
intens=[]
j=0
for i in fvals2:
    intens.append(fotoPROM[i,j])
    j=j+1
    
intens=np.array(intens)  #vector de intensidades de cada punto sobre la recta de mejor ajuste

plt.figure()
plt.plot(intens,'-')


#fig, axs = plt.subplots(2) #grafico lo calculado
plt.figure()
gs = gridspec.GridSpec(2,1, height_ratios=[2/3,1/3])
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.imshow(fotoPROM)
ax1.plot(xx,fvals2,'r.')
ax2.plot(intens,'-')
ax2.set_xlabel('componente x de distancia sobre recta')

#y a esto pueden hacerseles los ajustes del modelo de difracción (seno cardinal)