# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 17:19:25 2014

@author: pascal
"""
import numpy as np


# Fast approximate return 3 closest lonlat points (quarries) of file.      
def closest(lon,lat,file):
    
    
    # print str
    
    # print np.__version__ chck version and path
    # print np.__file__
    deg2rad = np.pi/180    
    
    # Read quarries with labert2 coords
    try:
        list = np.genfromtxt(file, dtype=None, delimiter=';', names=True, usecols = (9, 10))
    except IOError:
        print "File not found: ",file
        return[]
    
    # Array of lonlat (degree)
    #lonq = np.array([float(x[0].replace(',','.')) for x in list]) 
    #latq = np.array([float(x[1].replace(',','.')) for x in list]) 
    
    lonq = np.array([float(x[0]) for x in list]) 
    latq = np.array([float(x[1]) for x in list]) 

    dlon = lonq - lon
    dlat = latq - lat  
    
    dp2 = dlat**2 + dlon**2 * np.cos(lat*deg2rad)
    dp2.sort()
    
    R = 6371 # Earth radius (km)
    return np.sqrt(dp2[0:3])*deg2rad*R
    

#############################################
## Resif return 3 closests quarries from file
#############################################

if __name__ == "__main__":
    lon =  0.3665         # Seism lonlat (degree)
    lat = 43.0591    
    errlon=  8.39             # Kilometers
    errlat= 16.49

    c = closest(lon,lat,'./data/carrieres_roches_massivesll.csv')
    if len(c)>0:
        print 'D (km)   %5.1f \t| %5.1f \t| %5.1f' % (c[0],c[1],c[2])
        s = np.sqrt((errlon**2 + errlat**2)/2.)
        print 'D (sigm) %5.1f \t| %5.1f \t| %5.1f' % (c[0]/s,c[1]/s,c[2]/s)
    
    
