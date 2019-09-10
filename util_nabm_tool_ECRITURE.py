"""Utilitaire pour la mise à jour de la NABM
gère des 2 tables nabm et incompatibility.

contient un menu déroulant."""

import sys
import csv
import pandas as pd
import numpy as np
# import lib_sqlite  
import conf_file as Cf
import lib_nabm
from lib_bm_utils import title as titrer
from lib_bm_utils import to4digits

# global nabm_version
nabm_version= 49

# Par défaut le logiciel attend des fichiers dans le répertoire suivant : 
import_export_rep = "mise_a_jour_nabm/input_output"

def get_excel_file_name():
    "retourne le nom attendu du fichier de NABM"
    return "NABM"+"{:03d}".format(nabm_version)+".xls"

def get_fullname_to_excel_file():
    return import_export_rep+"/" + get_excel_file_name()

def get_incompatibility_table_name():
    "retourne le nom de la table d'incompatibilité dasn la table sqlite"
    return "incompatibility" + str(nabm_version)

def get_nabm_table_name():
    "retourne le nom de la table d'incompatibilité dasn la table sqlite"
    return "nabm" + str(nabm_version)

def get_nabm_csv_name():
    return import_export_rep+"/" + "nabm" + str(nabm_version) +".csv" 

def get_incompatibility_csv_name():
    return import_export_rep+"/" + "incompatible_codes" + str(nabm_version) +".csv"                            

separator = ";"

def _test():
    """Execute doctests."""
    import doctest
    doctest.testmod(verbose=True)

def set_nabm_version(val):
    """Indiquer au système la version de NABM sur laquelle on travaille.
num : numéro sur 1 à 3 chiffres.
    >>> set_nabm_version(49)"""
    if not isinstance(val, int):
        return
    global nabm_version
    nabm_version = int(val)

def choose_nabm_version():
    "Demande la numéro de version de NABM sur laquelle on va travailler."
    print("nabm_version : ", nabm_version)
    rep = input("Indiquer la version de NABM sur laquelle vous voulez travailler(exemple : 49)")
    set_nabm_version(rep)
    print("Version de NABM : {}".format(nabm_version))
    
def describe_a_code(input_code = None):
    """Afficher la fiche d'un code"""
    if input_code is None :
        input_code = input("Code décrire (4 chiffres) : " )
    BASE = lib_nabm.Nabm()
    BASE.NABM_DB.quick_sql("Select * from nabm where code = '{}'".format(input_code), single_column = True)
    
def search_code_containing():
    """Rechercher une chaîne dans la NABM"""
    input_string = input("Saisir une chaîne à chercher dans le libellé (non sensible à la case) : ")
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

def creer_fichier_csv_incompatibilites(path_to_file, path_to_output):
    """Création du CSV des incompatibilités de la NABM.
    Ce fichier est créé pour être intégré dans la base sqlite."""
    print("NABM file {}".format(path_to_file))
    ws = pd.read_excel(path_to_file)
    # ws = wb.parse(sheet_name = 0)
    incomp = ws[ws['CODES INCOMPATIBLES'].notnull()] [['CODE', 'CODES INCOMPATIBLES']]
    la_liste = incomp.values.tolist()
    def formater(x, y ):
        return to4digits(x) + separator + to4digits(y) +"\n"

    with open(path_to_output,"w") as f:
        f.write("code" + separator + "incompatible_code\n")
        for line in la_liste:
            code = line[0]
            incompatibles_codes = line[1]
            if isinstance(line[1], int):
                f.write(formater(code, incompatibles_codes))
            else:
                for item in incompatibles_codes.split("-"):
                    f.write(formater(code, item))

                    
def creer_fichier_csv_nabm(data_in, data_out, separator = ";"):
    """Création du CSV de la NABM à partir du fichier NABM.
Ce fichier est créé pour être intégré dans la base sqlite.

     separator : separator for csv import and export.
"""
 
    def to_int(x):
        """Force x to integer or 0 if null"""
        return x if x else 0

    # on importe une première fois : 
    wb  =  pd.read_excel(data_in)
    dicto = {col : to_int for col in wb.columns if wb[col].dtypes == 'float64'}

    # seconde importation : 
    wb2 =pd.read_excel(data_in, converters= dicto)
    wb3 = wb2[wb2.columns[:-1]].copy()
    wb3['CODE'] = wb3['CODE'].apply(to4digits)
    
    wb3.to_csv(data_out, sep = separator, index = False, encoding = "UTF-8")

