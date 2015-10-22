20/10/2015:

 Description :
 -------------
 Maptool affiche la vue satellite d'un seisme, typiquement via seiscomp3, complétée d'informations pour faciliter la discrimination des tirs de carrière.
- pointage des carrières 
- echelle des distances 
- sismicite historique 
- heure, jour/nuit, numero de jour locaux 
- statistiques locales


Le module se trouve dans un répertoire unique, aucune modification de seiscomp3 n'est necessaire. L'intéraction avec seiscomp3 se limite à completer deux fichiers de configuration, scolv.cfg et queries.cfg.

 Installation :
 --------------
  sans github: telecharger https://github.com/scresif/blast/archive/master.zip
  mkdir ~/seiscomp3/blast
  y placer les fichiers decomprimes

  avec github: 
  $ git clone https://github.com/scresif/blast.git ~/seiscomp3/blast (!!a verifier repertoire et pull)

  Seules modifications de config seiscomp3: ajouts labellises
  $ cd ~/seiscomp3/blast
  $ cat cfg/addto_scolv.cfg >>  ~/seiscomp3/etc/scolv.cfg
  $ cat cfg/addto_queries.cfg >>  ~/.seiscomp3/queries.cfg

  Verifier les droits en exec:
  $ chmod +x flushev.py scolvloc.py maptool_callback.py

 Librairies python pyephem et pytz:
 ------------------
  $ sudo app-get install ephem ou bien sudo pip install ephem avec dependance  
  
 Utilisation :
 ------------- 
  Fermer scolv et le relancer. Ajouter le mode debug pour voir si tout va bien:
  (fermer scolv)
  $ seiscomp exec scolv --debug 

  Sur selection d'une origine, des informations complementaires apparaissent dans scolv/location view : Distance aux 3 plus proches carrieres, bouton "Map tool" affichant vue satellite et diagrammes statistiques
   
  Merci pour vos remarques à pascal.guterman@cnrs.fr

 
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

