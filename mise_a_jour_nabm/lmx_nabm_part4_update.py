"""Etpae 4 de l'importation de la NABM.

Modification des constantes du fichier local.php
mis au point lors de la NABM 45 """

# J'ai utilisé du code venant de mon programme dict_corr
# j'ai mis ce code dans lib_file_editor

DEBUG = False  # False, ou 1 (bavard) , ou 2 (très bavard)
TO_VERSION = 43 # Version à installer

from conf_file_amz import *
from  lmx_nabm_part3_update import Nabm_verifier 

import os, sys

# importer les librairies de fact_xpert.
sys.path.append(FACT_XPERT_REP)

from bm_u import title, prt_lst, readkey
import lib_file_editor as Fe

def doctest_sandbox(a, b):
    """
    >> doctest_sandbox( 1,  2)
    [1,    2]
    >> doctest_sandbox( 5,  4) # doctest: +NORMALIZE_WHITESPACE
    [5,    4]
    >> doctest_sandbox( 1,  4) # doctest: +NORMALIZE_WHITESPACE
    [1,    4,]
    """
    return [a, b] 

def get_modifications_of_nabm_names(vers = TO_VERSION):
    """return the changes to be reported in local.php 
    >>> get_modifications_of_nabm_names(43) == [ \
             ['NABM_ACTUAL_VERSION',  'NABM 43 app. 20/04/2016'], \
             ['NABM_PREV_VERSION', 'NABM 42 app. 01/09/2014'], \
             ['NABM_NEXT_VERSION', 'NABM 43 app. 20/04/2016']]
    True
"""
    lst = []
    nabm = Nabm_verifier().nabm_tests
    lst.append(['NABM_ACTUAL_VERSION', "NABM {} app. {}".format(vers, nabm[vers]['date'] )])
    lst.append(['NABM_PREV_VERSION', "NABM {} app. {}".format(vers-1, nabm[vers-1]['date'] )])
    lst.append(['NABM_NEXT_VERSION', "NABM {} app. {}".format(vers, nabm[vers]['date'] )])
    return lst

def _test():
    import doctest
    doctest.testmod(verbose = False )

if __name__ == '__main__':
    _test() 
   
    FILE = "/var/www/html/amazilia/test/library/local.php"
    # Déterminer les lignes à modifier.
    buts = get_modifications_of_nabm_names()
    prt_lst(buts)
    
    print("Voici le résumé des modifications qu'il faut \
apporter au fichier {}".format(FILE))
    print("\nVerifier la ligne ci-dessus, sinon Ctrl -C\n")
    if readkey("Confirmez par 'yes'  sinon Ctrl -C" ) != 'yes':
        print("abandon")
        sys.exit()
        
    # copier le fichier local.php par sécurité

    F = Fe.File_editor()
    F.open_file(FILE)
    F.backup_the_file
    
    for constante, definition in buts:
        formated_pattern = r"^define.?\(.?'" + constante + "'" + ".*"
        formated_new_string = "define('" + constante+"','" + definition +"');"
        print("formated_new_string", formated_new_string)
        print("Je recherche", constante + '  : ', end = '')
        occ = F.count_regex(formated_pattern)
        print("occurence = " , occ)
        if occ == 1:
            F.replace_regex(formated_pattern,  formated_new_string)

    print("Verify the end of this file...")
    prt_lst(F.tail(20))
    
    if readkey("Confirmez par 'yes'  sinon Ctrl -C" ) != 'yes':
        print("abandon")
    else:
        F.write_file(FILE)
    
