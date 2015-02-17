#  !/usr/bin/env python
#-*- coding: utf-8 -*-

#import csv
#

#def localsism():

import numpy as np
#from matplotlib import cm
#from matplotlib import pyplot
#%% Inits
fcata = '/Volumes/SharedFolders/Resif/Data/catalogue-SiHex/Artif/Catalogue_SiHex_Mw.lst'
fileout = '/Volumes/SharedFolders/Resif/blast/html/localsism.js'
radius  = 40. #(km)
cata = np.genfromtxt(fcata,dtype={'names':('id','date','time','lat','lon','depth','auteur','type','Mw'), 'formats':('S11','S22','S33','f4','f4','f4','S8','S5','f4')})    
#%%
import xmlev
origin = xmlev.origin('orginfo.xml')     
# Cercle de 30 km autour de l'evenement
deg2rad = np.pi/180
r2 = (cata[:]['lat']-origin['lat'])**2 + ((cata[:]['lon']-origin['lon'])*np.cos(origin['lat']*deg2rad))**2
R = 6371 # Earth radius (km)
i = [i for i in range(0,cata.size) if r2[i]< (radius/(R*deg2rad))**2]
local = cata[i]   
d = np.sqrt(r2[i])*R*deg2rad
   
# Write javascript array for maptool
# -----------------------------------
fout = open(fileout,'wb')
fout.write("var locsism = [ // EVID YYY/MM/DD HH:MM:SS.S LAT LON DEPTH AUTEUR TYPE Mw\n")
for line in local:
    fout.write('["%8s", "%10s", "%10s", %9.5f,%9.5f,%6.1f, "%6s", "%2s",%5.2f],\n' % (line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8] ));
fout.write("];")
fout.close()
#%%

# Prepare figure's data
# ---------------------
#%% Compute origin's parameters
from datetime import datetime

#  Catalog timestamp, format normalised time in [0,1] and year decimal
timestamp = [datetime.strptime(x['date'] + 'T' + x['time'],"%Y/%m/%dT%H:%M:%S.%f") for x in local]
frac_hour = [timestamp[i].time().hour*3600+timestamp[i].time().minute*60+timestamp[i].time().second for i in xrange(local.itemsize)]
frac_hour = [x / 86400. for x in frac_hour]
fracyear = [timestamp[i].year + (timestamp[i]-datetime(timestamp[i].year,1,1,0,0,0)).days/365. for i in xrange(local.itemsize)]

#  Origin timestamp
org_timestamp=datetime.strptime(origin["date"],"%Y-%m-%dT%H:%M:%S.%fZ")
org_hour = (org_timestamp.time().hour*3600+org_timestamp.time().minute*60+org_timestamp.time().second)/86400.
org_year = org_timestamp.year + (org_timestamp-datetime(org_timestamp.year,1,1,0,0,0)).days/365.
fracyear.append(org_year)
frac_hour.append(org_hour)
d = np.append(d,0)

#  Graphic common frame
from matplotlib import pyplot as plt
# Create figure if needed
tit = "Local SiHex"
if tit not in plt.get_figlabels():
    fig=plt.figure(num=tit, figsize=(12, 5), facecolor='none')
else:
    fig=plt.figure(tit) # make current
    plt.clf()

#%% test
ax3 = plt.subplot(1,13,5)
plt.plot([1,3],[1,5]) 

#%% ======
#%%  === Plot 1 : Time Date ===   
theta = 2*np.pi*np.array(frac_hour)
colors=['r' if x['type'] in ('ke','se','ls') else 'b' for x in local] # red for natural, blue otherwise
area = [100*(max((x['Mw'],1.5))-1.3)**2 for x in local]
aref = [100*(x-1.3)**2 for x in (1.5,2,2.5)] # Further legend of plot


