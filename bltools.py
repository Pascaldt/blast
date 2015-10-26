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
    return cfgp


def inventory(file):
    # All stations inventory xml file
    # Parse all records fulfilling Inventory/network/station/longitude,
    # latitude, start or end date.
    # Parse input file 
    try:
        tree = ET.parse(file)
    except IOError:
        print "Error parsing ", file 
        return []
     
    # Extract namespace  like {'sc3': 'http://geofon.gfz-potsdam.de/ns/seiscomp3-schema/0.7'}
    root = tree.getroot()    
    uri = root.tag.split('{')[1].split('}')[0]
    namespaces = {'sc3': uri}     
    
    # Sweep networks
    inv = []
    for nw in root.findall('sc3:Inventory/sc3:network[sc3:station]',namespaces):
        # Sweep stations
        for st in nw.findall('sc3:station',namespaces):
            try: # start-end dates if any
                start = st.find('sc3:start',namespaces).text
            except:
                start=[]

            try:
                end = st.find('sc3:end',namespaces).text
            except:
                end=[]
                
            inv.append({'networkCode':nw.get('code'), 'stationCode':st.get('code'), \
            'longitude':float(st.find('sc3:longitude',namespaces).text), \
            'latitude':float(st.find('sc3:latitude',namespaces).text), \
            'start':start, 'end':end})
            
    return inv

def stations(forg,inventory):
    # list of all detecting/non detecting stations

    # Detecting stations
    tree = ET.parse(forg)
    root = tree.getroot()    

    # Extract namespace  like {'sc3': 'http://geofon.gfz-potsdam.de/ns/seiscomp3-schema/0.7'}
    uri = root.tag.split('{')[1].split('}')[0]
    namespaces = {'sc3': uri}

    # Enritch inventory with detection information from trigged stations in origin.xml
    detect=[] 
    
    #for i,st in inventory:    
    # Extract all stations producing a pick and containing a 'stationCode' attribute
    # pick = [] # Get networkCode, stationCode
    # for st in root.findall('sc3:EventParameters/sc3:pick/sc3:waveformID[@stationCode]',namespaces=namespaces):
    #    pick.append({'networkCode':st.get('networkCode'), 'stationCode':st.get('stationCode'), \
    #    'publicID':st.get('publicID')})
    
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
 
    # Extend inventory with detection informations azimuth, distance and residual time
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
# Returns the ascii values of xml origin

    # Parse input file 
    tree = ET.parse(f)
    root = tree.getroot()    

    # Extract namespace  like {'sc3': 'http://geofon.gfz-potsdam.de/ns/seiscomp3-schema/0.7'}
    uri = root.tag.split('{')[1].split('}')[0]
    namespaces = {'sc3': uri}
    
    # Make sure one origin exactly (event xml may have several)
    if len(root.findall('sc3:EventParameters/sc3:origin',namespaces))!= 1:
        print 'origin not unique'
        return []
        
    # Extract origin infos

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
            
    # Local time attribute
    from datetime import datetime
    import pytz    # Timezones for local time
    utc = datetime.strptime(out['date'],"%Y-%m-%dT%H:%M:%S.%fZ") # float Timestamp
    loctime =  utc.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/Paris'))
    out['loctime'] = loctime.strftime("%Y-%m-%d %H:%M:%S")
    
    # Load event ID
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
    
    f2 = './orginfo_inventory.xml'
    
    ivt = inventory(f2)
    #print ivt

    s = stations(f,ivt)
    
    print "\n Stations de l'epicentre:"
    for qq in s:
        print qq
        
