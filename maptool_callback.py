#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Launch maptool webbrowser 

Created on Thu Jun 19 16:08:42 2014

@author: pascal
"""
import bltools  

# Pathes 
cfg = bltools.get_config()
forg = cfg['file']['origin']
finv = cfg['file']['stations']
#print forg,'\n',finv

import maptool
# Load origin
origin = bltools.origin(forg)

# Load inventory    
inventory = bltools.inventory(finv)

# Load stations    
stations = bltools.stations(forg,inventory) # trigged and untrigged stations

# Store javascript arrays origin.js, stations.js, carrieres.js 
# Display enritched map  
maptool.maptool(origin, stations)