ax = plt.subplot(121, polar=True)        # Polar view
#ax=plt.subplot2grid((3,3), (1, 0), colspan=2, polar=True)
#ax.subplots_adjust(left  = 0.125,right = 0.4,  bottom = 0.1, wspace = 0.2, hspace = 0.5)
#ax.add_axes([0.1, 0.1, 0.4, 0.4])
ax.set_theta_zero_location("N")          # Clockwise origin up
ax.set_theta_direction(-1)        
#ax.set_title("Date", fontsize=14) # Title
plt.xlabel('Date', fontsize=14)

inner=[3000-x for x in fracyear]         # Substitute radial labels for descending years
                                         # leaving inner disc empty
                                 
plt.scatter(theta, inner,s=area,c=colors,alpha=.5) # Plot catalog
plt.scatter(theta[-1], inner[-1],s=70,facecolors='r',edgecolors='k',linewidth=2) # Overplot origin
plt.scatter(theta[-1], inner[-1],s=1,facecolors='none',edgecolors='k',linewidth=2)
#  Time angular axis
labels = ['0 h', '3 h', '6 h','9 h','12 h','15 h','18 h','21 h'] # Subtitude labels
spoke_angles=[ 0., 45., 90., 135., 180., 225., 270., 315.]
(g_lines, g_labels)  = ax.set_thetagrids(spoke_angles, labels)

#  Year radial axis
ax.set_ylim(min(inner),max(inner))
val=list(ax.get_yticks())
label = ['%4.0f' % (3000-x) for x in val]
innerrat = .3                            # let 30% empty center
infbound = max(val) - (max(val)-min(val))/(1-innerrat)
val.insert(0,infbound)                   # Related bound
label.insert(0,'')
plt.rgrids(val, label)                   # Labels



#%%  === Plot 2 : Time Distance ===  

 
#ax2 = plt.subplot(122, polar=True)       # Polar view
#ax2.set_theta_zero_location("N")
#ax2.set_theta_direction(-1)
#ax2.set_title("Distance (km)", fontsize=14)

                                         # Substitute radial labels for descending years
                                         # leaving inner 30% empty disc
# Prepare legend
ax2 = plt.subplot(122, polar=True)       # Polar view
p1=plt.scatter(theta[-1], d[-1],s=area[0],c='r',alpha=.5)
p2=plt.scatter(theta[-1], d[-1],s=area[0],c='b',alpha=.5)
p3=plt.scatter(theta[-1], d[-1],s=area[0],facecolors='r',edgecolors='k',linewidth=2)
p4=plt.scatter(theta[-1], d[-1],s=aref[0],facecolors='none',edgecolors='k',linewidth=1)
p5=plt.scatter(theta[-1], d[-1],s=aref[1],facecolors='none',edgecolors='k',linewidth=1)
p6=plt.scatter(theta[-1], d[-1],s=aref[2],facecolors='none',edgecolors='k',linewidth=1)
fig.delaxes(ax2)
#plt.clf()

ax2 = plt.subplot(122, polar=True)       # Polar view
ax2.set_theta_zero_location("N")
ax2.set_theta_direction(-1)
#ax2 = plt.subplot(122, polar=True)    
innerrat = .35  
#ofs = (innerrat*max(d) - min(d))/(1-innerrat)
#innerd = d+ofs
inner = (0-innerrat*max(d))/(1-innerrat)
ax2.set_ylim(inner,max(d)*1.05)
plt.scatter(theta, d,s=area,c=colors,alpha=.5)
plt.xlabel('Distance (km)', fontsize=14)
#plt.legend(('Natural','Artificial'),scatterpoints=1,marker('*'),fontsize=8,bbox_to_anchor=(0., 1.02, 1., .102))
plt.figlegend((p1,p2,p3,p4,p5,p6),('Natural','Artificial','Origin','Mw <1,5','  2','  2,5'),'upper right',scatterpoints=1,fontsize=8,)
#qq=ax2.get_ybound()
#print qq

