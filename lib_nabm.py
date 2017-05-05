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
import datetime
# listes des actes de la règle des sérologies hépatite B et des protéines
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
    """Renvoie False si la liste contient plus de 2 protéines et la liste des actes
en erreur.
    >>> detecter_plus_de_deux_proteines(['1806','1805','1605','1819'])
    (False, ['1806', '1805', '1819'])

    """
    return _detect_more_than_n_objects_in_a_list(actes_lst, PROT_LST_REF, 2)

def detecter_plus_de_trois_sero_hepatite_b(actes_lst):
    """Renvoie False si la liste contient plus de 3 sérologies hépatite B.
    >>> a = detecter_plus_de_trois_sero_hepatite_b(['1806','1805','0323', '0353', '0354'])
    >>> a[0]
    True

    """
    return _detect_more_than_n_objects_in_a_list(actes_lst, HEP_B_LST_REF, 3)

  

def get_name_of_nabm_files(nabm_version):
    """Return names of database tables corresponding to NABM version.
--> (nabm_table_name, incompatibility_table_name).

    >>> get_name_of_nabm_files(41)
    ('nabm41', 'incompatibility41')
    >>> get_name_of_nabm_files('42')
    ('nabm42', 'incompatibility42')
    >>> get_name_of_nabm_files('43')
    ('nabm', 'incompatibility')
    
"""
    tables = { 43:('nabm', 'incompatibility'),
               41:('nabm41', 'incompatibility41'),
               42:('nabm42', 'incompatibility42'),
          }
    return tables[int(nabm_version)]

    
def nabm_version_from_dt(dt):
    """Return nabm version form a datatime.

TODO : verifier que dt est au format datetime.

    >>> nabm_version_from_dt(frdate2datetime('14/04/2014'))
    41
    >>> nabm_version_from_dt(datetime.date(2014,4,18))
    41
    >>> nabm_version_from_dt(datetime.date(2016,4,19))
    42
    >>> nabm_version_from_dt(datetime.date(2016,4,20))
    43
    >>> nabm_version_from_dt(datetime.date(2016,4,25))
    43
    >>> nabm_version_from_dt(datetime.date(2000,4,19))
    'avant'
"""
    # table contient différentes versions de nabm.
    # chaque date de mise en place est suivi de la version de la nabm
    table = [
        [datetime.date(2014, 4, 14), 41],
        [datetime.date(2014, 9, 4), 42],
        [datetime.date(2016, 4, 20), 43],
        ]
    
    prec = table[0]
    if dt < prec[0]:
        return 'avant'
    else:
        for line in table:
            if dt < line[0]:
                return prec[1]
            else:
                prec = line
        return prec[1]


# get_nabm_version_from_fr_date(datetime.date())   
def frdate2datetime(fr_date):
    """Return a datetime.date from a french date
Entrée : 01/02/2016
    >>> frdate2datetime("02/05/2015")
    datetime.date(2015, 5, 2)
"""
    year = int(fr_date[6:10]) # On convertit la chaine de caractère en integer   
    month = int(fr_date[3:5])
    day = int(fr_date[0:2])
    return datetime.date(year, month, day)


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

##    def charger_liste_de_codes(act_lst):
##        """Enregiste une liste dans la base de données.
##
##La table est nommée : nabm_sheet
##Ne semble plus servir à rien.
##"""
##        pass
        
    def __del__(self):
        self.NABM_DB.close()
        # print("POURQUOI ? Fermeture de la base {base} terminée".format(base=Cf.NABM_DB))

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
                           
def _test():
    """Execute doctests."""
    import doctest
    doctest.testmod(verbose=True)

if __name__=='__main__':
    _test()
    # Nabm()
