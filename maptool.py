# -*- coding: utf-8 -*-
"""
Convert origin and stations to Javascript 
Created on Thu Jun 19 16:08:42 2014

@author: pascal
"""
def maptool(origin, stations):
   # Launch map visu and sismicity plots
    import os
    import bltools
    cfg=bltools.get_config()
      
    # Day/Night/Lunch
    try: 
        if isnight(origin["lat"],origin["lon"],origin["date"]):
            origin["yesnight"] = 'Nuit'
        else:
            origin["yesnight"] = 'Jour'
    except:
        origin["yesnight"] = ""
        import traceback
        traceback.print_exc()

    # Lunch time decided from 11:45 to 13:15
    hm = origin["loctime"][11:16]  # ex. 12:04 
    if '11:45' <= hm <= '13:15':
        origin["yesnight"] = 'Lunch'
    
    # Day of the week
    from datetime import datetime
    origin["dayname"]=datetime.strptime(origin["date"],"%Y-%m-%dT%H:%M:%S.%fZ").strftime("%a")

    # Write  origin 
    fname = cfg['file']['jsorigin']
    f = open(fname, 'w')
    f.write("// Event-dependent variables\n")
    f.write('\t\tvar lat = %f \n'%origin["lat"])
    f.write('\t\tvar lng = %f \n'%origin["lon"])
    f.write('\t\tvar date = "%s" \n'%origin["date"])
    f.write('\t\tvar loctime = "%s" \n'%origin["loctime"][11:16])
    f.write('\t\tvar dlat = %f \n'%origin["latuncert"])
    f.write('\t\tvar dlng = %f \n'%origin["lonuncert"])
    f.write('\t\tvar isnight= "%s" \n'%origin["yesnight"]) # Night, Day, Lunch
    f.write('\t\tvar weekday= "%s" \n'%origin["dayname"]) 
    f.write('\t\tvar idev= "%s" \n'%origin["idev"])
    f.write('\t\tvar idorg= "%s" \n'%origin["idorg"])
    f.close()

    # Write javascript inventory array 
    #print origin
    fname = cfg['file']['jsstations']
    g = open(fname, 'w')
    g.write("var stations = [ // networkCode stationCode lon lat detect\n")
    for st in stations:
        if st['detect']:
            values = (st['networkCode'],st['stationCode'],st['longitude'],st['latitude'],\
                  'true',st['azimuth'],st['distance'],st['timeResidual'])
        else:
            values = (st['networkCode'],st['stationCode'],st['longitude'],st['latitude'],\
                  'false',-1.,-1.,-1.)
            
        # write line [netcode stationcode, detectY/N, lon, lat, azim, dist, timeresidual]
        g.write('["%2s","%5s",%10.6f, %10.6f, %6s, %6.2f, %9.4f, %7.4f],\n' % values )
     
    g.write("];\n")
    g.close()
    
    # Write js seismic history 
    import blhistory
    local = blhistory.get_local(origin)
    blhistory.writejs(local)    
    
    # Display the map
    import webbrowser
    webbrowser.open(cfg['file']['htmlmaptool'],new=0, autoraise=True)

    # Plot sismicity historic

    blhistory.plotpolar(origin,local)

    
def isnight(lat,lng,date,altit=20):
# Returns : 1-night, 0-day
#  All dates are UTC. 
#  Example: str=isnight(43.2, 1.5, "2014/06/17 03:46:31")

    import ephem
    from datetime import datetime
    
    # Convert YYYY-MM-DDThh:mm:ss.ssssssZ 
    #      to YYYY-MM-DD hh:mm:ss.ssssss
    date2 = datetime.strptime(date,"%Y-%m-%dT%H:%M:%S.%fZ"). \
              strftime("%Y-%m-%d %H:%M:%S.%f")
    #Make an observer
    fred      = ephem.Observer()

    #PyEphem takes and returns only UTC times. 15:00 is noon in Fredericton
    fred.date = date2        # With format 2014/6/18 03:19:10
    fred.lon  = str(lng)    # string format 
    fred.lat  = str(lat)    
    fred.elev = altit       # has no effect

    #To get U.S. Naval Astronomical Almanac values, use these settings
    fred.pressure= 0
    fred.horizon = '-0:34'

    # Return night-time when next event is a sunrise 
    nextrise=fred.next_rising(ephem.Sun()) #Sunrise
    nextset =fred.next_setting   (ephem.Sun()) #Sunset
    
    # Debug print [lng, lat, nextrise, nextset]
    if nextrise < nextset:
        return 1    # Next event is a rise so we are night
    else:
        return 0
        

###########################################################
## Resif map tool for seiscomp3
############################################################

if __name__ == "__main__":

#    lng =  0.3665         # Degree East
#    lat = 43.0591         
#    date = "2014-03-19 22:13:04.441"
#    dlng=  8.39             # Kilometers
#    dlat= 16.49
    
    import bltools
    origin = bltools.origin('orginfo.xml')     
    inventory = bltools.inventory('orginfo_inventory.xml')    
    stations = bltools.stations('orginfo.xml',inventory)    
    maptool(origin, stations)
    
    
    
    
