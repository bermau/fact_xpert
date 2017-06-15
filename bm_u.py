#!/bin/env/python3
# file : bm_u.py
# divers utilitaires

import datetime

def title(msg):
    "Print à title"
    print("*" * 30)
    print(msg)
    print("*" * 30)

def readkey(msg=''):
    print(msg)
    print("Touche... ")
    input()

def prt_lst(une_liste):
    """print a list in a human readable format."""
    for line in une_liste:
        print(line)

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

class Buffer():
    """Un buffer pour enregistrer des messages à écrire plus tard.

    >>> buf = Buffer()
    >>> buf.print(22, "poires")
    >>> buf.print(35, "abricots")
    >>> buf.show()
    22 poires
    35 abricots
    >>> buf2 = Buffer()
    >>> buf2.print("savons", "rien à voir", "de rien")
    >>> buf2.extend(["Line 1", "Line 2", "Line 3"])
    >>> buf.extend_buf(buf2)
    >>> buf.show()
    22 poires
    35 abricots
    savons rien à voir de rien
    Line 1
    Line 2
    Line 3

    
    """
    def __init__(self):
        """Le buffer est constitué d'une liste de lignes de texte."""
        self.msg_lst = []
    def write(self, msg):
        self.msg_lst.append(msg)
    def print(self, *args):
        self.msg_lst.append(" ".join([str(i) for i in args]))
    def extend(self, lst):
        """Etendre une buffer avec une liste."""
        self.msg_lst.extend(lst)
    def extend_buf(self, buf):
        """Etendre un buffer avec un autre Buffer"""
        self.msg_lst.extend(buf.msg_lst)
    def show(self):
        """Aficher le buffer"""
        for i in self.msg_lst:
            print(i)
def get_version():
    """Return version of this programm"""
    # cf facturation.print_version_and_date()
    
    
def _test():
    """Execute doctests."""
    import doctest
    (failures, tests) = doctest.testmod(verbose=True)
    print("{} tests performed, {} failed.".format(tests, failures))
    
if __name__=='__main__':
    _test()   

    
