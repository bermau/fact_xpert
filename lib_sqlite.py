# -*- coding: utf-8 -*-
# Gestion des connexions à une base sqlite.
# Evolution : Remplacement de basDonn par con.


import sqlite3
import os, sys
import conf_file as Cf # fichier de parametrage avec nom de la base sqlite

class GestionBD:
    """Mise en place et interfaçage d'une base de données Sqlite."""

    def __init__(self, dbName=None, in_memory=False):
        "Établissement de la connexion et création du curseur"
        if in_memory:
            self.con = sqlite3.connect(':memory:')
            self.cur = self.con.cursor()   # création du curseur
            self.echec = 0           
        else:
            self.dbname = dbName
            # Vérifier que le fichier de DB existe
            if not os.path.isfile(dbName): 
                print("Error : Database {} does not exist".format(dbName))   
            try:
                self.con = sqlite3.connect(dbName)
            except Exception as err:
                sys.stderr.write(('Connexion to database failed :\n'\
                      'SQL Error is :\n%s' % err))           
                self.echec = 1
            else:
                # print("Connexion OK") 
                self.cur = self.con.cursor()   # création du curseur
                self.echec = 0

    def execute_sql(self, req, param =None):
        "Exécution de la requête <req>, avec détection d'erreur éventuelle."
        try:
            # obligé de faire cette bidouille infame ! Je dois améliorer le
			# passage des arguments
            if param == None :
                self.cur.execute(req)
            else:
                self.cur.execute(req, param)
        except sqlite3.Error as e:
            sys.stderr.write("An SQL error occurred: {}\n".format(e.args[0]))
            sys.stderr.write("Request was: {}\n".format(req))
            sys.stderr.write("Param  was: {}\n".format(param))
            return 0
        else:
            return 1

    def resultat_req(self):
        "renvoie le résultat de la requête précédente (une liste de tuples)"
        return self.cur.fetchall()

    def quick_sql(self, req):
       if self.execute_sql(req):
          # Afficher les noms de colonnes
          records=self.resultat_req()         # ce sera un tuple de tuples
          # TypeError: 'NoneType' object is not iterable
          try:
             for i in self.cur.description:
                 print(i[0], '|', end=' ')
             print()
          # afficher les résulats
             for rec in records:             # => chaque enregistrement
                for item in rec:            # => chaque champ dans l'enreg.
                  print(item, '|', end=' ')
                print()
                 # print("|".join(rec))
                
          except:
             print("Rien à afficher")
    def commit(self):
        if self.con:
            self.con.commit()         # transfert curseur -> disque

    def close(self):
        if self.con:
            self.con.close()
            print("Database {} has been closed".format(self.dbname))

if __name__ == '__main__': 
    print("Connexion à base de donnée")
    BASE = GestionBD(Cf.NABM_DB)
    if BASE.echec:
        print("Pb connexion")
    else:
        print("OK")
    BASE.quick_sql("Select 1,2,3 ")
    BASE.quick_sql("Select 456, 345")
    BASE.quick_sql("Select * from nabm WHERE ID = 126")
    BASE.close()

    # Autre exemple avec une base en mémoire RAM.
    INRAM=GestionBD(in_memory=True)
    INRAM.quick_sql("Select 1,2,3 ")
    
