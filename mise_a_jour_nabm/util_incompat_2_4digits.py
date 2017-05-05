#!/bin/env python3
# -*- coding: utf-8 -*-
# file : util_incompat_2_4digits.py

"""Convertir des nombres en chaine de 4 caractères.

Le fichier provient de la l'utilisatire d'amazilia.
Le fichier est originelement nommé : couples_incompat.csv

Circonstances :
fichier commence par :
9001,9002
9001,9004
9004,9001
18,7886
18,7887
24,4127
40,41
41,40
901,902

la partie contenant

31,1254
2345,3453

est à convertir en :
0031,1254
2345,3453

la fonction à utiliser est dérivée de :
printf("%04d", id) # Sa syntaxe dans format est un peu différente.

"""

file_name = "import_nabm/couples_incompat.csv"
output_file_name = "import_nabm/couples_incompat_ok.csv"
def to4digits(num):
    """
    return a 4 digits formated number
    >>> to4digits(54)
    '0054'
    >>> to4digits('0054')
    '0054'
"""   
    return "{:04d}".format(int(num))


def _test():
    """Execute doctests."""
    import doctest
    doctest.testmod(verbose=True)

if __name__=='__main__':
    _test()
    
    output_lines = []
    # lecture
    with open(file_name, 'r') as f:
        a = f.readlines()

    # traitement    
    for ligne in  a:
        (a, b) = ligne.split(',') # DANGER ????
        output_lines.append((to4digits(a)+','+to4digits(b)+'\n'))

    # écriture
    with open(output_file_name, 'w') as out_f:
        out_f.writelines(output_lines)
        print("Converted file is now in : " + out_f.name)
    
