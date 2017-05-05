#!/bin/env python3
# -*- coding: utf-8 -*-
"""Calcul du nom de sortie d'un fichier."""

import os.path
def get_ouput_file_name(file, modif):
    """
    >>> get_ouput_file_name('mon fichier.csv', '.xls')
    'mon fichier.xls'
    >>> get_ouput_file_name('mon fichier.csv', '_ok')
    'mon fichier_ok.csv'
    
"""
    (basename, extension) = os.path.splitext(file)
    # print(basename, extension)
    if modif.startswith('.'):
        # remplacer l'extension
        return basename+modif
    else:
        # insérer modif avant l'extension
        return basename+modif+extension

def _test():
    """Execute doctests."""
    import doctest
    doctest.testmod(verbose=True)

if __name__=='__main__':
    _test()
    
