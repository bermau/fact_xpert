
"""Expertise par IEP sur Synergy.

Ce module présente une fonction de démonstration demo()

et une fonction de saisie manuelle de EP et date."""

import  syn_odbc_connexion
from syn_odbc_connexion import Syn


def demo():
    """Démonstration."""
    syn_odbc_connexion.CONNEXION = syn_odbc_connexion.MyODBC_to_infocentre()
    Syn().fac_de_IEP_date(IEP='1178170', date= '27/06/2016') # false data 
    del(syn_odbc_connexion.CONNEXION)

def saisie_manuelle():
    """Demande l'IEP et la date puis lance l'expertise."""
    print("""
Saisir L'IEP puis la date des actes au format français (ex. 21/01/2015)

Utiliser Ctrl-C pour arrêter ce programme.
""")
    IEP = input("IEP = ")
    date = input("Date : ")

    syn_odbc_connexion.CONNEXION = syn_odbc_connexion.MyODBC_to_infocentre()
    Syn().fac_de_IEP_date(IEP=IEP, date=date)                
    del(syn_odbc_connexion.CONNEXION)                 

if __name__ == '__main__':
    # demo()
    saisie_manuelle()
