# -*- coding: utf-8 -*-
"""Enregistrement des expertises de facturation dans une base.

Le but est d'enregistrer les résultats d'une expertise dans une base de
données sqlite.
Ce module comprend :
la déclaration de la structure de la base
Un outil pour créer la base.
Un outil pour enregistrer le résultat d'une expertise de facturation. 

"""

import sqlite3
import os
import lib_sqlite

class Glob:
    """Espace de noms pour les variables et fonctions <pseudo-globales>"""

    DB_FILE="PRIVATE/result.sqlite"
# Structure de la base de données.

    dicoTables={"rep":[
('id', "k", "clé primaire"),
('cle', 50, "Nom du Ctrl"), 
('date', 10, "Date expertise"),
('sum',4, "Somme" ),
('glob',4,"Réponse globale"),
('nabm', 4, "nabm"),
('repet', 4, "répétitions"),
('sang',4,"sang"),
('hep_b',4,"hep_b"),
('prot',4,"prot"),
('mont',4,"montant en erreur"),
('incomp',4,"Incompatibilité"),
('cotamin',4, 'Cotation minimale indue')
]
}


class DataRecorder(lib_sqlite.GestionBD):
    """"A module to record data in an Sqlite Database"""
    
    def __init__(self, db_name):
        "Établissement de la connexion et création du curseur"
        self.con = sqlite3.connect(db_name)
        
    def createTables(self, dicTables):
        "Création des tables"
        for table in dicTables:            # parcours des clés du dictionn.
            req = "CREATE TABLE %s (" % table
            pk =''
            for descr in dicTables[table]:
                nomChamp = descr[0]        # libellé du champ à créer
                tch = descr[1]             # type de champ à créer
                if tch =='i':
                    typeChamp ='INTEGER'
                elif tch =='r':
                    typeChamp ='REAL'
                elif tch =='k':
                    # champ 'clé primaire' (entier incrémenté automatiquement)
                    #typeChamp ='SERIAL'
                    typeChamp ='INTEGER NOT NULL'
                    pk = nomChamp
                else:
                    typeChamp ='VARCHAR(%s)' % tch
                req = req + "%s %s, " % (nomChamp, typeChamp)
            if pk == '':
                req = req[:-2] + ")"
            else:
                req = req + "CONSTRAINT %s_pk PRIMARY KEY(%s))" % (pk, pk)
            self.con.execute(req)
            print ("Fin de la création des tables")

    def dropTables(self, dicTables):
        "Suppression de toutes les tables décrites dans <dicTables>"
        for table in list(dicTables.keys()):
            req ="DROP TABLE %s" % table
            self.con.execute(req)
        self.con.commit()                       # transfert -> disque
        print ("Fin de la destruction des tables")

    def prt_sql_with_header(self,  sql, sep='\t'):
        """print the result of an SQL request, with columns name"""
        self.con.row_factory = sqlite3.Row # et non pas Row()
        c = self.con.cursor()
        c.execute(sql)
        for i, row in enumerate(c.fetchall()):
            if i == 0:
                print('\t'.join(row.keys()))
            print('\t'.join([str(item) for item in row]))

    def record_expertise(self, data):
        """enregistre le résultat d'une expertise de facturation.

data est un dictionnaire"""
##        if len(data) == 2 : 
##            sql = """INSERT INTO rep (cle, date, glob)
##                         VALUES(:cle ,CURRENT_TIMESTAMP, :glob)"""
##        else:
        sql = """INSERT INTO rep (cle, date, glob, sum, nabm,
                                  repet, sang, hep_b, prot, mont, incomp, cotamin)
                         VALUES(:cle ,CURRENT_TIMESTAMP, :glob, :sum, :nabm,
                         :repet, :sang,
                                :hep_b, :prot, :mont, :incomp, :cotamin)"""
        
        self.con.execute(sql, data)
      

    def show_rep(self):
        "print the content of te database"
        self.prt_sql_with_header(sql="select * from rep")        

    def close(self):
        "close database"
        self.con.commit()

def connect_db():
    "test la connexion"
    DR = DataRecorder(db_name=Glob.DB_FILE)
    DR.con.execute("Select 1,2,3 ;")
    # DR.con.close()
    
def quick_init():
    """permet de créer la base et la table de novo"""
    A= DataRecorder(db_name=Glob.DB_FILE)
    try:
        A.dropTables(Glob.dicoTables)
    except:
        pass
    A.createTables(Glob.dicoTables)
    A.close()

def sql_fn():
    "console Sql pour lancer quelques ordres"
    DR = DataRecorder(db_name=Glob.DB_FILE)
    sql = input("Sql : ")
    DR.prt_sql_with_header(sql)
    DR.close()
    
def help_fn():
    """Affichage de l'aide"""
    print(help(__name__))



def menu():
    """Un petit menu textuel avec quelques ordres pour gérer la base"""
    
    def my_quit_fn():
        raise SystemExit
    def fn_record_expertise():
        DR = DataRecorder(db_name=Glob.DB_FILE)
        data = (False, {'nabm': True, 'mont': True,
                        'repet': False, 'prot': False,
                        'hep_b': True, 'incomp': True,
                        'sang': 3})
        data0=data[0]
        data1=data[1]
        data1['glob']=data[0]
       
        DR.record_expertise(data1)
        DR.close()
        
    def fn_truncate_rep():
        """Vide la table rep"""
        DR = DataRecorder(db_name=Glob.DB_FILE)
        DR.con.execute("delete from rep")
        DR.commit()  
        
    def show_rep():
        DR = DataRecorder(db_name=Glob.DB_FILE)
        DR.show_rep()
        
    menu = {
        "01a":("Connection à la base (test de ...)", connect_db), 
        "02":("Quick Init",quick_init),
        "04":("Enter SQL",sql_fn),
        "05":("Demo : insert a record", fn_record_expertise),
        "06":("Demo : show rep", show_rep),
        "07":("Erase all data from rep", fn_truncate_rep),
        "08":("Help",help_fn),
        "09":("", my_quit_fn),
        "10":("Quit",my_quit_fn)
           }
    def invalid():
        print("\nChoix invalide !!!\n")       
    
    while True:
        print()
        for key in sorted(menu.keys()):
            print( key+" : " + menu[key][0])
        print()
        ans = input("Make A Choice : ")
        menu.get(ans,[None,invalid])[1]()
    
if __name__ == '__main__':

    DR = DataRecorder(db_name=Glob.DB_FILE)
    menu()



 
