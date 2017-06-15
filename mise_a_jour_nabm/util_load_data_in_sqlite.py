#!/bin/env python3
# -*- coding: utf-8 -*-
# file : util_load_data_in_sqlite.py

"""Charge les données csv dans la base sqlite de la nabm.

IMPORTANT : METTRE A JOUR la VARIABLE DE le VERSION de NABM de ce fichier

Il y a 2 fichiers :
- couples_incompat_ok.csv
- nabm_ok.csv

Ces 2 fichiers doivent être :
- utf8
- sep = virugle
- field delimiter  = double guillemets
- field sep est utilisé si besoin
"""

import sys, os, sqlite3
import pdb
import csv

class CsvForNabm(csv.excel):
    delimiter = ";"

# importer les bibliothèque du niveau au dessus.
dirname = os.path.dirname(__file__) # ! __file__ n'est pas défini sous IDLE 2.7 !
if dirname=='':
    dirname='.'
dirname = os.path.realpath(dirname)
updir = os.path.split(dirname)[0]
if updir not in sys.path:
    print("Ajout de {} à la variable PATH".format(updir)) 
    sys.path.append(updir)

# importer les bibliothèques
# import lib_sqlite
import conf_file as Cf
import bm_u

DB_FILE = '../nabm_plus_new_nabm.sqlite'
#DB_FILE = '../nabm_db.sqlite'

VERSION = str(44) 

INCOMPAT_FILE = 'import_nabm/couples_incompat_ok.csv'
INCOMPAT_TABLE_NAME = 'incompatibility' + VERSION

NABM_FILE = 'data_nabm/nabm_ok.csv'
NABM_TABLE_NAME = 'nabm' + VERSION


def read_a_key(msg=''):
    """Protection simple contre l'exécution"""
    input ("ATTENTION ce programme modifie la base : {} \n ! Contrl C or continue".format(msg))
    print("continuing...")
    
def get_sql_foo():
    return """Select 1,2,3"""

def connect_db():
    con = sqlite3.connect(DB_FILE)
    con.execute("Select 1,2,3 ;")
    con.execute("Select * from nabm43 LIMIT 10 ; ")
    con.close()


# Fonctions pour la table incompatibility
def req_create_incompat_table(table_name):
    return """CREATE TABLE {} (
    "code" TEXT  NOT NULL DEFAULT '0000',
    "incompatible_code" TEXT  NOT NULL DEFAULT '0000',
    PRIMARY KEY ("code","incompatible_code")
    )""".format(table_name)

def create_incompat():
    # print("Exécution fictive de : ", req_create_incompat_table())
    con = sqlite3.connect(DB_FILE)
    con.execute(req_create_incompat_table(INCOMPAT_TABLE_NAME))
    con.commit()    

def import_incompat_codes(table):   
    """Modifie la base: importe les données des couples incompatibles"""
    # essai d'écriture efficace, selon :
    # https://docs.python.org/dev/library/sqlite3.html#using-sqlite3-efficiently
    # Ici, je n'utilise pas mon module lib_sqlite.

    con = sqlite3.connect(DB_FILE)
    with open(INCOMPAT_FILE, 'r') as i_file:
        data = i_file.readlines()
    data_to_db = [ item.split(',') for item in data]
    
    for item in data_to_db:
        item[1] = item[1][0:-1] # retrait du '\n' final
    for line in data_to_db[0:20]:
        print(line)
    
    read_a_key('Importer la base des codes incompatibles ? ')
    con.executemany("insert into {} (code, incompatible_code)\
                    values (?, ?)".format(table), data_to_db)
    con.commit() # enregistre dans la base.

def import_incompat_codes_fn():
    "Lance la fonction d'importation des codes incompatibles"
    import_incompat_codes(INCOMPAT_TABLE_NAME)
    
def truncate_incompat():
    """Vide la table des incompatibilités"""
    table = INCOMPAT_TABLE_NAME
    con = sqlite3.connect(DB_FILE)
    con.execute("delete from {}". format(table))
    con.commit()
    
# Fonctions pour la table de la NABM
def req_create_nabm_table(table_name):
    "Renvoie la structure de la table nabmNN dans la base données."
    return """CREATE TABLE {table} 
    ("code" TEXT PRIMARY KEY  NOT NULL  DEFAULT ('0000')
    ,"chapitre" int(11) DEFAULT (NULL)
    ,"sous_chapitre" int(11) DEFAULT (NULL) 
    ,"lettre" char(3) DEFAULT (NULL) ,
    "coef" int(11) DEFAULT (NULL)
    ,"date_creation" date DEFAULT (NULL)
    ,"libelle" varchar(255) DEFAULT (NULL)
    ,"entente" tinyint(1) DEFAULT (NULL)
    ,"Remb100" tinyint(1) DEFAULT (NULL)
    ,"MaxCode" int(11) NOT NULL  DEFAULT (NULL)
    ,"ReglSpec" char(2) NOT NULL  DEFAULT ('')
    ,"RefMed" int(11) DEFAULT (NULL)
    ,"Reserve" tinyint(1) DEFAULT (NULL)
    ,"IniBio" tinyint(1) DEFAULT (NULL)
    ,"Tech" int(11) DEFAULT (NULL)
    ,"RMO" smallint(1) DEFAULT (NULL)
    ,"Sang" tinyint(1) DEFAULT (NULL)
    ,"DateEffet" date DEFAULT (NULL) ,"Rem" text)""".format(table=table_name)

