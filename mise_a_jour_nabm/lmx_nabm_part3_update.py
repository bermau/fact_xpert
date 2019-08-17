"""Etpae 3 de l'importation de la NABM.

mis au point lors de la NABM 45 """


# Essai de connexion à une base mysql depuis python3 
# en utilisant le paquet python3-mysql-connector
# En 2016 sur Debian8.1, j'ai simplement installé le paquet python3-mysql-connector
# et suivi la page :
# http://apprendre-python.com/page-database-data-base-donnees-query-sql-mysql-postgre-sqlite

import mysql.connector 

from conf_file_amz import *
import os, sys

DEBUG = False  # False, ou 1 (bavard) , ou 2 (très bavard)

# importer les librairies de fact_xpert.
sys.path.append(FACT_XPERT_REP)
import lib_sqlite
from bm_u import title

# Numéro de la prochaine version de la nabm
NABM_NEXT_VERSION = 45

def guess_col_name_from_year(year):
    """Return column name from year. Example :
    >>> guess_col_name_from_year(2011)
    'y1'
    >>> guess_col_name_from_year(2009 )
    'y9'
    >>> guess_col_name_from_year(2000)
    'y10'
    >>> guess_col_name_from_year(2010)
    'y10'
"""
    year=str(year)
    digit=str(year[-1])
    if digit=='0':
        digit='10'
    name='y'+digit
    return name

class ConnMysql(object):
    def __init__(self):
        self.conn = mysql.connector.connect(host=HOST,user=USER,
                                   password=PASSWORD,
                                   database=DATABASE)
        self.cursor=self.conn.cursor()

    def sendSelect(self,req):
        self.cursor.execute(req)
        rows = self.cursor.fetchall()
        if len(rows):               
            for row in rows:
                for col in row :
                    print(str(col)+'|',end='')
                print()
            return True
        else:
            return False
    def testSelect(self, req, result):
        """Effectue une requete Sql et vérifie le résultat"""
        self.cursor.execute(req)
        reponse = self.cursor.fetchone()[0]
        print("DANS test SELECT")
        print(req)
        print(reponse)       
        if reponse == result:
            return True
        else:
            return False
        
    def testAct(self, table,  act, expected):
        """Effectue une requete Sql et vérifie le résultat"""
        if DEBUG: print("DANS testAct")
        req = "SELECT coef FROM {} WHERE id = %s LIMIT 1".format(table)
        if DEBUG: print(req)
        self.cursor.execute(req, (act,))
        reponse = self.cursor.fetchone()

        if reponse == None:
            if expected == None:
                return True
            else:
                return False # Cas mal programmé
        else:
            return reponse[0] == expected
        
    def sendUpdate(self,req):
        if DEBUG :
            print("La requête sera ")
            print(req)
        self.cursor.execute(req)       
    
    def afficherCodesAMettreAJour(self,annee):
        title("Affichons les  30 premiers codes à mettre à jour pour {}".format(annee))
        self.sendSelect("""
select *
FROM tests_per_year
LEFT JOIN activity_{year}
ON tests_per_year.lms_code=activity_{year}.code
LIMIT 30
    """.format(year=annee,))

    def updateCodesExistants(self,annee, colonne):
        title("Mise à jour des codes existants")
        # Mise à jour des codes existants
        self.sendUpdate("""UPDATE
 tests_per_year
 LEFT JOIN activity_{the_year}
ON tests_per_year.lms_code=activity_{the_year}.code
SET tests_per_year.{the_column}=activity_{the_year}.nb
""".format(the_year=annee,the_column=colonne))
     
    def afficherNouveauxCodes(self):
        title("Affichons maintenant les nouveaux codes")
        self.sendSelect("""
        Select description,code, y1, y2, y3, y4, A.nb, y6, y7, y8, y9, y10
        FROM activity_2015 AS A LEFT JOIN tests_per_year
        ON A.code=tests_per_year.lms_code
        WHERE tests_per_year.lms_code IS NULL
""")        
    def updateNouveauxCodes(self):
        self.sendUpdate("""
        INSERT INTO  tests_per_year ( description, lms_code, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10)
        (SELECT description,code, y1, y2, y3, y4, activity_2015.nb, y6, y7, y8, y9, y10 FROM
        activity_2015 LEFT JOIN tests_per_year
        ON activity_2015.code=tests_per_year.lms_code
        WHERE tests_per_year.lms_code IS NULL)
        """)
    def copy_table_next_to_XX(table_name, XX):
        """Copie la une table de type nabm_next dans nabm_XX"""
        pass
        sql = "SELECT * FROM {table} WHERE code =  "

def max_key_of_dict(dico):
    """return the highest key of a dict.

    >>> max_key_of_dict({32 : "", 42 : "tutu"})
    42
    >>> max_key_of_dict({42 : "", 33 : "tutu"})
    42
    
    """
    return max([ int(key) for key in dico.keys() ])


