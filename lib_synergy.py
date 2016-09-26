
"""Utilisatires pour Synergy"""

def verif_IPP(valeur):
    """retourne une chaine IPP pour synergy.

Admet un nombre une chaine et retourne une chaine de longueur de 20 car.
    >>> verif_IPP('0000000001369119')
    '00000000000001369119'
    >>> verif_IPP(1369119)
    '00000000000001369119'
"""
    return str(valeur).rjust(20,'0')


    
def _test():
    """Execute doctests."""
    import doctest
    (failures, tests) = doctest.testmod(verbose=False)
    print("{} tests performed, {} failed.".format(tests, failures))


if __name__=='__main__':
    _test()   
