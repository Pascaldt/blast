#-*- coding: utf-8 -*-

import csv

def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        #print type(row), row
        #for ce in row:
        #    print type(ce),ce
        yield [unicode(cell, 'utf-8') for cell in row]


filename = './data/carrieres_roches_massivesll.csv'
reader = unicode_csv_reader(open(filename),delimiter=';')

next(reader)
out=open('./data/carrieresdecode.js','wb')
out.write('var carrieres = [\n')
n=0
for row in reader:
    #q=next(reader)
    print row
    for cell in row:
        print cell.decode()

    # Sortie fichier formattee
    # Retour chariot ligne n-1, sauf derniere ligne
    if n > 0:
        out.write(',\n')
    
    #  Nom
    out.write('["%s",'%row[0].replace('"','\\"').decode())
    
    #  Adresse
    out.write('"%s",'%row[1].replace('"','\\"').decode())
    
    #  Departement
    out.write('"%s",'%row[2].decode())

    #  Code postal
    out.write('"%s",'%row[3].decode())

    #  Nom Commune
    out.write('"%s",'%row[4].replace('"','\\"').decode())
    
    #  Insee Commune
    out.write('"%s",'%row[5].decode())
    
    # Lambert 2x
    out.write('%s,'%row[6].decode())
    
    # Lambert 2y
    out.write('%s,'%row[7].decode())
    
    # Substance
    out.write('"%s",'%row[8].replace('"','\\"').decode())
    
    # Lon
    lon=row[9]
    out.write('%s,' % lon.decode())
    
    # Lat
    lat=row[10]
    out.write('%s]' % lat.decode())

    n=n+1
#    if n == 777:
#        break
    
out.write('\n];\n')
    
out.close()
reader.close()
