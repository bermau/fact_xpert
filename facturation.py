#!/bin/env/python3
# file: lib_facturation.py
# Utilitaires pour la gestion de la facturation

"""La table de référence est dans une base sqlite qui n'est jamais modifiée.
Elle peut même être protégée en écriture, ce qui garantit son intégrité.
La facture à vérifier est écrite dans une base sqlite temporaire.
La fonction SQL attache permet de réaliser des opérations entre les 2 bases."""

import lib_sqlite
import sqlite3
import lib_nabm
import conf_file as Cf
import sys
from bm_u import title

def sub_title(msg):
    print("     **** "+msg+" ***")


class Invoice():
    """Gestion d'une facture NABM.

La facture est implémentée dans une base sqlite pour réaliser des requêtes"""

    def __init__(self):
        # Création de la base dans un fichier réel ou en RAM 
        # self.INVOICE_DB = lib_sqlite.GestionBD('tempo.sqlite')
        self.INVOICE_DB = lib_sqlite.GestionBD(in_memory=True)
        if not self.table_invoice_exists():
            self.create_table_invoice_in_database()
            
    def create_table_invoice_in_database(self):
        print ("JE PASSE PAR LA")
        sql = """CREATE TABLE IF NOT EXISTS invoice_list
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
        return False
    
    def load_invoice_list(self,act_list):
        """Constitue une table (id, acte_1), (id, acte2) ... """
        self.INVOICE_DB.execute_sql("""DELETE FROM invoice_list""")
        for act in act_list:
            # print("Traitemnt : ", act)
            self.INVOICE_DB.execute_sql("""INSERT INTO invoice_list
(code) VALUES (?) """, (act,))
        self.INVOICE_DB.commit()
            
    def show_data(self):
        """Affiche les datas"""
        self.INVOICE_DB.quick_sql("SELECT * FROM invoice_list")


class TestInvoiceAccordingToReference():
    """Tests d'une facture selon une référence.

La base contenant la nomenclature n'est jamais modifiée.
A la base de référence (REF) contenant la nomenclature,
on attache une base temporaire contenant la facture, ce qui permet
d'utiliser des instruction SQL.

On utilise pour cela la commande attach dans Sqlite."""
    def __init__(self, INV_DB, REF_DB, nabm_version):
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
        """Imprimer dans un buffer ou ailleurs."""
        # self.buf.append(msg)
        print(msg)

    def affiche_conclusion_d_un_test(self, rep):
        """Affiche le résultat en clair à l'utilisateur."""
        if rep:
            self.prt_buf("Conclusion : correct")
        else:
            self.prt_buf("Conclusion : incorrect")
        
    def conclude(self):
        """Imprime le rapport le sauve éventuellement."""
        for line in self.buf:
            print(line)
        if self.error == []:
            print("rapport vide")
        else:
            print("Rapport à sauvegarder : ", self.buf)

    def attach_invoice_database(self):
        """Attacher la base de la facture à la base de nomenclature."""
        self.ref.execute_sql("attach database 'tempo.sqlite' as inv")
 
    def affiche_etude_select(self, sql , comment='', param=None):
        """Affiche une liste des lignes de Select éventuellement vide.
-> Liste des résultats ou None.

        """
        if param is None:    
            self.ref.execute_sql(sql)
        else:
            self.ref.execute_sql(sql, param=param)
        res_as_list =  self.ref.resultat_req()
        if len(res_as_list) == 0:
            self.prt_buf("RAS")
            return None # Mieux que False
        else:
            self.prt_buf("{} lignes{} :".format(str(len(res_as_list)),comment))
            for line in res_as_list:
                print(line)
            return res_as_list
        
    def affiche_liste_et_somme_theorique(self, nabm_version=43):
        """"Les actes sont-ils dans la nomenclature.

Puis affiche le nombre de B."""
        
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
        res_lst = self.affiche_etude_select(req, comment=' dans la facture')

        sub_title("Somme théorique des B")
        self.prt_buf("d'après le code de facture, montant de la référence")
        if res_lst:
            total_B =sum([line[3] for line in res_lst
                          if line[3] is not None ])
            self.prt_buf("Somme des B : {}".format(str(total_B)))
        
    
    def verif_tous_codes_dans_nabm(self, nabm_version=43):
        """"Les actes sont-ils présent dans la nomenclature ?

Recherche des lignes absentes de la NABM.
Si anomalie, retourne False, sinon True"""
        
        self.prt_buf("Recherche des lignes absentes de la NABM");
        self.prt_buf("Question : toutes les lignes sont à la NABM ? ");
        req = """
        SELECT
           inv.invoice_list.id,
           inv.invoice_list.code,
           nabm.libelle AS 'libelle_NABM',
           nabm.coef
        FROM inv.invoice_list
        LEFT JOIN nabm 
        ON inv.invoice_list.code=nabm.id
        WHERE nabm.libelle IS NULL
"""
        res_lst = self.affiche_etude_select(req, comment=" hors NABM")
        return res_lst is None

    def inv_test3(self, nabm_version=43):
        """Test de codes répétés CODE TRES LAID"""
        noerror=True
        
        (nabm_file, incompatility_file) = lib_nabm.get_name_of_nabm_files(
            nabm_version)
        self.prt_buf("Certains codes sont-ils présents plus d'une fois ?");
        req="""SELECT  code AS code_NABM,
        count(code) AS 'occurence' 
        FROM inv.invoice_list GROUP BY code
        HAVING occurence> 1""";

        lst = self.affiche_etude_select(req)
        
        self.prt_buf("Le référentiel indique : ")
        for acte  in [ line[0] for line in lst ]:
           sql = """Select id, MaxCode  from {ref_name}
        WHERE id=?""". format(ref_name=nabm_file)
           
           res = self.affiche_etude_select(sql, param =(acte, ))
           # self.prt_buf(self.ref.resultat_req())
           # Un accès par nom serait préférable !
           maxcode =  int(res[0][1])
           print(maxcode)
           if maxcode !=  0:
               print("non nul")

               
    def verif_actes_trop_repetes(self, nabm_version=43):
        """Test de codes répétés.
MEILLEUR CODE avec appel par nom

-> True si pas d'anomalie, False sinon."""
        # On peut sans doute faire beaucoup plus simple avec une vue SQL.
        noerror=True
        
        (nabm_file, incompatility_file) = lib_nabm.get_name_of_nabm_files(
            nabm_version)
        self.prt_buf("Certains codes sont-ils présents plus d'une fois ?");
        req="""SELECT  code,
        count(code) AS 'occurence' 
        FROM inv.invoice_list GROUP BY code
        HAVING occurence> 1"""

        # self.ref est l'objet qui contient un connecteur (nommé con).
        self.ref.con.row_factory = sqlite3.Row
        cur = self.ref.con.cursor()
        
        cur.execute(req)
        for rowa in cur:
            # print (rowa)
            print(rowa['code'], rowa['occurence'])
            # lancer une seconde requête.
            cur2 = self.ref.con.cursor()
            sql2 = """Select id, MaxCode  from {ref_name} 
WHERE id=?""". format(ref_name=nabm_file)
            cur2.execute(sql2, (rowa['code'],))
            for rowb in cur2:
                print("Ref indique : ", (rowb['id']), (rowb['MaxCode']))
                if (rowb['MaxCode'] > 0) and \
                   (int(rowa['occurence']) > int(rowb['MaxCode'])):
                    print("ERREUR maxcode")
                    noerror=False
        return noerror     
           
    def rech_codes(self): 
        """Recherche de codes particulier.

Pour bien tester, j'ai besoin d'actes dont le max soit de
         1, 2 et 3, voire plus."""

        (nabm_file, incompatility_file) = lib_nabm.get_name_of_nabm_files(43)
        self.prt_buf("quelques codes avec MaxCode > 0");
        sql = """Select id, Libelle,MaxCode  from {ref_name}
        WHERE MaxCode > 5 """. format(ref_name=nabm_file)
        self.ref.execute_sql(sql)
        self.prt_buf(self.ref.resultat_req())
        # Je retiens comme exemples :
        # (557, 'LITHIUM (LI , LITHIEMIE , LI SERIQUE , LI ERYTHROCYTAIRE) (SANG)', 2)
        # (1374, 'VITAMINE B 12 (DOSAGE) (SANG)', 1),
        # (1137, 'C-PEPTIDE (SANG)', 3)
        # (703, 'INSULINE LIBRE (SANG)', 3)
        # (1154, 'TEST DIRECT DE COOMBS (ANTIGLOBULINE SPECIFIQUE)', 4)
        # (274, "MYCOBACTERIE : SENSIBILITE VIS A VIS D'UN ANTIBIO PAR ANTIBIO", 5)
    def macro_test(self, nabm_version_43):
        """Comprends plusieurs tests.

Renvoie True si aucun erreur, False sinon.
"""
        self.test_in_nabm(nabm_version=nabm_version)
        
