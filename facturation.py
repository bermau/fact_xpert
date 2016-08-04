#!bin/env/python3
# file: lib_facturation.py
# Utilitaires pour la gestion de la facturation

"""La tabble de référence est dans une base sqlite fermée.
La facture a vérifier est écrite dans une base sqlite temporaire."""


import lib_sqlite
import lib_nabm
import conf_file as Cf
import sys
from bm_u import titrer
 
class Invoice():
    """Gestion d'une facture NABM ou autre.

La facture est implémentée dans une base sqlite pour réaliser des requêtes"""

    def __init__(self):
        self.INVOICE_DB = lib_sqlite.GestionBD('tempo.sqlite')
        # self.INVOICE_DB = lib_sqlite.GestionBD(':memory:')
        if not self.table_invoice_exists():
            self.create_table_invoice_in_database()
            
    def create_table_invoice_in_database(self):
        sql = """CREATE TABLE invoice_list
(id INTEGER PRIMARY KEY, code VARCHAR(4))
"""
        # sys.stderr.write("sql = {}".format(sql))
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


class TestInvoiceAccordingToReference():
    """Tests d'une facture selon une référence.

Je pensais qu'il allait utiliser la structure attach dans python.
En fait il faut l'utiliser dans la base Sqlite."""
    def __init__(self, REF_DB, INV_DB, nabm_version):
        """Enregistrement de 2 connecteurs"""
        self.ref = REF_DB
        self.nabm_version = nabm_version
        (self.nabm_file,
         self.incompatility_file) = lib_nabm.get_name_of_nabm_files(nabm_version)
        self.invoice = INV_DB
        self.report = []
        self.buf = [] # buffer pour toutes les impressions temporaires.
        self.error = 0 # Nombre de résultats anormaux.
        
    def prt_buf(self, msg):
        """Imprimer dans un buffer """
        self.buf.append(msg)
        
    def conclude(self):
        """Imprime le rapport le sauve éventuellement"""
        for line in self.buf:
            print(line)
        if self.error == []:
            print("rapport vide")
        else:
            print("Rapport à sauvegarder : ", self.buf)

    def attach_another_database(self):
        """Attancher la base de la facture à la table de nomenclature"""
        self.ref.execute_sql("attach database 'tempo.sqlite' as inv")
        self.ref.quick_sql("SELECT 'La base 2 est connectée' AS COMMENTAIRE")

    def affiche_etude_select(self,sql):
        """Affiche une liste des lignes de Select éventuellement vide."""
        self.ref.execute_sql(sql)
        res_as_list =  self.ref.resultat_req()
        if len(res_as_list) == 0:
            self.prt_buf("RAS")
            return False
        else:
            self.prt_buf("{} lignes : " . format(str(len(res_as_list))))
            for line in res_as_list:
                print(line)
            return res_as_list
        
    def inv_test1(self, nabm_version=43):
        """"Un premmier test : Les actes sont-ils dans la nomenclature.

Puis affiche de nombre B."""
        
        self.prt_buf("Tous ces actes existent-ils dans la NABM ?");
        req = """
        SELECT
           inv.invoice_list.id,
           inv.invoice_list.code,
           nabm.libelle AS 'libelle_NABM',
           nabm.coef
        FROM inv.invoice_list
        LEFT JOIN nabm 
        ON inv.invoice_list.code=nabm.id 
"""
        res_lst = self.affiche_etude_select(req)
        if res_lst:
            total_B =sum([line[3] for line in res_lst
                          if line[3] is not None ])
            self.prt_buf("Somme des B : {}".format(str(total_B)))
       
    def inv_test2(self, nabm_version=43):
        """"Mettre en évidence les lignes non à la nomenclature."""
        question= "Actes absents du référentiel "
        self.prt_buf(question)

        select_req = """
        SELECT
           inv.invoice_list.id,
           inv.invoice_list.code,
           nabm.libelle AS 'libelle_NABM',
           nabm.coef
        FROM inv.invoice_list
        LEFT JOIN nabm 
        ON inv.invoice_list.code=nabm.id
        WHERE nabm.libelle IS NULL"""

        errors = self.affiche_etude_select(select_req)
        if errors:
            self.report.append(question)
            self.report.append(errors)

        self.prt_buf("Contrôle d'une liste vide : ")
        self.affiche_etude_select("Select 1,2 Where 1 = 2")
        
    def inv_test3(self, nabm_version=43):
        """Test de codes répétés"""
        (nabm_file, incompatility_file) = lib_nabm.get_name_of_nabm_files(nabm_version)
        self.prt_buf("Certains codes sont-ils présents plus d'une fois ?");
        req="""SELECT  code AS code_NABM,
        count(code) AS 'occurence' 
        FROM inv.invoice_list GROUP BY code
        HAVING occurence> 1""";
        lst = self.affiche_etude_select(req)
        self.prt_buf("Le référentiel indique : ")
        for acte in [ line[0] for line in lst ]:
           sql = """Select id, MaxCode  from {ref_name}
        WHERE id=?""". format(ref_name=nabm_file)
           self.ref.execute_sql(sql, param =(acte, ))
           self.prt_buf(self.ref.resultat_req())

        
def study_cursor(cursor):
    nb_lignes = False
    for line in cursor:
        print(line)
        nb_lines = True
    return True
    
                           
def _test():
    """Execute doctests."""
    import doctest
    doctest.testmod(verbose=False)

if __name__=='__main__':
    _test()
    # _demo()
    a = ['9105', '1104', '1610', '0126', '1127', '0174', '9005',
    '0996','0552', '1208', '0593', '0578', '0512','0352', '0353',
    '1245', '1806', '1207', '9105', '4340', '1465', '0322',
    '0323','2145', '4332', '4355', '4362', '4362']
    aa = ['9105', '1104', '1610', '0126', '1127', '0174', '9005',
    '0996','0552', '1208', '0593', '0578', '0352', '0353',
     '1806', '1207', '9105', '4340', '1465', '0322',
    '0323', '4332', '4355', '4362', '4362']
    # a = ['0323','9105', '1208']
    lib_nabm.Nabm().expertise_liste(a, nabm_version=43)
    # On a 2 représentations : la facture, la référence
    act_ref = lib_nabm.Nabm()
    invoice = Invoice()
    
    # invoice.create_table_invoice_in_database()
    invoice.load_invoice_list(a)
    # invoice.show_data()
    
    T = TestInvoiceAccordingToReference(act_ref.NABM_DB, invoice.INVOICE_DB,
                                        nabm_version=43)
    T.attach_another_database()
    T.inv_test1()
    T.inv_test2()
    T.inv_test3()
    T.conclude()    
    

