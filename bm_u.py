#!/bin/env/python3
# file : bm_u.py
# divers utilitaires

import datetime

def title(msg):
    print("*" * 30)
    print(msg)
    print("*" * 30)

def date_is_fr(date):
    """Verifie qu'une date est au format français.

    >>> date_is_fr('31/12/1964')
    True
    >>> date_is_fr('31/13/1964')
    False
    
    """
    year = int(date[6:10]) # On convertit la chaine de caractère en integer   
    month = int(date[3:5])
    day = int(date[0:2])
    try:
        a= datetime.date(year, month, day)
        return True
    except:
        return False

def _test():
    """Execute doctests."""
    import doctest
    (failures, tests) = doctest.testmod(verbose=False)
    print("{} tests performed, {} failed.".format(tests, failures))
    
if __name__=='__main__':
    _test()   

    