def _test():
    """Execute doctests."""
    import doctest
    (failures, tests) = doctest.testmod(verbose=False)
    print((failures, tests))

def _demo():
    """Exemple d'utilisation.
On définit une liste de codes d'exemples, on en choisit un (a), on teste.
"""
    a_inconnus_512_1245_2145 = ['9105', '1104', '1610', '0126', '1127', '0174', '9005',
    '0996','0552', '1208', '0593', '0578', '0512','0352', '0353',
    '1245', '1806', '1207', '9105', '4340', '1465', '0322',
    '0323','2145', '4332', '4355', '4362', '4362']
    actes_repetes = ['9105', '1104', '1610', '0126', '1127', '0174', '9005',
    '0996','0552', '1208', '0593', '0578', '0352', '0353',
     '1806', '1207', '9105', '4340', '1465', '0322',
    '0323', '4332', '4355', '4362', '4362']
    liste_ok = ['0323', '9105', '1208']
    actes_inconnu1515 = ['0323', '9105', '1515', '1208']

    a = a_inconnus_512_1245_2145
    # lib_nabm.Nabm().expertise_liste(a, nabm_version=43)
    # 3 représentations : la facture, la référence, les Test entre facture
    # et référence.
    # Déclaration et initilisation de la facture:
    # Le test de la facture nécessite une base de facture, une base de nabm
    # et une version de nomenclature.
    act_ref = lib_nabm.Nabm()
    invoice = Invoice()
    invoice.load_invoice_list(a)
    # invoice.show_data() 
    T = TestInvoiceAccordingToReference(invoice.INVOICE_DB, act_ref.NABM_DB,
                                        nabm_version=43)
    T.attach_invoice_database()
    
    title("Affichage")
    T.affiche_liste_et_somme_theorique()
    title("Vérifie si tous les codes sont dans la NABM")    
    rep = T.verif_tous_codes_dans_nabm()
    print("Réponse du test :", rep)
    T.affiche_conclusion_d_un_test(rep)

    title("Vérifie si certains actes ne sont pas trop répétés")
    rep4 = T.verif_actes_trop_repetes()
    print("Conlusion du test : {}".format(rep4))
    T.affiche_conclusion_d_un_test(rep4)

    title("Conclusion générale")
    T.conclude()

if __name__=='__main__':
    #_test()
    _demo()
    pass
    

