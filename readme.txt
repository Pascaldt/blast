20/10/2015:

 Description :
 -------------
 Maptool affiche via seiscomp3 la vue satellite d'un seisme  complétée d'informations pour faciliter la discrimination des tirs de carrière (ex. http://scresif.olympe.in).
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
  Mettre a jour les chemins dans blast.cfg. Fermer scolv, puis:
  $ seiscomp exec scolv --debug (le mode debug est facultatif. Il permet de voir si tout va bien)

  Sur selection d'une origine, des informations complementaires apparaissent dans scolv/location view : Distance aux 3 plus proches carrieres, bouton "Map tool" affichant vue satellite et diagrammes statistiques
   
  Merci pour vos remarques à pascal.guterman@cnrs.fr

 
 liste des fichiers:
 -------------------
  blast/readme.txt
  blast/blast.cfg              chemins et parametres
  blast/blhistory.py           historique local. Sortie javascript et plots                    
  blast/bltools.py             lecture config et fichiers dynamiques (stations, event, ..)
  blast/closest.py             carrieres les plus proches
  blast/flushev.py             ecriture infos internes seiscomp dans fichiers dynamiques
  blast/maptool.py             (2) creation et lancement vue satellite et plots 
  blast/maptool_callback.py    (1) point d'entre haut niveau du bouton "Map tool" 
  blast/orginfo.xml            dynamique - epicentre. 
  blast/orginfo_ev.txt         dynamique - evenement
  blast/orginfo_inventory.xml  dynamique - stations 

  html/carrieres.js            dynamique
  html/history.js              dynamique
  html/index.html              point d'entree vue satellite            
  html/infobox.js              popup
  html/logo_*.png              logos et markers javascript
  html/origin.js               dynamique
  html/stations.js             dynamique
  html/carrieres.js            dynamique
  html/v3_ll_grat.js           grille des lon-lat

  cfg/addto_queries.cfg        copier dans --> .seiscomp/queries.cfg
  cfg/addto_scolv.cfg          copier dans --> seiscomp/etc/scolv.cfg

  data/                        catalogues sismique et carrieres (voir blast.cfg), petits outils de conversion. 

  -- fin --
