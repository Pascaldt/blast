#!/usr/bin/python
# Flush binary event to sc3 xml file

def flushev():
    import seiscomp3.DataModel, seiscomp3.IO
    import os, sys
    
    foutxml = os.path.dirname(os.path.realpath(__file__)) + "/orginfo.xml"
    foutev  = os.path.dirname(os.path.realpath(__file__)) + "/orginfo_ev.txt"
    foutinv = os.path.dirname(os.path.realpath(__file__)) + "/orginfo_inventory.xml"
        
    # Read Origin
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
    # Options Picks, Amplitudes, Magnitudes, Focal mechanism, formtted output, file out 
    cmd = "seiscomp exec scxmldump -d sysop:sysop@localhost/seiscomp3 -O " + idorg + " -PAMF -f -o " + foutxml
    os.system(cmd)  
    
    # Separate export for inventory
    cmd = "seiscomp exec scxmldump -d sysop:sysop@localhost/seiscomp3 -I -f -o " + foutinv
    os.system(cmd)  

    # Export ID of event to file   
    try:
        from subprocess import Popen, PIPE
        stdout = Popen('scquery -d sysop:sysop@localhost/seiscomp3 getevent_mysql ' + idorg, shell=True, stdout=PIPE).stdout
        idev = stdout.read().strip()  # strip removes trailing line feeds
        # tester os.popen('scquery -d etc..').read()
    except:
        idev=''
        #sys.exit(0)
    foutev=open(foutev, 'w')    
    foutev.write(idev)
    foutev.close()    
   
