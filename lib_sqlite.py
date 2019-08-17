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
                # IMPORTANT la connection est 10 fois plus longue si le fichier 
                # est verrouillé en écriture.
                self.con = sqlite3.connect(dbName)
            except Exception as err:
                sys.stderr.write(('Connexion to database failed :\n'\
                      'SQL Error is :\n%s' % err))           
                self.echec = 1
            else:
                self.cur = self.con.cursor()   # création du curseur
                self.echec = 0
#        if self.echec:
#            raise ValueError('Connexion to database {} failed'.format(dbName))

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

    def quick_sql(self, req, single_column = False):
        """Print an SQL query.
        sql : string
        single_column : display the result on one column with title on the left.
        Possible only if the result of the query contains one record"""
        
        if self.execute_sql(req):
            # Afficher les noms de colonnes
            records = self.resultat_req()         # ce sera un tuple de tuples
          
            try:
                if not single_column:
                    # Mode multicolonnes.
                    for i in self.cur.description:
                        print(i[0], '|', end=' ')
                    print()
                    for rec in records:             # => chaque enregistrement
                         for item in rec:            # => chaque champ dans l'enreg.
                             print(item, '|', end=' ')
                         print()
                         # print("|".join(rec))
                else:
                    for pos, field_label in enumerate(self.cur.description):
                        import pdb
                        # pdb.set_trace()
                        # print("OKOKO3")
                        print(field_label[0], end=' : \t')
                        print(records[0][pos])
                      
            except:
                print("Erreur : Rien à afficher : SQL is : {}".format(req))

    def quick_sql_OK(self, req):
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
        # if self.con: # ??
        self.con.commit()         # transfert curseur -> disque

    def close(self):
        pass
        if self.con:
            self.con.close()
            # sys.stderr.write("Database {} has been closed\n".format(self.dbname))

if __name__ == '__main__': 
    print("Connexion à base de donnée")
    BASE = GestionBD(Cf.NABM_DB)

    BASE.quick_sql("Select 1,2,3 ")
    BASE.quick_sql("Select 456, 345")

    BASE.quick_sql("Select * from nabm Limit 5")
    print()
    BASE.quick_sql("Select * from nabm where code = '0126'")
    BASE.close()

    # Autre exemple avec une base en mémoire RAM.
    INRAM=GestionBD(in_memory=True)
    INRAM.quick_sql("Select 1,2,3 ")
    
