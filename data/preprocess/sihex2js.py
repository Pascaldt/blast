#-*- coding: utf-8 -*-

#import csv
#
def sihex2js():
#    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
#    for row in csv_reader:
#        #print type(row), row
#        #for ce in row:
#        #    print type(ce),ce
#        yield [unicode(cell, 'utf-8') for cell in row]
#
#
    namein = '/Volumes/SharedFolders/Resif/Data/catalogue-SiHex/Artif/Catalogue_SiHex_Mw.lst'
    nameout = '/Volumes/SharedFolders/Resif/blast/html/Catalogue_SiHex_Mw.js'
    
    fin = open(namein,'r')
    fout = open(nameout,'wb')

    fout.write("var catalog = [ // EVID YYY/MM/DD HH:MM:SS.S LAT LON DEPTH AUTEUR TYPE Mw\n")
    for line in fin:
        str = '['+line[4:10]+', "'+line[11:21]+'", "'+line[22:32]+'",'+line[40:52]+','+line[53:63]+','+line[67:74]+',"'+line[74:80]+'","'+line[90:92]+'",'+line[97:-1]+'],\n'
        fout.write(str);
        #print line
        #print str

    fout.write("];")
    fin.close()
    fout.close()

if __name__ == "__main__":
    print "sihex2js inputsihexname outputfilejs"    
    print "  convert sihex sismo catalog (fixed space columns) to js variable" 
    sihex2js()
    print "....Done."
