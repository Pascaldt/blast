#!/usr/bin/python
# Flush binary event to pickle and xml files
def flushev():
    import seiscomp3.DataModel, seiscomp3.IO
    import os, sys
    import bltools
    
    cfg=bltools.get_config() # data pathes

    # Read Origin from stdin
    ar = seiscomp3.IO.BinaryArchive()
    if not ar.open("-"):
        # Hmmm, opening stdin failed
        print 'err input '# + fout
        sys.exit(1)
    
        # Read back into an 'origin' object    
    obj = ar.readObject()    
    ar.close()
        
    org = seiscomp3.DataModel.Origin.Cast(obj)
        # No origin -> error
    if not org:
        sys.exit(1)

    # Export origin from database    
    idorg  = org.publicID()
    # extract associated event name from db   
    try:
        from subprocess import Popen, PIPE
        sql_req = 'seiscomp exec scquery -d '+ cfg['database']['host'] + ' ' + cfg['database']['getevent_query'] + ' ' + idorg
        stdout = Popen(sql_req, shell=True, stdout=PIPE).stdout
        idev = stdout.read().strip()  # strip removes trailing line feeds
    except Exception, exception:
        idev=''

    # extract type of event from db  
    try:
        sql_req2 = 'seiscomp exec scquery -d '+ cfg['database']['host'] + ' ' + cfg['database']['gettype_query'] + ' ' + idorg
        stdout = Popen(sql_req2, shell=True, stdout=PIPE).stdout
        typev = stdout.read().strip()  # strip removes trailing line feeds
    except Exception, exception:
        typev='NULL'

    # Quick write to disc, no waiting for sql requests completion 
    ev = {'idev':idev, 'idorg':idorg, 'lon': org.longitude().value(), 'lat': org.latitude().value(), 'typev': typev}     
    try:
        ev['lonuncert'] = org.longitude().uncertainty()
        ev['latuncert'] = org.latitude().uncertainty()
    except:
        pass

    # write on disc orginfo.p   
    import cPickle as pickle
    forgp = cfg['file']['originp']
    pickle.dump( ev, open( forgp, "wb" ) )
    
    # complete origin: Picks, Amplitudes, Magnitudes, Focal mechanism, formtted output, file out 
    forg = cfg['file']['origin']
    cmd = "seiscomp exec scxmldump -d " + cfg['database']['host'] + " -O " + idorg + " -PAMF -f -o " + forg
    os.system(cmd)  
    
    # Separate export for inventory
    finv = cfg['file']['stations']
    cmd = "seiscomp exec scquery -d "+ cfg['database']['host'] + " " + cfg['database']['getstation_query'] + " > " + finv
    os.system(cmd)  
   
if __name__ == "__main__":
    flushev()
