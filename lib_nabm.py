#!bin/env/python3
# Utilitaires pour la gestion de la NABM
# (nomenclature des actes de biologie médicale).
# par convention, j'écris tout en anglais, sauf les fonctions
# terminales que je laisse en français.
"""La tabble de référence est dans une base sqlite fermée.
La facture a vérifier est écrite dans une base sqlite temporaire."""


import lib_sqlite
import conf_file as Cf
import sys 

PROT_LST_REF = ['0321', '0324', '1805', '1806', '1807', '1808',
                '1809', '1810', '1811', '1812', '1813', '1814', '1815',
                '1816', '1817', '1818', '1819' ]

HEP_B_LST_REF = ['0322', '0323', '0351', '0352', '0353', '0354']

def _detect_more_than_n_objects_in_a_list(actes_lst, lst_ref, N):
    sous_liste = [ acte for acte in actes_lst if acte in lst_ref ]
    if len(sous_liste) > N:
        return True, sous_liste
    else:
        return False

def detecter_plus_de_deux_proteines(actes_lst):
    """Renvoie si la liste contient plus de 2 protéines."""
    return _detect_more_than_n_objects_in_a_list(actes_lst, PROT_LST_REF, 2)

def detecter_plus_de_trois_sero_hepatite_b(actes_lst):
    """Renvoie si la liste contient plus de 3 sérologies hépatite B."""
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


def titrer(msg):
    print("*" * 30)
    print(msg)
    print("*" * 30)
    
class Nabm():
    
    def __init__(self):
        pass
        self.NABM_DB = lib_sqlite.GestionBD(Cf.NABM_DB)
        sys.stderr.write("Ouverture de la base NABM\n")
        
    def expertise_liste(self, lst_actes, nabm_version=43):
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
        # self.NABM_DB.close()
        print("POURQUOI ?Fermeture de la base {base} terminée".format(base=Cf.NABM_DB))

class Invoice():
    """Gestion d'une facture NABM ou autre.
La facture est implémentée dans une base squlite pour réaliser des requêtes"""
    def __init__(self):
#         self.INVOICE_DB=Nabm().INVOICE_LIST
        self.INVOICE_DB = lib_sqlite.GestionBD('tempo.sqlite')
        # self.INVOICE_DB = lib_sqlite.GestionBD(':memory:')
        
##        import pdb
##        pdb.set_trace()
        if not self.table_invoice_exists():
            
            self.create_table_invoice_in_database()
            
    def create_table_invoice_in_database(self):
        sql = """CREATE TABLE invoice_list
(id INTEGER PRIMARY KEY, code VARCHAR(4))
"""
        sys.stderr.write("sql = {}".format(sql))
        self.INVOICE_DB.execute_sql(sql)

    def drop_table_invoice(self):
        self.INVOICE_DB.execute_sql("""
DROP TABLE invoice_list 
"""
            )
    def table_invoice_exists(self):
        """Test if table of invoices is defined."""
        return True
    
    def load_invoice_list(self,act_list):
        """Constitue une table (id, acte_1), (id, acte2) ... """
        self.INVOICE_DB.execute_sql("""DELETE FROM invoice_list""")
        for act in act_list:
            # print("Traitemnt : ", act)
            self.INVOICE_DB.execute_sql("""INSERT INTO invoice_list
(code) VALUES (?) """, (act,))
        self.INVOICE_DB.commit()
            
    def show_data(self):
        self.INVOICE_DB.quick_sql("SELECT * FROM invoice_list")

class TestInvoiceReference():
    """Tests d'une facture selon une référence.

Je pensais qu'il allait utiliser la structure attach dans python.
En fait il faut l'utiliser dans la base Sqlite."""
    def __init__(self, REF_DB, INV_DB):
        """Enregistrement de 2 connecteurs"""
        self.ref = REF_DB
        self.invoice = INV_DB

    def attach_another_database(self):
        self.ref.execute_sql("attach database 'tempo.sqlite' as inv")
        self.ref.quick_sql("SELECT 'La base 2 est connectée' AS COMMENTAIRE")
        # self.ref.quick_sql('SELECT * FROM inv.invoice_list')
        # La base de référence 'connait' à présent la notion de facture.
        # On peut réaliser des vérifications entre les 3 bases.

    def inv_test1(self, nabm_version=43):
        """"Un premmier test"""
        (nabm_file, incompatility_file) = get_name_of_nabm_files(nabm_version)
        titrer("Tous ces actes existent-ils dans la NABM ?");

        self.ref.quick_sql("""
        SELECT
           inv.invoice_list.id,
           inv.invoice_list.code,
           nabm.libelle AS 'libelle_NABM',
           nabm.coef
        FROM inv.invoice_list
        LEFT JOIN nabm 
        ON inv.invoice_list.code=nabm.id 
""")

    def inv_test2(self, nabm_version=43):
        """"Un premmier test"""
        titrer("actes non présent dans le référentiel ")
        # print("Fonction appelée : {}", )
        (nabm_file, incompatility_file) = get_name_of_nabm_files(nabm_version)

        self.ref.quick_sql("""
        SELECT
           inv.invoice_list.id,
           inv.invoice_list.code,
           nabm.libelle AS 'libelle_NABM',
           nabm.coef
        FROM inv.invoice_list
        LEFT JOIN nabm 
        ON inv.invoice_list.code=nabm.id
        WHERE nabm.libelle IS NULL
""")
        
    
                           
def _test():
    """Execute doctests."""
    import doctest
    doctest.testmod(verbose=False)

if __name__=='__main__':
    # _test()
    # _demo()
    a = ['9105', '1104', '1610', '0126', '1127', '0174', '9005',
    '0996','0552', '1208', '0593', '0578', '0512','0352', '0353',
    '1245', '1806', '1207', '9105', '4340', '1465', '0322',
    '0323','2145', '4332', '4355', '4362', '4362']
    # a = ['0323','9105', '1208']
    # Nabm().expertise_liste(a, nabm_version=43)
    # On a 2 représentations : la facture, la référence
    act_ref = Nabm()
    invoice = Invoice()
    
    # invoice.create_table_invoice_in_database()
    invoice.load_invoice_list(a)
    # invoice.show_data()
    
    T = TestInvoiceReference(act_ref.NABM_DB, invoice.INVOICE_DB)
    T.attach_another_database()
    T.inv_test1()
    T.inv_test2()
    
    
#    invoice.INVOICE_DB.close()
