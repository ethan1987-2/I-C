# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 17:23:48 2019

@author: Publico
"""
import cv2
import lantz
import time
from lantz.ino import INODriver, QuantityFeat, BoolFeat
from lantz import ureg
import numpy as np

class Servo(INODriver):       
    angle = QuantityFeat('ANGLE', units='degree',getter=False)
#    dofor= QuantityFear('dofor')
#    amax=QuantityFeat('ANGLEMAX', units='degree',getter=False)
#    amin=QuantityFeat('ANGLEMIN', units='degree',getter=False)
#    
    
    
if __name__ == '__main__':
    with Servo.via_packfile('Servo.pack.yaml') as dev:
        dev.angle = 0 #* ureg.degree

