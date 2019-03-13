#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 18:01:46 2019

@author: wirrbel
"""
path = '/media/wirrbel/a8fece16-8488-4abe-8878-80df6b8a233e/PV_P14/190925_L/'

import os
import numpy 
cells = numpy.loadtxt(os.path.join(path,'xyz.csv'), delimiter = ",")
numpy.save(os.path.join(path,'cells.npy'), cells)

intensities = numpy.loadtxt(os.path.join(path,'intensities.csv'), delimiter = ",")
numpy.save(os.path.join(path,'intensities.npy'),intensities)