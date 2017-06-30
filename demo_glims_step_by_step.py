#!/bin/env python3
"""Extraire des structures d'un tableau régulier.

Le cas est adapté pour des données venant de la facturation du logiciel Glims
de MIPS. 

Extraction de champs de longueur fixe"""


import lib_glims as gl
import data_for_tests
import facturation
from bm_u import readkey, prt_lst, title

def _test():
    """Execute doctests."""
    import doctest
    (failures, tests) = doctest.testmod(verbose=True)
    print("{} tests performed, {} failed.".format(tests, failures))

if __name__ == "__main__":
    _test()
    title("Extraction pas-à-pas")
    print("Données originales par copier/coller depuis Glims:\n\n")
    data = data_for_tests.GLIMS_01_MOD_XX
    print(data)

    readkey("Délimitation des lignes utiles... ")
    cleaned_data = gl.delimite_format(data)
    prt_lst(cleaned_data)

    readkey("Extraction des champs...")    
    a = gl.Splitter(data_for_tests.GLIMS_01_MOD_XX_corr, gl.seps_GLIMS)
    ar_strings = a.get_fields()
    print(ar_strings)

    readkey("Passage au fomat accepté par fact_xpert")    
    MOD02_fact_xpert_format = gl.glims_to_MOD02_format(ar_strings)
    print("Passage au fomat accepté par factxpert")
    print(MOD02_fact_xpert_format)
    
    readkey("Lancement de la facturation")
    print()
    facturation.model_etude_1(MOD02_fact_xpert_format, model_type='MOD02')



    title("On va maintenant lancer une expertise sur une facture avec erreurs...")
