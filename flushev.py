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
    # extract associated event name   
    try:
        from subprocess import Popen, PIPE
        stdout = Popen('scquery -d sysop:sysop@localhost/seiscomp3 getevent_mysql ' + idorg, shell=True, stdout=PIPE).stdout
        idev = stdout.read().strip()  # strip removes trailing line feeds
        # tester os.popen('scquery -d etc..').read()
    except:
        idev=''
    
    # Quick write to disc, no waiting for sql requests completion 
    ev = {'idev':idev, 'idorg':idorg, 'lon': org.longitude().value(), 'lat': org.latitude().value()}     
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
    cmd = "seiscomp exec scxmldump -d sysop:sysop@localhost/seiscomp3 -O " + idorg + " -PAMF -f -o " + forg
    os.system(cmd)  
    
    # Separate export for inventory
    finv = cfg['file']['stations']
    cmd = "seiscomp exec scxmldump -d sysop:sysop@localhost/seiscomp3 -I -f -o " + finv
    os.system(cmd)  

   
if __name__ == "__main__":
    flushev()
