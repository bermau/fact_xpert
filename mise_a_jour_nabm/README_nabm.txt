// Readme pour Importation de la NABM

// version pour utilitaires sous python 

// ré-écrit en mai 2017 lors de la mise à jour de la NABM 44.

====== A Faire ======
- il faut utiliser la suite amazilia pour créer les .csv.(je n'ai pas eu le temps de 
tout transcrire en python.
- les csv sont ensuite traités avec deux programmes : util_incompat_2_4digits et util_nabm_2_4digits
- les csv traités (terminés en _ok)) sont incorporés dans la base avec util_load_data_in_sqlite.py

ATTENTION : programme non vérifé.

Gros bug : les vides sont à remplacer par des 0.

====== Lors d'un changement de nomenclature =====
  * aller sur Amélie.fr et récupérer le fichier Excel.
  * placer le dossier de la nabm dans ~/nabm/nabm.xls (fichier non protégé en écriture)

en 2017, il FAUT utiliser l'utilitaire de Amazilia pour exploiter ce fichier : 
  * lancer le fichier : ./nabm_automatisation.sh, Ses menus sont : 
 1) Copier
 2) Supprimer
 3) OO avec macro
 4) Ouvrir OO pour préparer la table de NABM
 5) Inserer NABM dans la nabm_next
 6) OO pour couples
 7) Génerer Couples incompatibles
 8) Inserer incompatibles dans incompatility_next
 9) Tout le traitement
10) Liste des fichiers
11) Explications
12) Shell
13) Quitter

Utiliser les menus suivants dans l'ordre : 
  * 1, 
  * 6, 
  * 7, ce qui donnera le fichier couples_incompat.csv
  
  * 3, ce qui donnera le fichier nabm.csv
    
Détails sur le programme 3: 
  * lancer le programme nabm_macro.ods
  * Lancer le fichier OpenOffice (LibreOffice) 
  * Quand OpenOffice est lancé, Accepter les Macros, 
  * puis  cliquer sur le bouton "Lancer le traitement". Vous devez désigner le fichier nabm.
  * Le tableur travaille très vite.
  * Sortir du tableur.
  * retourner dans le dossier de départ (nabm) et récupérer les fichiers csv.

  
  Déposer les 2 csv dans le répertoire ci dessus dans data_nabm.

  
Vous obtenez 2 fichiers : 
  * /home/bertrand/nabm/pour_incompat.csv
  * /home/bertrand/nabm/nabm.csv

Les fichiers sont en :
    - séparateur : ,
    - utf8
    
pour_incompat.csv est traité par util_incompat_2_4digits.py pour donner pour_incompat_ok.csv
pour nabm.csv est traité par util_nabm_2_4digits.py pour donner le fichier nabm_ok.csv

Les 2 fichiers _ok sont corrigés pour que les nombres soient représentés sous forme d'une suite de 4 chiffres (éventuellement avec des 0).  
    
    

Il semble que le format du fichier excel de la NABM ait été modifié. 
Il semble que sur les versions antérieures à la version 44, les valeurs nulles étaient à 0 et quelles soient à présent à vide.

