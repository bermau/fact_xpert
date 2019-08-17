#!/bin/env python3
"""Démonstration de la facturation d'un dossier venant de Glims.

Le cas est adapté pour des données venant de la facturation du logiciel Glimps
de MIPS. """

if __name__ == "__main__":
    
    from lib_glims import Splitter, seps_GLIMS, glims_to_MOD02_format
    import data_for_tests
    import facturation
    
    
    ar_strings = []
    a = Splitter(data_for_tests.GLIMS_01_MOD2, seps_GLIMS)
    ar_strings = a.get_fields()
    format_MOD02 = glims_to_MOD02_format(ar_strings)


    facturation.model_etude_1(format_MOD02, model_type='MOD02')
    
