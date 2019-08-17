
"""Utilitaire pour la mise à jour de la NABM
pour l'instant ne gère que la table incompatibility.

contient un menu déroulant."""

import sys
import csv
import pandas as pd
import numpy as np
# import lib_sqlite
import conf_file as Cf
import lib_nabm
from lib_bm_utils import title as titrer

# global nabm_version
nabm_version= 49

# Pardéfaut le logiciel attend des fichiers dans le répertoire suivant : 
import_export_rep = "mise_a_jour_nabm/input_output"

def get_excel_file_name():
    "retourne le nom attendu du fichier de NABM"
    return "NABM"+"{:03d}".format(nabm_version)+".xls"

def get_incompatibility_table_name():
    "retourn le nom de la table d'incompatibilité"
    return "incompatibility" + str(nabm_version)

separator = ";"

def _test():
    """Execute doctests."""
    import doctest
    doctest.testmod(verbose=True)

def set_nabm_version( val ):
    """Indiquer au système la version de NABM sur laquelle on travaille.
num : numéro sur 1 à 3 chiffres.
    >>> set_nabm_version(49)"""
    global nabm_version
    nabm_version = int(val)


def choose_nabm_version():
    "Demande la numéro de version de NABM sur laquelle on va travailler."
    print()
    rep = input("Indiquer la version de NABM sur laquelle vous voulez travailler(exemple : 49)")
    set_nabm_version(rep)
    print("Version de NABM : {}".format(nabm_version))
    
def describe_a_code(input_code = None):
    if input_code is None :
        input_code = input("Code décrire (4 chiffres) : " )
    BASE = lib_nabm.Nabm()
    BASE.NABM_DB.quick_sql("Select * from nabm where code = '{}'".format(input_code), single_column = True)
    
def search_code_containing():
    input_string = input("Saisie une chaîne à chercher dans le libellé (non sensible à la case) : ")
    BASE = lib_nabm.Nabm()
    BASE.NABM_DB.quick_sql("""Select * from nabm where instr(libelle, "{}") > 0""".format(input_string.upper()) )

def sql():
    """Boucle de lancement de commandes SQL."""
    continuer = True 
    while continuer :
        input_string = input('SQL : ("Q" to quit)')
        if input_string == "Q":
            continuer = False
        else:
            BASE = lib_nabm.Nabm()
            BASE.NABM_DB.quick_sql(input_string)

def list_tables():
    """Affiche la liste des tables de la base de données"""
    req = "select name from sqlite_master where type = 'table'"
    BASE = lib_nabm.Nabm()
    BASE.NABM_DB.quick_sql(req)
        

    
def vider_table (table_name=incompatibility_table_name):
    "Vider une talbe sqlite."
    BASE = lib_nabm.Nabm()
    BASE.NABM_DB.quick_sql("DROP TABLE IF EXISTS {}".format(table_name))
    
def creer_table_inc(table_name = incompatibility_table_name):
   
    sql ="""
CREATE TABLE IF NOT EXISTS {} (
 code TEXT,
 incompatible_code TEXT)
 """.format(table_name)
    BASE = lib_nabm.Nabm()
    BASE.NABM_DB.quick_sql(sql)

def load_csv(table_name, csv_file):
    "Cahrge un CSV dans une table."
    FILE = open(csv_file, "r")
    reader = csv.reader(FILE, delimiter = separator)
    to_db = [(c1, c2) for c1, c2 in reader]

    BASE = lib_nabm.Nabm()
    BASE.NABM_DB.con.executemany("INSERT INTO {} ('code', 'incompatible_code') VALUES (?, ?) ; ".format(table_name), to_db[1:])
    BASE.NABM_DB.con.commit()
    BASE.NABM_DB.con.close()
    
def load_csv_inc():
    "Charge le CSV des incompatibilités."
    load_csv(incompatibility_table_name, "mise_a_jour_nabm/input_output/incompatible_codes.csv")

def voir_structure(table):
    "Affiche une structure de table de sqlite."
    BASE = lib_nabm.Nabm()
    BASE.NABM_DB.quick_sql("PRAGMA table_info({})".format(table))
    
def voir_structure_inc():
    "Structure de la table des incompatibilités."
    voir_structure(incompatibility_table_name)

def quitter():
    "Quit"
    print("OK, Quitter")
 
