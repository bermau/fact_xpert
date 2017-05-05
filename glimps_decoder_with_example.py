#!/bin/env python3
"""Extraire des structures d'un tableau régulier.

Le cas est adapté pour des doonnées venant de la facturation du logiciel Glimps
de MIPS. 

Extraction de champs de longueur fixe"""

 


if __name__ == "__main__":
    import lib_glimps 
    import data_for_tests
    import facturation
    
    seps_GLIMS = [2, 9, 20, 54, 61, 67]
    
    a = lib_glimps.Spliter(data_for_tests.GLIMS_DIDIER, seps_GLIMS)
    ar_strings = a.get_fields()
    
    print()
    print("J'ai extrait les champs suivants :")
    print(ar_strings)
    
    # Examen des paramètres récupérés
    print()
    print("En voici une présentation plus structurée :")
    a.print_fields(ar_strings)

    # récupérer la facturation la plus simple (MOD01) et la traiter
    MOD01_fact_xpert_format = lib_glimps.glims_to_MOD01_format(ar_strings)
    
    facturation.model_etude_1(MOD01_fact_xpert_format)


    # récupérer la facturation élaborée et la traiter
    MOD02_fact_xpert_format = lib_glimps.glims_to_MOD02_format(ar_strings)
    print("Format élaboré (assez moche")
    print(MOD02_fact_xpert_format)

    facturation.model_etude_1(MOD02_fact_xpert_format, model_type='MOD02')
    