class Nabm_verifier():
    """Usefull tool to verify NABM version."""
    nabm_tests = { # Dans cette structure : 'tests ':[ code, résultat, commentaire ]
       # 42 : la leptospirose disparait 
       42 : { 'tests' : [[1312, None, "SD Leptospose éliminée"],
             #        l'acte 1253 vaut B90
                      [1253, 90, ""],
                      [1208, 31, "TSH"]
                      ],
            'date' : "01/09/2014" # date d'application (None si inconnue)          
           },
       43 : { 'tests' : [[1208, 30, "TSH a baissé"]], 
             'date' : "20/04/2016"
           },
       44 : {'tests' : [[9914, 14, ""],  # création d'un B14 pour minima
             [9915, 15, ""],
             [2002, None, "Pas de Saturation de la sidérophiline"],
             ],
             'date' : "01/04/2017"
             },
       45 : { 'tests' : [[2002, 17,"Création Saturation sidérophiline"],],
              'date' : "13/07/2017" 
            }
        }
    lst_nabm_tables =  [
                        'nabm42', # table et sa version voulue
                        'nabm43',
                        #'nabm44',
                        #'nabm45',
                        'nabm_next',
                        'nabm_prev',
                        'nabm',
                 ]

    def guess_nabm_version(self, table, comment = ''):
        """try to guess the version of a NABM database.

        return NABM version"""
        sql = ''
        C = ConnMysql()
        test = None
        title("Testing table {}\n   Comment : {}.".format(table, comment))
        
        reponses = {}

        for i in [ key for key in sorted(Nabm_verifier.nabm_tests.keys()) ]:
            if DEBUG : print("teste la possibilité de version", i)
            tests_vers = True
            for (act, expected, comment) in Nabm_verifier.nabm_tests[i]['tests']:
                unit_test_vers = None
                if DEBUG > 1 : print("La question portera sur l'acte {} \
    et la réponse attendue est : {} \nCe test concerne : {}".format(act,expected, comment))
                if C.testAct(table, act, expected ):
                    if DEBUG > 1 :  print("Réponse : True") 
                    unit_test_vers = True
                else:
                    if DEBUG > 1 :  print("Réponse : False")
                    unit_test_vers = False
                tests_vers = tests_vers and unit_test_vers
                if DEBUG > 1 :  print()
            reponses[i] = tests_vers
           
        if DEBUG > 1 : print("Réponses pour la table : ", reponses)

        max_key = max([ key  for (key, rep) in reponses.items() if rep == True ])
        if DEBUG  : print (" * * * * * * * La version maximale probable est : ", max_key)
        return max_key
    
    def guess_version_of_all_nabm_table(self):
        """guess version a of all availale NABM tables."""
        for table in self.lst_nabm_tables:
            print(self.guess_nabm_version(table))
            
        
    def verify_all_nabm_tables(self):
        """Select all nabm versions and verify their version."""
        lst  =  [['nabm42', 42],
                 ['nabm43', 43],
                #['nabm44', 44],
                #['nabm45', 45],
                #['nabm46', 46],
                 ]
        for table, vers in lst:
            if self.guess_nabm_version(table) != vers:
                print("Table {} seems not to be version {}".format(table, vers))
            
def _demo_verif_nabm_version():
    C = Nabm_verifier()
    print(C.guess_nabm_version("nabm42", comment = "Assurément une 42"))   
    print(C.guess_nabm_version("nabm", comment = "Probablement une 43"))
    print(C.guess_nabm_version("nabm_next", comment = "Version 45 à installer"))


def adjust_nabm_version():
    global NABM_NEXT_VERSION 
    print("La prochaine de version de NABM prévue est : {}".format(NABM_NEXT_VERSION))
    version = input('next version ? :')
    try :
        if int(version) >= NABM_NEXT_VERSION:
            NABM_NEXT_VERSION=version
        else :
            print("Par securité, impossible de diminuer le numéro de version.")
            import sys
            sys.exist()
    except:
        pass
    print("NABM_NEXT_VERSION : ", NABM_NEXT_VERSION)

    
def _test():
    import doctest
    doctest.testmod(verbose = False )
    
if __name__ == '__main__':
    _test()
    print("Version de la prochaine nabm : {} ".format(NABM_NEXT_VERSION))
    DEBUG = False  #  False, ou 1 (bavard) , ou 2 (très bavard)
    _demo_verif_nabm_version()
    # adjust_nabm_version()
    
    print("La suite")

    Nabm_verifier().verify_all_nabm_tables()
    Nabm_verifier().guess_version_of_all_nabm_table()

    
    import sys
    sys.exit()


    C = ConnMysql()
    C.copy_table_next_to_XX()    
    # C.cursor.close()
              
    
##    annee = '2015'
##    colonne = guess_col_name_from_year(annee)
##    print("La colonne a étudier est {}".format(colonne))


    
    # C.afficherCodesAMettreAJour(annee)

