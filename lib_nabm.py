#!bin/env/ python3
# file : lib_nabm.py
# Utilitaires pour la gestion de la NABM
# (nomenclature des actes de biologie médicale).
# par convention, j'écris tout en anglais, sauf les fonctions
# terminales que je laisse en français.

"""La table de référence est dans une base sqlite fermée.
La facture à vérifier est écrite dans une base sqlite temporaire."""
import conf_file as Cf
import lib_fix_os
import lib_sqlite
import lib_nabm

import sys
from bm_u import title
import datetime

DEBUG = False

# listes des actes de la règle des sérologies hépatite B et des protéines
PROT_LST_REF = ['0321', '0324', '1805', '1806', '1807', '1808',
                '1809', '1810', '1811', '1812', '1813', '1814', '1815', 
                '1816', '1817', '1818', '1819' ]

HEP_B_LST_REF = ['0322', '0323', '0351', '0352', '0353', '0354']

COTA_MINIMALE = ['9905', '9910']
COTA_MINIMALE.extend([str (item) for item in range (9914, 9927)])




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

  
def contient_acte_de_cotation_minimale(act_lst):
    """renvoie True si la liste contient au moins un acte de cotation sang .
    >>> contient_acte_de_cotation_minimale(['9914','1805','9921','1819'])
    True
    >>> contient_acte_de_cotation_minimale(['9914',None,'9921','1819'])
    True
    >>> contient_acte_de_cotation_minimale(['1806','1805','1605','1819'])
    False
"""
    if get_actes_de_cotation_minimale(act_lst):
            return True
    return False    

def get_actes_de_cotation_minimale(act_lst):
    """retourne la liste des actes de cotation minimum de la liste entrée.

renvoie une liste.

True si la liste contient au moins un acte de cotation sang .
    >>> get_actes_de_cotation_minimale(['9914','1805','9921','1819'])
    ['9914', '9921']
    >>> get_actes_de_cotation_minimale(['9914',None,'1610','1819'])
    ['9914']
    >>> get_actes_de_cotation_minimale(['1806','1805','1605','1819'])
    []
"""
    return [item for item in act_lst if item in COTA_MINIMALE]


def get_name_of_nabm_files(nabm_version):
    """Return names of database tables corresponding to NABM version.
--> (nabm_table_name, incompatibility_table_name).

    >>> get_name_of_nabm_files(41)
    ('nabm41', 'incompatibility41')
    >>> get_name_of_nabm_files('42')
    ('nabm42', 'incompatibility42')
    >>> get_name_of_nabm_files('43')
    ('nabm43', 'incompatibility43')
    
"""
    tables = { 
               41:('nabm41', 'incompatibility41'),
               42:('nabm42', 'incompatibility42'),
               43:('nabm43', 'incompatibility43'),
               44:('nabm44', 'incompatibility44'),
          }
    return tables[int(nabm_version)]

    
def nabm_version_from_dt(dt):
    """Return nabm version from a datatime.

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
    >>> nabm_version_from_dt(datetime.date(2017,4,1))
    44
    >>> nabm_version_from_dt(datetime.date(2000,4,19))
    'avant'
"""
    # table contient différentes versions de nabm.
    # chaque date de mise en place est suivie de la version de la nabm
    table = [
        [datetime.date(2014, 4, 14), 41],
        [datetime.date(2014, 9, 4), 42],
        [datetime.date(2016, 4, 20), 43],
        [datetime.date(2017, 4, 1), 44],
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


class Nabm(lib_sqlite.GestionBD):
    "Une classe pour la consultation de la NABM."
    
    def __init__(self, version=Cf.NABM_DEFAULT_VERSION, verbose=None):
        """Ouvre la base de données contenant la NABM

        >>> AA = Nabm()
        >>> AA.describe_acte #doctest: +ELLIPSIS
        <bound method Nabm.describe_acte ...>
        """
        self.NABM_DB=Cf.NABM_DB # ceci est le nom du fichier.
        lib_sqlite.GestionBD.__init__(self, dbName=Cf.NABM_DB)
        if verbose: sys.stderr.write("Ouverture de la base NABM\n")
        self.nabm_name, self_nabm_incompatibility=get_name_of_nabm_files(version)

    def describe_acte(self, code):
        sql = "SELECT * FROM {} WHERE code = ? LIMIT 1".format(self.nabm_name)
        self.prt_sql_in_page_mmode(sql, param=(code,), sep = ":\t")
        
    def test(self):
        title("Ceci est un test avec 1610")
        self.describe_acte(1610)
        title("Ceci est un autre test avec '1610'")
        self.describe_acte("1610")
            
    def __del__(self):
        self.close()
        if DEBUG : print("NABM Object closed")

class Menu(Nabm):
    """Menu déroulant pour la consultation de la Nabm.

MAL écrit à refaire."""

    def __init__(self):
        Nabm.__init__(self)
        
        menu = {
        "01":("Connection à la base (test de ...)", self.connect_db), 

        "05":("Décrire un acte de la NABM", self.fn_describe_acte),
        "06":("Un petit test", self.test),
        "09":("Quitter le Système", self.my_quit_fn),
        "10":("System Quit",self.my_quit_fn)
           }
        pass
        while True:
            print()
            for key in sorted(menu.keys()):
                print( key+" : " + menu[key][0])
            print()
            ans = input("Make A Choice : ")
            menu.get(ans,[None,self.invalid])[1]()
    
    def connect_db(self):
        pass
    def my_quit_fn(self):
        raise SystemExit
    
    def fn_describe_acte(self):

        print()
        acte=input("Acte")
        print()
        self.describe_acte(acte)

    def invalid(self):
        print("\nChoix invalide !!!\n")       
    

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
##    BB = Nabm()
##    BB.test()
##    Menu()
