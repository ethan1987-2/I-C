# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 03:53:58 2019

@author: KBZ
"""

from matplotlib import pyplot as pp
import numpy as np
import cv2 
import lantz
import time
from lantz.ino import INODriver, QuantityFeat, BoolFeat
from Arduino0 import Servo

#input del usuario
musi=input('posic inicial del servo:')
v=eval(input('vector de barrido en microseconds del ciclo PWM del servo (puede usarse np.linspace por ej):'))

musi=float(musi)#posic inic...conviene trabajar en rangos cercanos a los 1500 microseconds

camera = cv2.VideoCapture(0)  

if __name__ == '__main__':
    with Servo.via_packfile('Servo.pack.yaml') as dev:
        dev.angle = musi # Posicionamiento inicial 


poss=[] #repositorio

    
if __name__ == '__main__':
    with Servo.via_packfile('Servo.pack.yaml') as dev:
        for i in v:
            print('posicion ',i)
            dev.angle = i #orden de posicionamiento al servo/arduino
            time.sleep(20) #espera de correccion a la posicion
            return_value, img = camera.read() #tomo la foto
            nombre='imagenes/foto{}.png'.format(np.around(i,decimals=2))
            cv2.imwrite(nombre,img) #guardo la foto
            poss.append([i,nombre]) #guardo ubicaciones de cada foto

del(camera) #libero la camara

poss=np.array(poss)

#ANALISIS DE LAS FOTOS

def func(x, m, x0, y0): #funcion lineal para cuadrados minimos
    return m*(x-x0)+y0

ind=0
rs=[] #ratios de varianzas varx/vary

for f in poss[:,1]:
    foto=cv2.imread('imagenes/'+f)
    foto=np.array(foto)
    fotoPROM=np.sum(foto,axis=2)/3#promedio de las matrices RGB
    lim=np.mean(fotoPROM) #promedio absoluto de intensidad
    val,binary=cv2.threshold(fotoPROM,lim,255,cv2.THRESH_BINARY) #binarización de la imagen
    y,x=np.nonzero(binary) #posiciones de las iluminaciones
    y=480-y #redefinicion de origen
    params,covar=curve_fit(func,x,y,p0=(0.3,0,200))# cuadrados minimos para sacar el eje principal de la difraccion , p0 parametros iniciales
    dire=[5,func(5,params[0],params[1],params[2])-func(0,params[0],params[1],params[2])] #vector director del eje principal  del patron
    rads=np.arctan(-dire[1]/dire[0]) #angulo de rotación para enderezar el patron respecto al eje de la camara
    [rows,cols]=binary.shape
    M = cv2.getRotationMatrix2D((cols/2,rows/2),rads*180/np.pi,1) #construyo la matriz de rotación
    dst = cv2.warpAffine(binary,M,(cols,rows)) #enderezo la imagen
    proyY=np.sum(dst,axis=0) #vector de proyeccion de intensidades en eje Y
    if np.sum(proyY)==0: proyY=1 #evito un error de division por 0
    proyX=np.sum(dst,axis=1) #vector de proyeccion de intensidades en eje X
    r=np.var(proyX)/np.var(proyY) #la razon de varianzas de las distribuciones de intensidad en x respecto de y
    rs=rs.append([poss[ind,0],r])
    ind=ind+1

rs=np.array(rs)
iM=np.argmax(rs[:,1])
posicM=rs[:,0][iM]

if __name__ == '__main__':
    with Servo.via_packfile('Servo.pack.yaml') as dev:
        dev.angle = posicM # Posicionamiento final en donde hay difraccion 

