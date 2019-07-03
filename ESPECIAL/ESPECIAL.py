# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 17:50:58 2019

@author: Publico
"""
from matplotlib import pyplot as pp
import numpy as np
import cv2 
import lantz
import time
from lantz.ino import INODriver, QuantityFeat, BoolFeat
from Arduino0 import Servo


del(camera)



camera = cv2.VideoCapture(0)  
return_value, image = camera.read()  


#M = cv2.imread('opencv.png')
#  caracterizacion de movimiento del servo

v=[0,1,2,3,4,5,6,7,8,9,10]
v=np.linspace(1400,1500,15)#microseconds
#v=np.linspace(10,0,11) #angulos
v[1]-v[0]




if __name__ == '__main__':
    with Servo.via_packfile('Servo.pack.yaml') as dev:
        dev.angle = 1450 #* ureg.degree   #ANGULO DE FINAL


if __name__ == '__main__':
    with Servo.via_packfile('Servo.pack.yaml') as dev:
        for i in v:
#        for i in range(400,11):
            print(i)
            dev.angle = i #* ureg.degree      #ANGULO DE COMIENZO
            time.sleep(30)


for i in v:          
    if __name__ == '__main__':
        with Servo.via_packfile('Servo.pack.yaml') as dev:           
            #            dev.angle = 0
#            time.sleep(20)
            print('inicio',i)
            dev.angle = i #* ureg.degree      #ANGULO DE COMIENZO
    

for a in range(400,700) :
    print(a)
  
if __name__ == '__main__':
    with Servo.via_packfile('Servo.pack.yaml') as dev:
        dev.angle = 1300 #* ureg.degree   #ANGULO DE FINAL

angs=np.linspace(1400,1500,15)  
p=0
results=[]

image=0
if __name__ == '__main__':
    with Servo.via_packfile('Servo.pack.yaml') as dev:
        for i in angs:
            dev.angle =i #* ureg.degree
            time.sleep(15)
            return_value, image = camera.read()
            cv2.imwrite('imagenes/foto{}.png'.format(i),image)
            time.sleep(5)
            prom = np.mean(image)    
            results.append([i,prom])
            print(p)
            p=p+1
        
results = np.array(results)

imax = np.max(results[:,1])

for i in range(len(results)):
    if results[i, 1] == imax:
        angmax = results[i, 0]
        
if __name__ == '__main__':
    with Servo.via_packfile('Servo.pack.yaml') as dev:
        dev.angle = angmax #* ureg.degree
    
np.savetxt('results.txt', results)
del(camera)
