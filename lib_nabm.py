#!bin/env/python3
# file : lib_nabm.py
# Utilitaires pour la gestion de la NABM
# (nomenclature des actes de biologie médicale).
# par convention, j'écris tout en anglais, sauf les fonctions
# terminales que je laisse en français.

"""La table de référence est dans une base sqlite fermée.
La facture à vérifier est écrite dans une base sqlite temporaire."""

import lib_sqlite
import conf_file as Cf
import sys
from bm_u import title as titrer

PROT_LST_REF = ['0321', '0324', '1805', '1806', '1807', '1808',
                '1809', '1810', '1811', '1812', '1813', '1814', '1815',
                '1816', '1817', '1818', '1819' ]

HEP_B_LST_REF = ['0322', '0323', '0351', '0352', '0353', '0354']

def _detect_more_than_n_objects_in_a_list(actes_lst, lst_ref, N):
    """Renvoie False si une liste contient plus de n membres d'une liste de reférence.
    """
    sous_liste = [ acte for acte in actes_lst if acte in lst_ref ]
    if len(sous_liste) > N:
        return False, sous_liste
    else:
        return True, sous_liste

def detecter_plus_de_deux_proteines(actes_lst):
    """Renvoie si la liste contient plus de 2 protéines.
    >>> detecter_plus_de_deux_proteines(['1806','1805','1605','1819'])
    (False, ['1806', '1805', '1819'])

    """
    return _detect_more_than_n_objects_in_a_list(actes_lst, PROT_LST_REF, 2)

def detecter_plus_de_trois_sero_hepatite_b(actes_lst):
    """Renvoie si la liste contient plus de 3 sérologies hépatite B.
    >>> a = detecter_plus_de_trois_sero_hepatite_b(['1806','1805','0323', '0353', '0354'])
    >>> a[0]
    True

    """
    return _detect_more_than_n_objects_in_a_list(actes_lst, HEP_B_LST_REF, 3)

def _demo():
    """Une démonstration des possibilité de ce module"""
    a = ['9105', '1104', '1610', '0126', '1127', '0174', '9005',
    '0996','0552', '1208', '0593', '0578', '0512','0352', '0353',
    '1245', '1806', '1207', '9105', '4340', '1465', '0322',
    '0323','2145', '4332', '4355', '4362', '4362']
    print("Voilà une liste d'actes : ", a)
    print("Test des protéines : ")
    print(detecter_plus_de_deux_proteines(a))
    print("Test des sérologies Hépatite B :")
    print(detecter_plus_de_trois_sero_hepatite_b(a))    

def get_name_of_nabm_files(nabm_version):
    """Renvoie le nom des tables de la nabm en fonction de la version.
--> (nabm_table_name, incompatibility_table_name).

    >>> get_name_of_nabm_files(41)
    ('nabm41', 'incompatibility41')
    >>> get_name_of_nabm_files('42')
    ('nabm42', 'incompatibility42')
"""
    tables = { 43:('nabm', 'incompatibility'),
               41:('nabm41', 'incompatibility41'),
               42:('nabm42', 'incompatibility42'),
          }
    return tables[int(nabm_version)]


class Nabm():
    
    def __init__(self):
        """Ouvre la base de données contenant la NABM

        >>> TEST=Nabm()
        
        """
        self.NABM_DB = lib_sqlite.GestionBD(Cf.NABM_DB)
        sys.stderr.write("Ouverture de la base NABM\n")
        
    def expertise_liste(self, lst_actes, nabm_version=43):
        """Ce premier essai me semble à déplacer."""
        (nabm_file, incompatility_file) = get_name_of_nabm_files(nabm_version)
        print(lst_actes)
        titrer("Tous ces actes existent-ils dans la NABM ?");
        for acte in lst_actes:
            print("{} : ".format(acte), end='')
            req="""SELECT nabm.id, nabm.libelle 
        AS 'libelle_NABM', 'B', nabm.coef
        FROM nabm
        WHERE nabm.id=  {} """.format(acte)
            self.NABM_DB.execute_sql(req)
            res = self.NABM_DB.cursor.fetchall()
            if res:
                for line in res:
                    print(line)
            else:
                print("---")
        titrer("Un libellé manquant signifie probablement \
que votre liste de codes contient un code qui a disparu de la nomenclature.");

    def charger_liste_de_codes(act_lst):
        """Enregiste une liste dans la base de données.

La table est nommée : nabm_sheet
"""
        pass
        
    def __del__(self):
        self.NABM_DB.close()
        # print("POURQUOI ? Fermeture de la base {base} terminée".format(base=Cf.NABM_DB))
                           
def _test():
    """Execute doctests."""
    import doctest
    doctest.testmod(verbose=True)

if __name__=='__main__':
    # _test()
    Nabm()
