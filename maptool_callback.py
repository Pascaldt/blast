#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Launch maptool webbrowser 

Created on Thu Jun 19 16:08:42 2014

@author: pascal
"""
import os
import xmlev  

# Pathes 
dirxml  = os.path.dirname(os.path.realpath(__file__)) + "/"
dirhtml = os.path.dirname(os.path.realpath(__file__)) + "/html/"

forg = dirxml + 'orginfo.xml'
finv = dirxml + 'orginfo_inventory.xml'

import maptool
# Load origin
origin = xmlev.origin(forg)

# Load inventory    
inventory = xmlev.inventory(finv)

# Load stations    
stations = xmlev.stations(forg,inventory) # trigged and untrigged stations

# Store javascript arrays origin.js, stations.js, carrieres.js   
maptool.maptool(origin, stations)

# Display the map
import webbrowser
webbrowser.open(dirhtml+'maptool.html',new=0, autoraise=True)


