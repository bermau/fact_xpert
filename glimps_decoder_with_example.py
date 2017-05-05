#!/bin/env python3
"""Extraire des structures d'un tableau régulier.

Le cas est adapté pour des doonnées venant de la facturation du logiciel Glimps
de MIPS. 

Extraction de champs de longueur fixe"""
 
struct = """
AAA 123 Ceci est le libellé 234.5
ALO 345 Ceci est une autre  124.5
"""

seps = [0, 5, 8, 28 ]

class Spliter():
    """Split a text as the Unix cut function
    >>> seps = [0, 4, 8, 28 ]
    >>> a = Spliter(struct, seps)
    >>> a.get_fields()
    [['AAA', '123', 'Ceci est le libellé', '234.5'], \
['ALO', '345', 'Ceci est une autre', '124.5']]
    """
 
    lines = []
    def __init__(self, struct, seps):
        self.struct = struct
        self.seps = seps        
 
    def get_fields(self):
        lst_lines = [ line  for line in self.struct.rsplit("\n") if line ]
        ar = [] # array
        limit = len(self.seps) - 1     
        for line in lst_lines:
            ar_line = [] # line in the array
            for i in range(0, len(self.seps)):
                # print("i",i)
                if i == 0:
                    field = line[self.seps[i]: self.seps[i+1]-1]
                elif i == limit :
                    field = line[self.seps[i]:]
                else: #cas général
                    field = line[self.seps[i]:self.seps[i+1]-1]
                ar_line.append(field.strip())
            ar.append(ar_line)        
        return ar
    
    def print_fields(self, fields_str):
        """Frint tabulated fields"""
        for line in fields_str:
        # print(line)
            for field in line:
                print(field + "\t", end = '')
            print()        
        

def glims_to_MOD01_format(splitted_data):
    """Convert splitted data into a fact_xpert MOD01 array."""
    A = [ line[1]  for line in splitted_data ]
    return A

def glims_to_MOD02_format(splitted_data):
    """Convert splitted data into a fact_xpert MOD02 array."""
    A = [( '1230567890', line[1], '*'+line[2], int(line[3][:-2]), line[0])  for line in splitted_data ]
    return A

def _test():
    """Execute doctests."""
    import doctest
    (failures, tests) = doctest.testmod(verbose=True)
    print("{} tests performed, {} failed.".format(tests, failures))


if __name__ == "__main__":
    _test()


    # ici on récupère une facture de Glimps.
    import data_for_tests
    
    seps_GLIMS = [2, 9, 20, 54, 61, 67]
    
    a = Spliter(data_for_tests.GLIMS_DIDIER, seps_GLIMS)
    ar_strings = a.get_fields()
    
    print()
    print("J'ai extrait les champs suivants :")
    print(ar_strings)
    # Examen des paramètres récupérés
    print()
    print("En voici une présentation plus structurée :")
    a.print_fields(ar_strings)
    # récupérer la facturation la plus simple (MOD01) et la traiter
    MOD01_fact_xpert_format = glims_to_MOD01_format(ar_strings)
    import facturation
    facturation.model_etude_1(MOD01_fact_xpert_format)


    # récupérer la facturation élaborée et la traiter
    MOD02_fact_xpert_format = glims_to_MOD02_format(ar_strings)
    print("Format élaboré (assez moche")
    print(MOD02_fact_xpert_format)

    facturation.model_etude_1(MOD02_fact_xpert_format, model_type='MOD02')
    
