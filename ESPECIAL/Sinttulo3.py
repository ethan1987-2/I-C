# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 17:50:58 2019

@author: Publico
"""

import lantz
import time
from lantz.ino import INODriver, QuantityFeat, BoolFeat

class Aparato(INODriver):       
    tension = QuantityFeat('Tension', units='V', setter=False)

    enable = BoolFeat('ENABLE')


if __name__ == '__main__':
    with Aparato.via_packfile('Aparato.pack.yaml') as dev:
        print('hola')
        for i in range(200):
            print(dev.tension)
            time.sleep(0.1)