#!/bin/env python3
# -*- coding: utf-8 -*-

"""Implémentation d'une facture de NABM.
La facture est implémentée dans une base sqlite pour réaliser des requêtes
"""

import lib_sqlite
import sys

class Invoice():
    """Implémentation d'une facture de NABM.
"""
    STRUCT_MOD02 = """
invoice_list
(id INTEGER PRIMARY KEY,
record VARCHAR(10), 
code VARCHAR(4),
analyse VARCHAR(5),
nb_letters INTEGER,
letter VARCHAR(1)
)
"""
    def __init__(self, model_type):
        """Initie une implémentation de facture selon un modèle.
MOD01 : liste simple
MOD02 : liste évoluée. 
"""
        # Création de la base dans un fichier réel ou en RAM 
        # pour l'instant l'attachement d'une base RAM ne fonctionne pas.
        self.model_type = model_type
        self.INVOICE_DB = lib_sqlite.GestionBD('tempo.sqlite')
        # self.INVOICE_DB = lib_sqlite.GestionBD(in_memory=True)
        if not self.table_invoice_exists():
            # self.create_table_invoice_MOD02_in_database()
            self._force_creation_of_invoice_in_db()
        self.act_lst = [] # copy of data in database
        
    def create_view_for_nabm(self):
        """Tool to create a view.

Il peut existe plusierus tables notées nabmXX.
Il faut créer des vues nabmXX_view"""
        sql = """CREATE VIEW IF NOT EXISTS nabm_view AS
SELECT * from nabm ; """
        # pas terminé et sans doute à déplacer.
        
    def create_table_invoice_MOD01_in_database(self):
        sql = """CREATE TABLE IF NOT EXISTS invoice_list
(id INTEGER PRIMARY KEY, code VARCHAR(4))
"""
        # sys.stderr.write("sql = {}".format(sql))
        self.INVOICE_DB.execute_sql(sql)
        self.INVOICE_DB.commit() # QUESTION est-ce indispensable ?

    def create_table_invoice_MOD02_in_database(self):
        """Create a table for invoice.

Record is as following : [('5305051750', '1610', 'SIONO', 24, 'B') ... ]"""
        sql = "CREATE TABLE IF NOT EXISTS" + self.STRUCT_MOD02
        sys.stderr.write("Creation of invoice table in database.")
        sys.stderr.write("sql = {}".format(sql))
        self.INVOICE_DB.execute_sql(sql)
        self.INVOICE_DB.commit() # QUESTION est-ce indispensable ?

    def _force_creation_of_invoice_in_db(self):
        """Force creation of table invoice_list."""
        self.drop_table_invoice()
        sql = "CREATE TABLE " + self.STRUCT_MOD02
        sys.stderr.write("Creation of invoice table in database.")
        sys.stderr.write("sql = {}".format(sql))
        self.INVOICE_DB.execute_sql(sql)
        self.INVOICE_DB.commit() # QUESTION est-ce indispensable ?        
        
    def drop_table_invoice(self):
        self.INVOICE_DB.execute_sql("""DROP TABLE invoice_list""")
        
    def table_invoice_exists(self):
        """Test if table of invoices is defined."""
        return True
    
    def load_invoice_list(self, act_lst):
        """Load invoice data in database according to model type."""
        if self.model_type is 'MOD01':
            self.load_invoice_list_MOD01(act_lst)
        if self.model_type is 'MOD02':
            self.load_invoice_list_MOD02(act_lst)
    
    def load_invoice_list_MOD01(self, act_simple_list):
        """Constitue une table (id, acte_1), (id, acte2) ... """
        self.act_lst = act_simple_list
        self.INVOICE_DB.execute_sql("""DELETE FROM invoice_list""")
        for act in act_simple_list:
            self.INVOICE_DB.execute_sql("""INSERT INTO invoice_list
                                     (code) VALUES (?) """, (act,))
        self.INVOICE_DB.commit()

    def load_invoice_list_MOD02(self, act_lst):
        """Constitue une table (id, acte_1), (id, acte_2) ...
Adapté au modèle MOD02."""
        self.act_lst = [item[1] for item in act_lst]
        # sys.stderr.write("Loading data\n")
        self.INVOICE_DB.execute_sql("""DELETE FROM invoice_list""")
        for line in act_lst:
            print(str(line)+',')
            self.INVOICE_DB.execute_sql("""INSERT INTO invoice_list
                            (record, code, analyse, nb_letters, letter)
                             VALUES (?, ?, ?, ?, ?) """, line)
        self.INVOICE_DB.commit()
        
    def show_data(self):
        """Affiche les datas"""
        self.INVOICE_DB.quick_sql("SELECT * FROM invoice_list")
