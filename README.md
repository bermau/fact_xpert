# fact_xpert
Un utilitaire de vérification des factures selon la nomenclature de biologie médicale (NABM).

Fonctionnement prévu dans un terminal.
Pas de version graphique pour l'instant.



Nécessite :
  - python 3.4 OK. (python >=3 devrait être OK). Utiliser de préférence IDLE.
  - pyodbc pour faire fonctionner syn_syn_odbc_connexion.py
  - pour extraire les factures du SGL : Synergy V5 et une base de management de type SQL-Server. 

Utilisation : 
  - copier le fichier conf_file_template.py et conf_file.py
  - modifier le fichier conf_file.py
  - lancer, par exemple le programme facturation.py
  
Démarrage rapide : 
  - copier le fichier conf_file_template.py en conf_file.py
  - A l'aide de IDLE, ouvrir facturation.py. Lancer le programme (touche [F5]). Vous devez obtenir une 
  expertise sur une facture d'essai. 
  
  Démonstration de la connexion à la base de management de Synergy v5). 
  - ouvrir conf_file.py et le renseigner pour votre configuration, en particulier 
  la chaine CONNEXION_BASE_PROD.
  - Exécuter : syn_odbc_connexion.py  (adapter les exemplxe de la fin à votre cas.)
Principaux programmes : 
  - syn_syn_odbc_connexion.py : permet l'extraction de facture depuis le serveur.
  - lib_nabm.py : outils pour tester une facture vis-à-vis de la nabm.
  - facturation.py : test d'une facture.
  - syn_par_IEP.py (v0.14): extrait de Synergy (v5, base de Sql Serveur) une facture pour un IEP et une date donnée
  et lance l'expertise.

Version du 02/09/2016 : 
- syn_odbc_connexion.py permet pour un jour donné: 
  - de récupérer la liste des patients
  - pour chaque patient de récupérer la liste des demandes
  - pour chaque patient d'établir une facture cumulée.
  - pour chaque facture cumulée, un audit est pratiqué avec pour règles : 
        - la recherche des actes surnuméraires dans la liste de protéines, 
        - la recherche des actes surnuméraires dans la liste des séro hép B.
  - ce fichier utilise la librairie lib_nabm.

5 sept : 
- introduction de unittest.
6 sept : 
-  Mise en place data_for_tests.
9 sept : 
- Mise en place des suggestions.

Explications diverses : 
- lib_nabm permet : 
  - contient une base NABM (NABM 41, 42, 43) dans une base sqlite.
  - contient un décorateur pour n'enregistrer que les dossiers en anomalie.

  
version 0.04 : détection des erreurs de nombre maximum de cotation.
  
version 0.08 : 
Depuis le programme syn_odbc_connexion, on peut réaliser les opérations suivantes:

Etudier la facturation d'un jour donné.
    _demo_etude_facturation_d_un_jour("05/06/2016")
Cette fonction accepter un filtre de service. 
Le filtre est soit une seule UF (noter le format), ou une série d'UF (noter le format).
    _demo_etude_facturation_d_un_jour("02/06/2016",  uf_filter='6048')
    _demo_etude_facturation_d_un_jour("02/06/2016",  uf_filter=[ 6048, 2105, 'UHCD'])
version 0.908