def creer_fichier_csv_incompatibilites(path_to_file, path_to_output):
    """Creation du CSV des incompatibilités de la NABM.
    Ce fichier est créé pour être intgré dans la base sqlite."""
    pass
    ws = pd.read_excel(path_to_file) 
    # ws = wb.parse(sheet_name = 0)
    incomp = ws[ws['CODES INCOMPATIBLES'].notnull()] [['CODE', 'CODES INCOMPATIBLES']]
    la_liste = incomp.values.tolist()

    with open(path_to_output,"w") as f:
        def formater(x, y ):
            return str(x) + separator + str(y) +"\n"
        f.write("code" + separator + "incompatible_code\n")
        for line in la_liste:
            code = line[0]
            incompatibles_codes = line[1]
            if isinstance(line[1], int):
                f.write(formater(code, incompatibles_codes))
            else:
                for item in incompatibles_codes.split("-"):
                    f.write(formater(code, item))

                    
def creer_fichier_csv_nabm(path_to_file, path_to_output):
    """Creation du CSV de la NABM à partir du fichier NABM.
Ce fichier est créé pour être intégré dans la base sqlite.
        TODO : SIMPLIFIER
"""
        
    data_in = path_to_file    
    data_out =  path_to_output

    separator = ";" # sep for csv import and export.

    def to_int(x):
        """Force x to integer or 0 if null"""
        return x if x else 0

    # on importe une première fois : 
    wb  =  pd.read_excel(data_in)
    dicto = { col : to_int for col in wb.columns if wb[col].dtypes == 'float64' }
    # seconde importation : 
    wb2 =pd.read_excel(data_in, converters= dicto)
    wb3 = wb2[wb2.columns[:-1]]
    wb3.to_csv(data_out, sep = separator, index = False, encoding = "UTF-8")

def _creer_fichier_csv_nabm():
    """Lance la création du fichier CSV de la NABM."""
    # set_nabm_version(num)
    path_to_file = import_export_rep+"/" + get_excel_file_name()
    path_to_output = import_export_rep+"/" + "nabm" + str(nabm_version) +".csv"

    print("\nCréation du fichier NABM")
    print("Fichier d'entrée : {}".format(path_to_file))
    print("Fichier de sortie : {}".format(path_to_output))
    creer_fichier_csv_nabm(path_to_file, path_to_output)

def _creer_fichier_csv_incomp():
    """Lance la création du fichier CSV des incompatibilités"""
    #import pdb
    #pdb.set_trace()
    
    
    path_to_file = import_export_rep+"/" + get_excel_file_name()
    path_to_output = import_export_rep+"/" + "incompatible_codes" + str(nabm_version) +".csv"
    print("\nCréation du fichier des incompatibilités")
    print("Fichier d'entrée : {}".format(path_to_file))
    print("Fichier de sortie : {}".format(path_to_output))
    creer_fichier_incompatibilites(path_to_file, path_to_output)
    
def traitement_complet_nabm(num_nabm):
    """A partir d'un numéro de nabm, crée les fichiers csv et les importe
dans la base sqlite."""

    _creer_fichier_nabm(num_nabm)
    creer_fichier_incompatibilites(num_nabm)
    # integrer_fichier_nabm
    # integrer_incompatibilites

   
class Menu():
    """Un petit menu pour gérer quelques paramètres"""
    lst_menu = [
        ["1", "Décrire un code", describe_a_code],
        ["V", "Indiquer la version de NABM", choose_nabm_version],
        ["C", "Chercher dans la description", search_code_containing],
        ["S", "Requete SQL", sql],
        ["L", "Liste des tables", list_tables],
        ["CIT","Créer table incompat", creer_table_inc ],
        ["LIT", "Load table incompat", load_csv_inc],
        ["DIT", "Drop (supprimer table incompat)", vider_table],
        ["SIT", "Show structure table_incompat", voir_structure_inc],
        ["CNABM", "Créer Fichier CSV pour NABM", _creer_fichier_csv_nabm],
        ["CINC", "Créer Fichier CSV pour incompatibilité", _creer_fichier_csv_incomp],
        ["Q", "Quitter", quitter],
                ]
    
    def __init__(self):
        self.print_menu()
        pass
    
    def print_menu(self):
        
        def menu():
            """Affiche le menu et retourne une réponse clavier."""

            for (lettre, texte, action) in Menu.lst_menu:
                print(lettre + ' ' + texte)
            rep = input ("Choix : ")
            return rep

        rep =''
        while rep.upper() != 'Q':
            print()
            rep = menu()
            for line in Menu.lst_menu:
                if rep == line[0]:
                    line[2]()

    
if __name__=='__main__':
    #_test()
    pass
    Menu()

