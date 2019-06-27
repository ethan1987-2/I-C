# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 16:43:06 2019

@author: Publico
"""
import cv2

camera = cv2.VideoCapture(0)    
for i in range(10):
    return_value, image = camera.read()
    cv2.imwrite('opencv'+str(i)+'.png', image)
del(camera)
