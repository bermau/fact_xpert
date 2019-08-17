"""Tool for Glims.
Example to use lib_glims.

Extraire des structures d'un tableau régulier.
Extraction de champs de longueur fixe.

Les données sont issues d'un copier coller de 
Dossier/ Cotation / visualisation facture.

"""

import lib_glims
import data_for_tests

from data_for_tests import GLIMS_01_MOD_XX  


def go():
    undelimited_raw_visu_txt = AA

    print("Données entrées : \n\n**{}**\n".format(undelimited_raw_visu_txt))

    
    print("Le type de données est {}".format(type(undelimited_raw_visu_txt)))
    # import pdb
    # pdb.set_trace()
    
    clear_txt = lib_glims.delimite_format(undelimited_raw_visu_txt)
    print()
    print("Données propres : \n\n{}\n".format(clear_txt))

    print()
    
    S = lib_glims.Splitter(data_for_tests.GLIMS_02_MOD2, lib_glims.seps_GLIMS)
    print()
    print("\nDonnées par get_fields : ")
    print(purge_double_liste(S.get_fields()))
    print("\nDonnées mieux présentées : ")
    print(list_to_tab(purge_double_liste(S.get_fields())))
    

if __name__ == '__main__':
    pass
    # Il est délicat de faire accepter une chaine de plusieurs lignes
    # input is an undelimiter_raw visualizationi text.
    # 
    # undelimited_raw_visu_txt = GLIMS_01_MOD_XX
    try:
        if AA :
            go()
    except:
        print("Saisir la chaîne dans la variable AA, puis lancer go()")

    
    
    
    