def _creer_fichier_csv_nabm():
    """Lance la création du fichier CSV de la NABM."""

    path_to_file= get_fullname_to_excel_file()
    path_to_output = get_nabm_csv_name()

    print("\nCréation du fichier NABM")
    print("Fichier d'entrée : {}".format(path_to_file))
    print("Fichier de sortie : {}".format(path_to_output))
    creer_fichier_csv_nabm(path_to_file, path_to_output)

def _creer_fichier_csv_incomp():
    """Lance la création du fichier CSV des incompatibilités"""

    path_to_file= get_fullname_to_excel_file()
    
    path_to_output = get_incompatibility_csv_name()
    print("\nCréation du fichier des incompatibilités")
    print("Fichier d'entrée : {}".format(path_to_file))
    print("Fichier de sortie : {}".format(path_to_output))
    creer_fichier_csv_incompatibilites(path_to_file, path_to_output)

        
def vider_table (table_name=None):
    "Vider une table sqlite."
    if table_name is None:
        table_name = get_incompatibility_table_name()
    BASE = lib_nabm.Nabm()
    BASE.NABM_DB.quick_sql("DROP TABLE IF EXISTS {}".format(table_name))
    
def creer_table_inc(table_name = None):
    if table_name is None:
        table_name=get_incompatibility_table_name()
    sql ="""
CREATE TABLE IF NOT EXISTS {} (
 code TEXT,
 incompatible_code TEXT)
 """.format(table_name)
    BASE = lib_nabm.Nabm()
    BASE.NABM_DB.quick_sql(sql)

def creer_table_nabm(table_name = None):
    if table_name is None:
        table_name=get_nabm_table_name()
    sql ="""
CREATE TABLE IF NOT EXISTS {} (
 code TEXT PRIMARY KEY,
 chapitre INTEGER,
 sous_chapitre INTEGER,
 coef INTEGER,
 date_creation TEXT,
 libelle TEXT,
 entente INTEGER,
 remb100 INTEGER,
 maxcode INTEGER,
 regl_spec INTEGER,
 refmed INTEGER,
 acte_res INTEGER, 
 inibio INTEGER,
 tech INTEGER,
 RMO INTEGER,
 sang INTEGER,
 date_effet TEXT
 )
 """.format(table_name)

    # Ci dessus je pourrai plus tard introduire  deux champs
    # ,  lettre char(3)
    # , rem TEXT   
    BASE = lib_nabm.Nabm()
    BASE.NABM_DB.quick_sql(sql)

"""
Dans le sqlite j'ai :
cid | name | type | notnull | dflt_value | pk | 
0 | code | TEXT | 1 | '0' | 1 | 
1 | chapitre | int(11) | 0 | NULL | 0 | 
2 | sous_chapitre | int(11) | 0 | NULL | 0 | 
3 | lettre | char(3) | 0 | NULL | 0 |      ****************
4 | coef | int(11) | 0 | NULL | 0 | 
5 | date_creation | date | 0 | NULL | 0 | 
6 | libelle | varchar(255) | 0 | NULL | 0 | 
7 | entente | tinyint(1) | 0 | NULL | 0 | 
8 | Remb100 | tinyint(1) | 0 | NULL | 0 | 
9 | MaxCode | int(11) | 1 | '0' | 0 | 
10 | ReglSpec | char(2) | 1 | '' | 0 | 
11 | RefMed | int(11) | 0 | '0' | 0 | 
12 | Reserve | tinyint(1) | 0 | NULL | 0 | 
13 | IniBio | tinyint(1) | 0 | NULL | 0 | 
14 | Tech | int(11) | 0 | '0' | 0 | 
15 | RMO | smallint(1) | 0 | NULL | 0 | 
16 | Sang | tinyint(1) | 0 | NULL | 0 | 
17 | DateEffet | date | 0 | NULL | 0 | 
18 | Rem | text | 0 | None | 0 |         ********************

On va déplacer les 2 codes en trop en fin de table. PLus tard, je ferai une seconde table
de remarques sur les codes ss.

Nom dans la table NABM du fichier Excel :

['CODE',
 'CHAPITRE',
 'SOUS-CHAPITRE',
 'COEFFICIENT B',
 'DATE CREATION',
 'LIBELLE',
 'ENTENTE PREALABLE',
 'REMBOURSEMENT 100%',
 'NBR MAXI DE CODE',
 'N° REGLE SPECIFIQUE',
 'REF INDICATION MEDICALE',
 'ACTES RESERVES',
 'INITIATIVE BIOLOGISTE',
 'CONTINGENCE TECHNIQUE',
 'R.M.O.',
 'EXAMEN SANGUIN',
 'DERNIERE DATE EFFET']
"""

