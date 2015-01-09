30/10/2014:

 Description :
 -------------
 Maptool affiche dans l'explorateur par défaut les informations provenant de 
  seiscomp et les complete. L'intéraction avec la config seiscomp se limite à :
  - Etendre scolv.cfg et queries.cfg
  - Installer ephem.py + dependance. 
  - Tout les autre fichiers tiennent dans un répertoire unique ~/seiscomp/blast

 Installation :
 --------------
  $ cd
  sauver la config actuelle, si ces fichiers existent :
  $ cp seiscomp3/etc/scolv.cfg seiscomp3/etc/scolvref.cfg 
  $ cp .seiscomp3/queries.cfg .seiscomp3/queriesref.cfg 

   sans github:  
  telecharger https://github.com/scresif/blast/archive/master.zip
  renomer Downloads/blast-master en ~/tmp

   avec github: 
  $ git clone https://github.com/scresif/blast.git tmp



  $ mv tmp/seiscomp3/blast ~/seiscomp3/ 
  Merger le debut de tmp/.seiscomp3/queries.cfg dans ~/.seiscomp3/queries.cfg 
  Merger tmp/seiscomp3/etc/scolv.cfg dans ~/seiscomp3/etc/scolv.cfg
  Effacer ~/tmp 

 Librairies python:
 ------------------
  $ sudo app-get install ephem ou bien sudo pip install ephem avec dependance  
  Voilà. (Re)lancer scolv, en mode debug pour voir si tout va bien
  $ seiscomp exec scolv --debug 
  Merci pour vos remarques (pascal.guterman@dt.insu.cnrs.fr)


 liste des fichiers:
 -------------------
  seiscomp/etc/scolv.cfg       ajout indicateurs et bouton "Maptool"
  .seiscomp/queries.cfg        extension de config
  blast/readme.txt
  blast/closest.py             carrieres les plus proches
  blast/flushev.py             ecriture xml des epicentre et inventaire 
  blast/indic1.py              calcul indicateurs dans scolv onglet 'Location'
  blast/maptool_callback.py    point d'entre maptool. Lecture origin, stations, carrieres et affichage 
  blast/maptool.py             conversion xml --> javascript des infos dynamiques 
  blast/orginfo.xml            data dynamique - epicentre xml. 
  blast/orginfo_ev.txt         data dynamique - nom d'evenement
  blast/orginfo_inventory.xml  data dynamique - stations xml (recree à chaque fois)
  blast/xmlev.py               extraction sc3 xml bas niveau


  html/infobox.js              popup
  html/logo_daytime.png        logos jour/lunch/nuit locale
  html/logo_sandwich.png       
  html/logo_sleepmoon.gif      
  html/logo_void.png           si erreur
  html/maptool.html            fichier principal
  html/v3_ll_grat.js           grille des lon-lat
  html/origin.js               data dynamique epicentre, carrieres et stations 
  html/carrieres.js            
  html/stations.js             




 Preprocessing:
 --------------
  - rassembler, trier la liste des carrières csv
  - la convertir en js

  - data/carrieres_roches_massivesll.csv

 A faire:
 --------
 - diagrammes polaires

