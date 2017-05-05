#!/bin/env python3
"""Une démonstration pour Didier !

Ceci est une explication.
"""

# import pyodbc
##import conf_file as Cf
##import bm_u 
##import lib_nabm # utilitaires pour la NABM
##import facturation
import datetime, sys
##import lib_smart_stdout
##import lib_synergy # utilitaires pour Synergy
##

def le_lendemain(jour_fr_str):
    """Retourne le jour suivant d'un jour en français
    >>> le_lendemain('28/02/2015')
    '01/03/2015'
    >>> le_lendemain('31/01/2015')
    '01/02/2015'
    >>> le_lendemain('24/12/2015')
    '25/12/2015'
    """
 
    annee = int(jour_fr_str[6:10]) # On convertit la chaine de caractère en integer   
    mois = int(jour_fr_str[3:5])
    jour = int(jour_fr_str[0:2])
         
    jour = datetime.datetime(annee, mois, jour)
    duree_de_un_jour = datetime.timedelta(1) # la durée d'une journée
    demain = jour + duree_de_un_jour
    
    return demain.date().strftime('%d/%m/%Y')

def _test():
    """Execute doctests."""
    import doctest
    (failures, tests) = doctest.testmod(verbose=True)
    print("{} tests performed, {} failed.".format(tests, failures))
    

if __name__ == '__main__':
    _test()
    print(le_lendemain('27/03/2017'))
    
