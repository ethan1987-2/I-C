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
    angle = QuantityFeat('ANGLE', units='degree', getter=False)




