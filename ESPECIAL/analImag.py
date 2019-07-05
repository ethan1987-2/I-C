# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 21:00:56 2019

@author: KBZ
"""

from scipy.optimize import curve_fit

import numpy as np
import scipy as sp
from matplotlib import pyplot as plt
import cv2
print (cv2.__version__)


#ANALISIS POR VARIANCIA (PROPUESTA por HERNAN GRECCO)


foto=cv2.imread('foto.png')

foto=np.array(foto)
fotoPROM=np.sum(foto,axis=2)/3



#1er aproximacion simple comparacion de varianza segun ejes de la camara

proyY=np.sum(fotoPROM,axis=0)
proyX=np.sum(fotoPROM,axis=1)

plt.plot(proyY)
plt.plot(proyX)

rxy=np.var(proyX)/np.var(proyY)

#################################################
#2da aproximacion : comparacion de varianza segun ejes de la figura de difraccion (generalizacion para cualquier orientacion de rendija)

            #spot=cv2.imread('spot.png')
            #
            #spot=np.array(spot)
            #spotPROM=np.sum(spot,axis=2)/3
            #
            #lim=np.mean(spotPROM)
            #val,binaryspot=cv2.threshold(spotPROM,lim,255,cv2.THRESH_BINARY)
            #
            #proyX=np.sum(binaryspot,axis=0)/480
            #proyY=np.sum(binaryspot,axis=1)/640
            #
            #j=0
            #v=0
            #for i in proyY:
            #    v=i*j+v
            #    j=j+1
            #    
            #yspot=v/np.sum(proyY)
            #
            #
            #j=0
            #v=0
            #for i in proyX:
            #    v=i*j+v
            #    j=j+1
            #    
            #xspot=v/np.sum(proyX)
            #
            #plt.figure()    
            #plt.imshow(binaryspot)
            #plt.plot(xspot,yspot,'k.')


            #y,x=np.nonzero(binaryspot)
            #y=480-y



        #def func(x, m, x0, y0):
        #    return m*(x-x0)+y0
        #
        #params,covar=curve_fit(func,x,y,p0=(0.3,0,200))




            ##verifico que el centro de masa del spot coincide con el punto del ajuste de cuad min para xCM func(xCM)
            #plt.figure()    
            #plt.plot(x,y,'.')
            #plt.plot(xspot,func(xspot,params[0],params[1],params[2]),'g.')
            #plt.xlim(0,640)
            #plt.ylim(0,480)

#saco la direccion perpendicular al eje del patron
dire=[5,func(xspot+5,params[0],params[1],params[2])-yspot]

        #perp=[dire[1],-dire[0]]
        #
        ##saco la pendiente
        #m=-dire[0]/dire[1]
        #
        #
        #xx=np.linspace(0,639,640)
        #
        #
        ##funcion de la direccion perpendicular
        #eje2=lambda x: m*(x-xspot)+yspot
        #eje2vals=eje2(xx).astype(int)


fvals=func(xx,params[0],params[1],params[2])
fvals=fvals.astype(int)

        #observamos las 2 direcciones y el punto central
        #plt.figure()    
        #plt.imshow(binaryspot)
        #plt.plot(xx,eje2vals,'r-')
        #plt.plot(xx,fvals,'b-')
        #plt.plot(xspot,yspot,'k.')
        #plt.xlim(0,640)
        #plt.ylim(0,480)
        #plt.plot(xspot,func(xspot,params[0],params[1],params[2]),'g.')

#################################################
#VERSION 3 rotacion de la imagen SIN conocer SPOT
foto=cv2.imread('spot.png')

foto=np.array(foto)
fotoPROM=np.sum(foto,axis=2)/3



lim=np.mean(fotoPROM) #Umbral de intensidad para binarizado

val,binary=cv2.threshold(fotoPROM,lim,255,cv2.THRESH_BINARY)

y,x=np.nonzero(binary) #posiciones de los puntos iluminados
y=480-y #redefinición de origen

plt.figure(1)    
plt.plot(x,y,'.')
plt.xlim(0,640)
plt.ylim(0,480)

def func(x, m, x0, y0):
    return m*(x-x0)+y0

params,covar=curve_fit(func,x,y,p0=(0.3,0,200))

dire=[5,func(5,params[0],params[1],params[2])-func(0,params[0],params[1],params[2])]

rads=np.arctan(-dire[1]/dire[0])

[rows,cols]=binary.shape

M = cv2.getRotationMatrix2D((cols/2,rows/2),rads*180/np.pi,1)
M2 = cv2.getRotationMatrix2D((cols/2,rows/2),45,1)
dst = cv2.warpAffine(binary,M2,(cols,rows))

plt.imshow(dst) #Ahora la figura esta al derecho y se puede aplicar el criterio de la primer version


proyY=np.sum(dst,axis=0)
proyX=np.sum(dst,axis=1)

plt.imshow(binary) 
proyY=np.sum(fotoPROM,axis=0)
proyX=np.sum(fotoPROM,axis=1)

plt.plot(proyY)
plt.plot(proyX)

rxy=np.var(proyX)/np.var(proyY) #la razon de varianzas de las distribuciones de intensidad en x respecto de y


