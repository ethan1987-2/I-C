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

foto=cv2.imread('foto.png')
foto0=foto[:,:,0]
foto1=foto[:,:,1]
foto2=foto[:,:,2]

foto=np.array(foto)
fotoPROM=np.sum(foto,axis=2)/3

fotoMax=foto[:,:,2]
fotoMin=foto[:,:,0]


for i in range(3):
    plt.figure()
    plt.imshow(foto[:,:,i]);
    plt.title(i)
    plt.colorbar()
    plt.show()


plt.figure()
plt.imshow(fotoPROM)
plt.colorbar()
plt.show()


lim=np.mean(fotoPROM)

val,binary=cv2.threshold(fotoPROM,lim,255,cv2.THRESH_BINARY)

plt.figure()    
plt.imshow(binary)

#y,x=np.nonzero(fotoPROM)
y,x=np.nonzero(binary)
y=480-y

plt.figure(1)    
plt.plot(x,y,'.')
plt.xlim(0,640)
plt.ylim(0,480)


def func(x, m, x0, y0):
    return m*(x-x0)+y0

params,covar=curve_fit(func,x,y,p0=(0.3,0,200))


xx=np.linspace(0,639,640)
fvals=func(xx,params[0],params[1],params[2])
#fvals=fvals[0:480]
plt.figure(1)    
plt.plot(xx,fvals,'.')


fvals=np.around(fvals)
fvals=fvals.astype(int)


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
    
intens=np.array(intens)  

plt.figure()
plt.plot(intens,'-')


fig, axs = plt.subplots(2)
axs[0].imshow(fotoPROM)
axs[0].plot(xx,fvals2,'r.')
axs[1].plot(intens,'-')

#ANALISIS POR VARIANCIA (PROPUESTA por HERNAN GRECCO)

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
foto=cv2.imread('foto.png')


plt.figure(1)    
plt.plot(x,y,'.')
plt.xlim(0,640)
plt.ylim(0,480)

def func(x, m, x0, y0):
    return m*(x-x0)+y0

params,covar=curve_fit(func,x,y,p0=(0.3,0,200))

dire=[5,func(5,params[0],params[1],params[2])-func(0,params[0],params[1],params[2])]

rads=np.arctan(-dire[1]/dire[0])

[rows,cols]=fotoPROM.shape

M = cv2.getRotationMatrix2D((cols/2,rows/2),rads*180/np.pi,1)
dst = cv2.warpAffine(fotoPROM,M,(cols,rows))

plt.imshow(dst) #Ahora la figura esta al derecho y se puede aplicar el criterio de la primer version


proyY=np.sum(dst,axis=0)
proyX=np.sum(dst,axis=1)

plt.plot(proyY)
plt.plot(proyX)

rxy=np.var(proyX)/np.var(proyY) #la razon de varianzas de las distribuciones de intensidad en x respecto de y


