# -*- coding: utf-8 -*-
"""
Extract origin, detecting and non-detecting stations from sc3 xml file

Created on Fri Oct  3 13:57:34 2014

@author: pascal
"""


import xml.etree.ElementTree as ET 
import os

def get_config():
# Get config    
    import ConfigParser
    cfg = ConfigParser.ConfigParser()
    BLAST_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"
    cfg.read(BLAST_DIR+"blast.cfg")    
        
    cfgp=dict()
    cfgp['dir'] = BLAST_DIR
    cfgp['file']=dict((x,BLAST_DIR+y) for x,y in cfg.items('file'))
    cfgp['param']=dict((x,float(y)) for x,y in cfg.items('param'))
    cfgp['database']=dict((x,y) for x,y in cfg.items('database'))
    return cfgp


def inventory(filename):
    # Parse inventory file into a list station lon, lat, start, end.

    inv = []
    #   Open text file orginfo_inventory.csv
    try:
        file_content = open(filename, 'r').read()

    except IOError:
        print "Error parsing ", file 
        return inv

    #   text file parse inventory
    fields = ['networkCode', 'stationCode', 'latitude', 'longitude', 'start', 'end']
    for current_line in file_content.split('\n'):
        if current_line == '':
            continue
        station = dict(zip(fields, current_line.replace('|', ' ').split()))
        station['latitude'] = float(station['latitude'])
        station['longitude'] = float(station['longitude'])
        inv.append(station)

    return inv

def stations(forg,inventory):
    # Combine into detecting/non detecting station list

    # XML parse origin
    tree = ET.parse(forg)
    root = tree.getroot()    

    # Get detecting station
    #   Extract namespace  like {'sc3': 'http://geofon.gfz-potsdam.de/ns/seiscomp3-schema/0.7'}
    uri = root.tag.split('{')[1].split('}')[0]
    namespaces = {'sc3': uri}
    detect=[] 
    for st in root.findall('sc3:EventParameters/sc3:origin/sc3:arrival',namespaces):        
        # Get network and station code from EventParameters/pick/waveformID 
        pickID = st.find('sc3:pickID',namespaces).text
        predicate = 'sc3:EventParameters/sc3:pick[@publicID="'+pickID+'"]/sc3:waveformID'        
        wform = root.find(predicate,namespaces)
        networkCode = wform.get("networkCode")
        stationCode = wform.get("stationCode")
        
        detect.append({'networkCode':networkCode, \
                        'stationCode':stationCode, \
                        'azimuth':float(st.find('sc3:azimuth',namespaces).text), \
                        'distance':float(st.find('sc3:distance',namespaces).text), \
                        'timeResidual':float(st.find('sc3:timeResidual',namespaces).text), \
                       })
 
    # Complete inventory information detect/non
    out = []
    for inv in inventory: # Complete inventory with detecting information  
        out.append(inv)
        out[-1]['detect']=False
        d = [x for x in detect if x["networkCode"]==inv["networkCode"] and x["stationCode"]==inv["stationCode"]]
        if len(d) > 0:
            #print d[0]["stationCode"]
            out[-1]['detect']=True
            out[-1]['azimuth']=d[0]['azimuth']
            out[-1]['distance']=d[0]['distance']
            out[-1]['timeResidual']=d[0]['timeResidual']
            
    # Backwrd remove duplicates like caused by same station changes in history file
    for i in xrange(len(out)-1,-1,-1):
        if any(x["networkCode"] == out[i]["networkCode"] and \
               x["stationCode"] == out[i]["stationCode"] for x in out[0:i]):   
            out.remove(out[i])
            
   
    return out     

def origin(f):
    # Return origin as a dictionary

    # XML parse origin file
    tree = ET.parse(f)
    root = tree.getroot()    

    #   Extract namespace  like {'sc3': 'http://geofon.gfz-potsdam.de/ns/seiscomp3-schema/0.7'}
    uri = root.tag.split('{')[1].split('}')[0]
    namespaces = {'sc3': uri}
    
    #   Make sure one origin exactly (event xml may have several)
    if len(root.findall('sc3:EventParameters/sc3:origin',namespaces))!= 1:
        print 'origin not unique'
        return []
        
    # Build the dictionary
    out = { \
    'idorg':root.find('sc3:EventParameters/sc3:origin',namespaces).get('publicID'), \
    'date':root.find('sc3:EventParameters/sc3:origin/sc3:time/sc3:value',namespaces).text, \
    'lon':float(root.find('sc3:EventParameters/sc3:origin/sc3:longitude/sc3:value',namespaces).text), \
    'lat':float(root.find('sc3:EventParameters/sc3:origin/sc3:latitude/sc3:value',namespaces).text), \
    'lonuncert':root.find('sc3:EventParameters/sc3:origin/sc3:longitude/sc3:uncertainty',namespaces), \
    'latuncert':root.find('sc3:EventParameters/sc3:origin/sc3:latitude/sc3:uncertainty',namespaces), \
    'm': root.find('sc3:EventParameters/sc3:origin/sc3:magnitude/sc3:magnitude/sc3:value',namespaces)}

    # Default values  
    if out['lonuncert'] is not None:
        out['lonuncert'] = float(out['lonuncert'].text)
    else:
        out['lonuncert'] = 0.
         
    if out['latuncert'] is not None:
        out['latuncert'] = float(out['latuncert'].text)
    else:
        out['latuncert'] = 0.

    if out['m'] is not None:
        out['m'] = float(out['m'].text)
    else:
        out['m'] = 0.
            
    # Add local time
    from datetime import datetime
    import pytz    # Timezones for local time
    utc = datetime.strptime(out['date'],"%Y-%m-%dT%H:%M:%S.%fZ") # float Timestamp
    loctime =  utc.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/Paris'))
    out['loctime'] = loctime.strftime("%Y-%m-%d %H:%M:%S")
    
    # Add event ID
    cfg = get_config()
    import cPickle as pickle
    orgp = pickle.load( open(cfg['file']['originp'], "rb" ) ) # pickle file
    out['idev'] = orgp['idev']
    
    return out     
    
###########################################################
## Resif map tool for seiscomp3
############################################################

if __name__ == "__main__":
    f = './orginfo.xml'
    print "Donnees de l'epicentre:"
    org = origin(f)
    print org
    
    f2 = './orginfo_inventory.csv'
    
    ivt = inventory(f2)
    #print ivt

    s = stations(f,ivt)
    
    print "\n Stations de l'epicentre:"
    for qq in s:
        print qq
        