def load_csv(csv_file, table_name):
    "Charge un CSV dans une table."
    FILE = open(csv_file, "r")
    reader = csv.reader(FILE, delimiter = separator)

    to_db = [line for line in reader]
    
    BASE = lib_nabm.Nabm()
    BASE.NABM_DB.con.executemany("INSERT INTO {} ('code', 'incompatible_code') VALUES (?, ?) ; ".format(table_name), to_db[1:])
    BASE.NABM_DB.con.commit()
    BASE.NABM_DB.con.close()

def load_csv_many_columns(csv_file, table_name):
    """Charge CSV de la NABM dans la table NABM. Contient N = 17 champs."""

    # you must create a N long chain of question marks.
    N = 17 
    sql_string = "INSERT INTO {} VALUES (" + ", ".join(["?"] * N)+") ; "

    FILE = open(csv_file, "r")
    reader = csv.reader(FILE, delimiter = separator)
    to_db = [line for line in reader]
    
    BASE = lib_nabm.Nabm()
    # explanation : to_db[1:] : will skip first column (= header)
    BASE.NABM_DB.con.executemany(sql_string.format(table_name), to_db[1:])
    BASE.NABM_DB.con.commit()
    BASE.NABM_DB.con.close()   
    
def load_csv_inc():
    "Charge le CSV des incompatibilités dans la table sqlite."
    load_csv(get_incompatibility_csv_name(), get_incompatibility_table_name())

def load_csv_nabm():
    "Charge le CSV de la NBAM dans la table Sqlite."
    load_csv_many_columns(get_nabm_csv_name(), get_nabm_table_name())

def voir_structure(table):
    "Affiche une structure de table de sqlite."
    BASE = lib_nabm.Nabm()
    BASE.NABM_DB.quick_sql("PRAGMA table_info({})".format(table))
    
def voir_structure_inc():
    "Structure de la table des incompatibilités."
    voir_structure(get_incompatibility_table_name())

def voir_structure_nabm():
    "Structure de la table de la nabm."
    voir_structure(get_nabm_table_name())

def quitter():
    "Quit"
    print("OK, Quitter")
    
    
def traitement_complet_nabm(num_nabm):
    """A partir d'un numéro de nabm, créer les fichiers csv et les importer
dans la base sqlite."""
    # indiquer la version de NABM :
    set_nabm_version(num_nabm)
    
    # créer les 2 fichiers CSV
    path_to_file = get_fullname_to_excel_file()
    creer_fichier_csv_nabm(path_to_file, get_nabm_csv_name())
    creer_fichier_csv_incompatibilites(path_to_file, get_incompatibility_csv_name())
    
    # Créer les 2 tables dans la base sqlite
    creer_table_nabm()
    creer_table_inc()
    
    # intégrer les 2 fichiers CSV dans les tables.
    load_csv_nabm()
    load_csv_inc()

def nothing():
    pass

class Menu():
    """Un petit menu pour gérer quelques paramètres"""
    lst_menu = [
        ["1", "Décrire un code", describe_a_code],
        ["V", "Indiquer la version de NABM", choose_nabm_version],
        ["C", "Chercher dans la description", search_code_containing],
        ["S", "Requete SQL", sql],
#         ["SN", "Changer de version de NABM", ask_set_nabm_version],
        ["L", "Liste des tables", list_tables],
        [" ", "", nothing],
        ["CNABM", "Créer Fichier CSV pour NABM", _creer_fichier_csv_nabm],
        ["CINC", "Créer Fichier CSV pour incompatibilité", _creer_fichier_csv_incomp],
        [" ", "", nothing],
        ["CIT","Créer table incompatibilités", creer_table_inc ],
        ["CNT", "Créer table NABM", creer_table_nabm], 
        ["LIT", "Charge CSV incompat dans table", load_csv_inc],
        ["LNT", "Charge CSV NABM dans table", load_csv_nabm],
        ["DIT", "Supprimer table incompat)", vider_table],
        [" ", "", nothing],      
        ["SIT", "Show structure table_incompat", voir_structure_inc],
        ["SNABM", "Show structure table_nabm", voir_structure_nabm],
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
