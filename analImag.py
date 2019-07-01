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

