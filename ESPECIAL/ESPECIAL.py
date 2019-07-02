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
v=np.linspace(400,600,10)


if __name__ == '__main__':
    with Servo.via_packfile('Servo.pack.yaml') as dev:
        for i in v:
#        for i in range(400,11):
            print('inicio',i)
            dev.angle = i #* ureg.degree      #ANGULO DE COMIENZO
            time.sleep(20)
            print('fin',i)


for a in range(400,700) :
    print(a)
  
if __name__ == '__main__':
    with Servo.via_packfile('Servo.pack.yaml') as dev:
        dev.angle = 400 #* ureg.degree   #ANGULO DE FINAL

angs=np.linspace(500,700,50)  
p=0
results=[]



if __name__ == '__main__':
    with Servo.via_packfile('Servo.pack.yaml') as dev:
        for i in angs:
            dev.angle =i #* ureg.degree
            time.sleep(2)
            return_value, image = camera.read()
            cv2.imwrite('imagenes/foto{}.png'.format(i),image)
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
