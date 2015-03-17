#  !/usr/bin/env python
#-*- coding: utf-8 -*-

#import csv
#

import numpy as np
import bltools
cfg=bltools.get_config()    

def get_local(origin):
    # Read catalog
    cata = np.genfromtxt(cfg['file']['catalog'] \
       , dtype={'names':('id','date','time','lat','lon','depth','auteur','type','Mw')\
       , 'formats':('S11','S22','S33','f4','f4','f4','S8','S5','f4')})    
    # Restrict to 40 km around origin
    radius  = cfg['param']['loc_radius'] # 40. km around origin
    deg2rad = np.pi/180
    r2 = (cata[:]['lat']-origin['lat'])**2 \
        + ((cata[:]['lon']-origin['lon'])*np.cos(origin['lat']*deg2rad))**2 # Square distance to origin
    R = 6371 # Earth radius (km)
    iok = [i for i in range(0,cata.size) if r2[i]< (radius/(R*deg2rad))**2] # Tresh 
    #local = cata[iok]   
    d = np.sqrt(r2[iok])*R*deg2rad
    local= [dict(zip(x.dtype.names,x)) for x  in cata[iok]]
    for i in xrange(len(local)):
        local[i]['dist']=d[i]    
    return local


def writejs(local):
      
    fileout = cfg['file']['jshistory']
    # Write javascript array for maptool
    # -----------------------------------
    fout = open(fileout,'wb')
    fout.write("var locsism = [ // EVID YYY/MM/DD HH:MM:SS.S LAT LON DEPTH AUTEUR TYPE Mw\n")
    for quake in local:
        fout.write('["%8s", "%10s", "%10s", %9.5f,%9.5f,%6.1f, "%6s", "%2s",%5.2f],\n' % (quake['id'], quake['date'], quake['time'], quake['lat'], quake['lon'], quake['depth'], quake['auteur'], quake['type'], quake['Mw'] ));
    fout.write("];")
    fout.close()
    #%%
    
