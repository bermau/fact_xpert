# fact_xpert
Un utilitaire de vérification de factures NABM.
Fonctionnement prévu dans un terminal.

Nécessite :
  - python 3.4 OK. (python >=3 devrait être OK).
  - pyodbc pour faire fonctionner syn_syn_odbc_connexion.py

Utilisation : 
  - copier le fichier conf_file_template.py et conf_file.py
  - modifier le fichier conf_file.py
  - lancer, par exemple le programme facturation.py

Principaux programmes : 
  - syn_syn_odbc_connexion.py : permet l'extraction de facture depuis le serveur.
  - lib_nabm.py : outils pour tester une facture vis-à-vis de la nabm.
  - facturation : test d'une facture.

Version du 02/09/2016 : 
- syn_syn_odbc_connexion.py permet pour un jour donné: 
  - de récupérer la liste des patients
  - pour chaque patient de récupérer la liste des demandes
  - pour chaque patient établit une facture cumulée.
  - pour chaque facture cumulée, un audit est pratiqué avec pour règles : 
        - la recherche des actes surnuméraires dans la liste de protéines, 
        - la recherche des actes surnuméraires dans la liste des séro hép B.
  - ce fichier utilise la librairie lib_nabm.

- lib_nabm permet : 
  - contient une base NABM (NABM 41, 42, 43)dans une bae sqlite.
  - contient un décorateur pour n'enregistrer que les dossiers en anomalies.