val=list(ax2.get_yticks())
lab2 = ['%i' % x for x in val]
val.insert(0,0.001)
lab2.insert(0,'0')
plt.rgrids(val, lab2)
#ax2.set_yticklabels(ll)
#print ll
#lab2=[xx.get_text() for xx in ax2.get_yticklabels()]
#print lab2
plt.scatter(theta[-1], d[-1],s=70,facecolors='r',edgecolors='k',linewidth=2)
plt.scatter(theta[-1], d[-1],s=1,facecolors='none',edgecolors='k',linewidth=2)
#ax2.set_yticklabels(lab2)

#plt.rgrids(val, lab2)
#ax2.clear()
#plt.scatter(theta, innerd,s=area,c=colors,alpha=.5)
# Superpose origin
#plt.scatter(theta[-1], innerd[-1],s=70,facecolors='r',edgecolors='k',linewidth=2)
#plt.scatter(theta[-1], innerd[-1],s=1,facecolors='none',edgecolors='k',linewidth=2)

#  Time angular axis
labels = ['0 h', '3 h', '6 h','9 h','12 h','15 h','18 h','21 h']
spoke_angles=[ 0., 45., 90., 135., 180., 225., 270., 315.]
(g_lines, g_labels)  = ax2.set_thetagrids(spoke_angles, labels)
#  Dist radial axis
#ax2.set_ylim(0,max(innerd)*1.05)
#val=list(ax2.get_yticks())
#lab2 = ['%4.1f' % (x) for x in val]
#infbound = max(val) - (max(val)-min(val))/(1-innerrat)
#plt.rgrids(val+ofs, lab2) #

#%%
plt.show()



#N = local.itemsize
#r = np.array([((t0 - timestamp[i]).days)/365.25 for i in xrange(local.itemsize)]) # make np array of years
#y = [timestamp[i].year()+timestamp[i].time().minute*60+timestamp[i].time().second for i in xrange(local.itemsize)]

#r = 2*rand(N)
#theta = 2*pi*rand(N)
#theta = [2*pi*x for x in frac_hour]
#area = 20
#colors = theta
#plt.clf()
#fig=plt.figure(figsize_in inc=(12,3))
#faire un if ~exsit fig then fig=figure(size_inch(blabla))
#fig.set_size_inches(12,4)
#fig.set_size_inches(18.5,12.5)
#fig.set_figwidth(5)

    

#if 'fig' in locals() or 'fig' in globals():
#else:
    
#plt.fignum_exists(<figure number>):
    # Figure is still opened
#    fig=plt.gcf()
#    plt.clf()
#    print "existe fig"
#    fig.number
#else:
    # Figure is closed    
#    print "nexiste pas, recreee"
#    fig = plt.figure(num=125, figsize=(12, 5), facecolor='none')
    
#figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')

#%%
#c = scatter(theta, r, c=colors, s=area, cmap=cm.hsv,label='ke')
#axis([0,5,0,5])
#c = plt.scatter(theta, fracyear, s=area, cmap=cm.hsv,label='ke')


#print qq[3]
#ax.invert_xaxis()
#plt.rgrids((2000,1995,1990), ('Tom20', 'Dick195', 'Harry190' ))
#plt.gca().invert_xaxis()
#ax.rgrids(radii, labels=None, angle=22.5)

#rc('xtick', labelsize=12)
#ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], projection='polar', axisbg='#d5de9c')
#ax.set_xlim(max(r)*1.03,-1)
#ax.invert_xaxis()
#ax.axis([0, 100, 0, 5])
# legende naturel, artificiel ax.legend()
#grid(True)
#c.set_alpha(0.75)
#def onclick(event):
#    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
#        event.button, event.x, event.y, event.xdata, event.ydata)
#
#def mouse_move(event):
#    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
#        event.button, event.x, event.y, event.xdata, event.ydata)
#
#cid = fig.canvas.mpl_connect('button_press_event', onclick)
#cid2 = fig.canvas.mpl_connect('bmotion_notify_event', mouse_move)

#fig.savefig('circum.png')
#%%    
if __name__ == "__main__":
    #localsism()
    #print "sihex2js inputsihexname outputfilejs"    
    #print "  convert sihex sismo catalog (fixed space columns) to js variable" 
    #sihex2js()
    #print "....Done."
    pass