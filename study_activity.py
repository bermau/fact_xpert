#!/bin/env python3
# -*- coding: utf-8 -*-
# file : study_activity.py


"""Incidence de la nabm sur l'activité.

On dispose des différentes nabm.
On dispose d'une activié de facturé de référence (dans acti.sqlite).

Quelle est la variation de la facturation selon la NABM appliquée ?

"""

import sys, os, sqlite3
import conf_file as Cf
import bm_u
import csv

# ACTI_DB = '/home/bertrand/Bureau/PB_0008_activité_en_baisse_nomenclature/acti.sqlite'
ACTI_DB = 'acti.sqlite'

NABM_DB = 'nabm_db.sqlite'

VERSION = str(44) 

def prt_sql_with_header(CON, sql, sep='\t'):
    CON.row_factory = sqlite3.Row # et non pas Row()
    c = CON.cursor()
    c.execute(sql)
    for i, row in enumerate(c.fetchall()):
        if i == 0:
            print('\t'.join(row.keys()))
        print('\t'.join([str(item) for item in row]))


def _test():
    """Execute doctests."""
    import doctest
    doctest.testmod(verbose=True)

if __name__=='__main__':
    # _test()

    con = sqlite3.connect(NABM_DB)
        
    # con.execute("attach database {db_file} as inv".format(db_file=ACTI_DB))
    con.execute("attach database 'acti.sqlite' as acti")
    # Quelques data pour acti_2016
    print(); print()
    for row in con.execute("PRAGMA table_info(acti_2016)"):
        print(row[1], end=' ')
    print()
    for row in con.execute("Select * from acti.acti_2016 limit 3"):
        print(row)
    # Quelques data pour nabm44
    print(); print()
    for row in con.execute("PRAGMA table_info(nabm44)"):
        print(row[1], end=' ')
    print()
    for row in con.execute("Select * from nabm44 limit 3"):
        print(row)
    print(); print()
    # Quelques donnée de jointures :
    sql_str="""
            SELECT
                acti_2016.code
                , mnemo
                , shortname
                , total
                , nabm42.coef
                , total * nabm42.coef
                , SUM(total * nabm42.coef)
                , nabm43.coef
                , total * nabm43.coef
                , SUM(total * nabm43.coef) AS 'Nabm 43'
                , nabm44.coef
                , total * nabm44.coef
                , SUM(total * nabm44.coef) AS 'Nabm 44'


            FROM acti_2016
                        LEFT JOIN nabm42
            ON acti_2016.code = nabm42.code

                        LEFT JOIN nabm43
            ON acti_2016.code = nabm43.code

                        LEFT JOIN nabm44
            ON acti_2016.code = nabm44.code

            """
    prt_sql_with_header(con, sql_str)
    
