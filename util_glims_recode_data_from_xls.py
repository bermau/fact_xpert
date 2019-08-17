"""Utilisatire pour le module de facturation.

Permet de convertir une saisie excel verticale en ligne horizontal.

input ne permettant pas la saisie de multiples lignes, je suis
obligé d'écrire cette affreuse structure."""

import facturation

import pdb


STRUC="""
0126
0552
0563
0578
0584
0593
0999
1104
1127
1610
9001
9105
0999
9001
9005
9105

"""


def xls_column_to_py():
    "convert an excel column to a list" 

    item_lst = [ item for item in STRUC.split("\n") if item is not '' ]
    print()
    for item in item_lst:
        print(item, end=' ')

if __name__ == '__main__':
    
     xls_column_to_py()
    

