#!/usr/bin/python
import seiscomp3.DataModel, seiscomp3.IO

def bob():
    
    #pdb.set_trace()

    ar = seiscomp3.IO.BinaryArchive()

    # Open standard input
    if not ar.open("-"):
        # Hmmm, opening stdin failed
        return 1

    # Read the object
    obj = ar.readObject()
    ar.close()

    # Try to cast obj to an origin
    org = seiscomp3.DataModel.Origin.Cast(obj)

    # No origin -> error
    if not org:
        return 1

    # Try to print the standard error to stdout
    try: print "%4.2f"%org.quality().standardError()
    # Field not set, return error
    except: return 1

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(bob())