def plotpolar(origin,local):    
    # Prepare figure's data
    # ---------------------

    #%% Compute origin's parameters
    from datetime import datetime
   
    #  Quakes time, normalised in [0,1]*day, and fractional year
    timestamp = [datetime.strptime(x['date'] + 'T' + x['time'],"%Y/%m/%dT%H:%M:%S.%f") for x in local] # datetime structure
    timestamp=[x for x in timestamp] # Set reference timezone to UTC
    timestamp=[x for x in timestamp] # Convert to local time Europe/Paris
    frac_hour = [timestamp[i].time().hour*3600+timestamp[i].time().minute*60+timestamp[i].time().second for i in xrange(len(local))]
    frac_hour = [x / 86400. for x in frac_hour]
    frac_year = [timestamp[i].year + (timestamp[i]-datetime(timestamp[i].year,1,1,0,0,0)).days/365. for i in xrange(len(local))]
    dist = [x['dist'] for x in local]
    
    #  Append origin
    org_timestamp=datetime.strptime(origin['loctime'],"%Y-%m-%d %H:%M:%S")
    org_hour = (org_timestamp.time().hour*3600+org_timestamp.time().minute*60+org_timestamp.time().second)/86400.
    org_year = org_timestamp.year + (org_timestamp-datetime(org_timestamp.year,1,1,0,0,0)).days/365.
    frac_year.append(org_year)
    frac_hour.append(org_hour)
    dist.append(0.)
    
    #  Graphic common frame
    from matplotlib import pyplot as plt
    #tit = " Local History (SiHex) "
    tit=2
    tit2 = "(utc)%s,  (lon)%-8.4f,  (lat)%-8.4f" % (origin['date'],origin['lon'],origin['lat'])
    #tit = 'Local History (SiHex) of ' + origin['date'] + ' (utc) lon ' + str(origin['lon']) + ' lat ' + str(origin['lat'])
    if tit not in plt.get_figlabels():     # Create figure or make current
        fig=plt.figure(num=tit, figsize=(12, 5), facecolor='none') # create
    else:
        fig=plt.figure(tit)                                # activate
        plt.clf()
        plt.cla()

    #plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)    
    def Mwsurf(m):
        if not hasattr(m,'__iter__'): m = [m] # make singleton iterable
        return [20*(max(x,1.5))**2 for x in m]
        
        
    #%%  === Plot 1 : Radial Date ===   
    # Prepare data
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15)    
    fig.suptitle(tit2,weight='bold',y=0.03,verticalalignment = 'bottom')
    theta = 2*np.pi*np.array(frac_hour)
    colors=['r' if x['type'] in ('ke','se','ls') else 'b' for x in local] # red for natural, blue otherwise
    area = Mwsurf([x['Mw'] for x in local])
    aref = Mwsurf([1.5,2,2.5]) # Further legend of plot
    areaorg = Mwsurf(origin['m'])
    
    # Make axes
    ax = plt.subplot(121, polar=True)        # Polar view
    ax.set_theta_zero_location("N")          # Clockwise origin up
    ax.set_theta_direction(-1)   
    #plt.xlabel('Date radius', fontsize=12)
    
    inner=[3000-x for x in frac_year]         # Substitute radial labels for descending years
                                             # leaving inner disc empty  
    plt.scatter(theta, inner,s=area,c=colors,alpha=.5,edgecolors='k',linewidth=1,zorder=2) # Plot catalog
    plt.scatter(theta[-1], inner[-1],s=areaorg,facecolors='w',linewidth=4,edgecolors='r',zorder=3) # Overplot origin

    #  Time angular axis
    labelsy =  ['Time\n 0h', '','2h','','4h','','6h','','8h','','10h','','12h','','14h','','16h','','18h','','20h','','22h',''] # Subtitude labels
    spoke_angles=[0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 240, 255, 270, 285, 300, 315, 330, 345]
    (g_lines, g_labels)  = ax.set_thetagrids(spoke_angles, labelsy,weight='bold')
    #  Year radial axis
    innerrat = .3                            # let 30% empty center
    infbound = max(inner) - (max(inner)-min(inner))/(1-innerrat)
    #   convert labels of internal scale to ascii years
    ax.set_ylim(infbound,max(inner)+0.1*(max(inner)-min(inner)))
    val=list(ax.get_yticks())
    label=[]
    for x in val:
        if x >= min(inner):
            label.append('%4.0f' % (3000-x))
        else:
            label.append(' ')
    plt.rgrids(val, label, angle=40,weight='bold')                   # Labels    
    cntr = ax.axis()[2]      # aiguille
    plt.plot([0,theta[-1]],[cntr,inner[-1]],linewidth=1,c='k')   
    
    #%%  === Plot 2 : Radial Distance ===  
    
                                             # Substitute radial labels for descending years
                                             # leaving inner 30% empty disc
    # Prepare legend
    ax2 = plt.subplot(122, polar=True)       # Polar view
    p1=plt.scatter(theta[-1], dist[-1],s=aref[0],facecolors='w',edgecolors='r',linewidth=4)
    p2=plt.scatter(theta[-1], dist[-1],s=aref[0],c='r',alpha=.5,edgecolors='k',linewidth=1)
    p3=plt.scatter(theta[-1], dist[-1],s=aref[0],c='b',alpha=.5,edgecolors='k',linewidth=1)
    p4=plt.scatter(theta[-1], dist[-1],s=aref[0],facecolors='none',edgecolors='k',linewidth=1)
    p5=plt.scatter(theta[-1], dist[-1],s=aref[1],facecolors='none',edgecolors='k',linewidth=1)
    p6=plt.scatter(theta[-1], dist[-1],s=aref[2],facecolors='none',edgecolors='k',linewidth=1)
    fig.delaxes(ax2)

    # Prepare polar parameters
    ax2 = plt.subplot(122, polar=True)       
    ax2.set_theta_zero_location("N")
    ax2.set_theta_direction(-1)
    innerrat = .35 # ratio of inner void disc
    inner = (0-innerrat*max(dist))/(1-innerrat)
    ax2.set_ylim(inner,max(dist)*1.05)
    #ax2.set_axisbelow(True)

    
    # Plot
    plt.scatter(theta, dist,s=area,c=colors,alpha=.5,edgecolors='k',linewidth=1)
    plt.scatter(theta[-1], dist[-1],s=areaorg,facecolors='w',linewidth=4,edgecolors='r',zorder=3)
    
    fig.legend((p1,p2,p3,p4,p5,p6),('Origin','Natural','Artificial','Mw <1,5','  2','  2,5'),'upper right',scatterpoints=1,prop={'size':10})
    # Custom radial grid
    val=list(ax2.get_yticks()) 
    lab2 = ['%i' % x for x in val]
    val.insert(0,0.001)
    lab2.insert(0,'0')
    lab2[-1]+='km'
    plt.rgrids(val, lab2, angle=45, weight='bold')
    
    cntr = ax2.axis()[2]      # aiguille
    plt.plot([0,theta[-1]],[cntr,dist[-1]],linewidth=1,c='k')   
    #  Time angular axis
    labelsd =  ['Distance\n 0h', '','2h','','4h','','6h','','8h','','10h','','12h','','14h','','16h','','18h','','20h','','22h',''] # Subtitude labels

    (g_lines, g_labels)  = ax2.set_thetagrids(spoke_angles, labelsd, weight='bold')
    plt.draw()
    plt.show()

    #plt.show()
    
#fig.savefig('circum.png')
#%%    
if __name__ == "__main__":
    import bltools
    
    cfg = bltools.get_config()    
    origin = bltools.origin(cfg['file']['origin'])
    local = get_local(origin)
    #print local
    writejs(local)
    
    plotpolar(origin,local)
    #plt.show()
    #localsism()
    #print "sihex2js inputsihexname outputfilejs"    
    #print "  convert sihex sismo catalog (fixed space columns) to js variable" 
    #sihex2js()
    #print "....Done."
    #pass