def create_nabm():
    """Crée la structure de la table NABM"""
    # print("Exécution fictive de : ", req_create_incompat_table())
    con = sqlite3.connect(DB_FILE)
    con.execute(req_create_nabm_table(NABM_TABLE_NAME))
    con.commit()

def import_nabm(file, table):
    """Charge les données de la nabm à parti d'un CSV"""
    # On pourrait sans doute faire beaucoup plus simple avec Pandas.
    
    csv.register_dialect('format_nabm', CsvForNabm())
    # lecture du csv
    print("Importation du fichier CSV : {} ".format(file))
    file = open(file, "r")
    data = []
    try:
      reader = csv.reader(file, 'format_nabm')
      for row in reader:   
          data.append(row)
    finally:
        file.close()   
    del data[0] # retrait de l'entête

    # Chargement dans la table
    con = sqlite3.connect(DB_FILE)
        
    # Demande de confirmation et enregistrement dans la table
    bm_u.prt_lst(data[0:19])
    read_a_key('Importer la base des codes de la NABM ? ')
    con.executemany("insert into {} \
                    values (?,?,?,'B',?,?,?,?,?,?,?,?,?,?,?,?,?,?,'')".format(table), data)
    con.commit() # enregistre dans la base.
    
def import_nabm_fn():
    """Donne le nom de fichier et de table pour le chargement de la NABM"""
    import_nabm(NABM_FILE, NABM_TABLE_NAME)    

def truncate_nabm():
    """Vide la table NABM"""
    table = NABM_TABLE_NAME
    con = sqlite3.connect(DB_FILE)
    con.execute("delete from {}". format(table))
    con.commit()

def drop_nabm():
    """supprime la table nabm"""
    table = NABM_TABLE_NAME
    con = sqlite3.connect(DB_FILE)
    con.execute("DROP TABLE IF EXISTS {} ". format(table))
    con.commit()
    
def correct_nabm(table = None):
    """Remède pour ce qui est sans doute un bug du fichier d'import"""

    pass
    # SELECT * from nabm44 WHERE MaxCode =''
    # UPDATE nabm44 set MaxCode=0 ;
    if not table: table = NABM_TABLE_NAME;
    con = sqlite3.connect(DB_FILE)
    con.execute("UPDATE {} set MaxCode=0 WHERE MaxCode ='' ".format(table))
    con.commit()

    
def sql_fn():
    "Une console Sql pour lancer quelques ordres"
    table = NABM_TABLE_NAME
    con = sqlite3.connect(DB_FILE)
    sql = input("Sql : ")
    for row in con.execute(sql):
        print(row)
    print()
def help_fn():
    """Affichage de l'aide"""
    print(help(__name__))
    
def menu():
    """Un petit menu textuel avec quelques ordres pour gérer la base"""
    
    def my_quit_fn():
       raise SystemExit
        
    menu = {
        "01a":("Connection à la base (test de ...)", connect_db), 
        "01":("Créer la table des incompatibilités",create_incompat),
        "02":("Import incompatibles codes",import_incompat_codes_fn),
        "03":("Vider la tables des incompatibilités", truncate_incompat),
        "03z":("Supprimer la tables de la NABM", drop_nabm),
        "04":("Créer la table de la NABM",create_nabm),
        "05":("Importer les données de la NABM",import_nabm_fn),
        "05a":("correct nabm 44 ",correct_nabm), 
        "06":("Vider la table de la NABM", truncate_nabm),
        "07":("Console SQL", sql_fn),
        "08":("Help",help_fn),
        "09":("", my_quit_fn),
        "10":("Quit",my_quit_fn)
           }
    def invalid():
        print("\nChoix invalide !!!\n")       

    while True:

        print("Vous travaillez pour la version : {}\n".format(str(VERSION)))
        for key in sorted(menu.keys()):
            print( key+" : " + menu[key][0])
        print()
        ans = input("Make A Choice : ")
        menu.get(ans,[None,invalid])[1]()

def _test():
    """Execute doctests."""
    import doctest
    doctest.testmod(verbose=True)

if __name__=='__main__':
    # _test()
    menu()


