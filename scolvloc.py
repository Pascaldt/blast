#!/usr/bin/python
import numpy
import closest

def indic1():
    import bltools  
    cfg=bltools.get_config()
    # Load config 
    fcar = cfg['file']['quarries'] # Local pathes
    forg = cfg['file']['origin']
    ev = bltools.origin(forg)      # xml event 

    # print 3 smallest distances to quarries
    c=closest.closest(float(ev['lon']), float(ev['lat']), fcar) 

    print "-- Resif ---------------------------------------"

    if len(c)>0:   # A value is returned from csv distances to quarries
        print 'D (km)   %5.1f \t| %5.1f \t| %5.1f' % (c[0],c[1],c[2])

    try:
        s = numpy.sqrt((float(ev['lonuncert'])**2 + float(ev['latuncert'])**2)/2.)   
        if s > 0:
            print 'D (sigm) %5.1f \t| %5.1f \t| %5.1f' % (c[0]/s,c[1]/s,c[2]/s)
            
    except:
        pass   
   
    return 0

if __name__ == "__main__":
    import sys
    import flushev

    flushev.flushev()
    sys.exit(indic1())
