#!/bin/env/python3
# file: lib_facturation.py
# Utilitaires pour la gestion de la facturation

"""La table de référence est dans une base sqlite qui n'est jamais modifiée.
Elle peut même être protégée en écriture, ce qui garantit son intégrité.
La facture à vérifier est écrite dans une base sqlite temporaire.
La fonction SQL attache permet de réaliser des opérations entre les 2 bases."""


# Les mots PEU EFFICACE indique les axes d'améliorations

import sys, os , datetime
import lib_sqlite
import sqlite3
import lib_nabm
import conf_file as Cf
import lib_invoice
import lib_smart_stdout

from bm_u import title

def sub_title(msg):
    print("     **** "+msg+" ***")

def advice(msg):
    print("                *** CONSEIL :    +"+msg + "   ****")
   

class TestInvoiceAccordingToReference():
    """Tests d'une facture selon une référence.

La base contenant la nomenclature n'est jamais modifiée.
A la base de référence (REF) contenant la nomenclature,
on attache une base temporaire contenant la facture, ce qui permet
d'utiliser des instruction SQL.

On utilise pour cela la commande attach dans Sqlite."""
#    def __init__(self, INV_DB, REF_DB, nabm_version):
    def __init__(self, invoice, REF_DB, nabm_version):
        """Enregistrement de 2 connecteurs"""
        
        self.ref = REF_DB
        self.nabm_version = nabm_version
        (self.nabm_table,
         self.incompatibility_table) = lib_nabm.get_name_of_nabm_files(nabm_version)
        self.invoice = invoice
        self.report = []
        self.buf = [] # buffer pour toutes les impressions temporaires.
        self.error = 0 # Nombre de résultats anormaux.
        self.debug = True
    def prt_buf(self, msg):
        """Imprimer dans un buffer ou ailleurs."""
        # self.buf.append(msg)
        print(msg)

    def affiche_conclusion_d_un_test(self, rep):
        """Affiche la conclusion d'un test en clair à l'utilisateur."""
        if rep:
            print(" : correct")
        else:
            print(" :"+" "*40+"******** incorrect ******")
        
    def conclude(self):
        """Imprime le rapport et le sauve éventuellement."""
        for line in self.buf:
            print(line)
        if self.error == []:
            print("rapport vide")
        else:
            print("Rapport à sauvegarder : ", self.buf)

    def attach_invoice_database(self):
        """Attacher la base de la facture à la base de nomenclature."""
        # ILLOGIQUE : on devrait pouvoir attacher ce qui vient de invoice.
        self.ref.execute_sql("attach database 'tempo.sqlite' as inv")
        
        # self.ref.execute_sql("attach database ':memory:' as inv")
        sys.stderr.write("Invoice db attached\n")
        
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
            # self.prt_buf("RAS")
            return None # Mieux que False
        else:
            self.prt_buf("{} lignes{} :".format(str(len(res_as_list)),comment))
            for line in res_as_list:
                print(line)
            return res_as_list
        
    def affiche_liste_et_somme_theorique(self, nabm_version=43):
        """"Les actes sont-ils dans la nomenclature.

Puis affiche le nombre de B."""
        # BUG : il faut pouvoir indiquer la version de nabm
        # self.prt_buf("Liste des actes de la facture.");
        req = """
        SELECT
           inv.invoice_list.id,
           inv.invoice_list.code,
           N.libelle AS 'libelle_NABM',
           N.coef
        FROM inv.invoice_list
        LEFT JOIN {nabm_table} AS N 
        ON inv.invoice_list.code=N.id 
""".format(nabm_table=self.nabm_table)
       
        res_lst = self.affiche_etude_select(req, comment=' dans la facture')       
        self.prt_buf('')
        self.prt_buf('Format python :')
        self.prt_buf(res_lst)

        self.prt_buf('')
        self.prt_buf('Format pour AMZ: ')
        self.prt_buf(" ".join([code[1] for code in res_lst]))
        
        sub_title("Somme théorique des B")
        self.prt_buf("d'après le code de facture, montant de la référence")
        if res_lst:
            total_B =sum([line[3] for line in res_lst
                          if line[3] is not None ])
            self.prt_buf("Somme des B : {}".format(str(total_B)))
        
    def verif_tous_codes_dans_nabm(self, nabm_table=None):
        """"Les actes sont-ils présents dans la nomenclature ?

Recherche des lignes absentes de la NABM.
Si anomalie, retourne False, sinon True"""
        if nabm_table is None:
            nabm_table=self.nabm_table
        # self.prt_buf("Recherche des lignes absentes de la NABM");
        # self.prt_buf("Question : toutes les lignes sont à la NABM ? ");
        req = """
        SELECT
           inv.invoice_list.id,
           inv.invoice_list.code,
           N.libelle AS 'libelle_NABM',
           N.coef
        FROM inv.invoice_list
        LEFT JOIN {} AS N 
        ON inv.invoice_list.code=N.id
        WHERE N.libelle IS NULL
""".format(nabm_table)
        res_lst = self.affiche_etude_select(req, comment=" hors NABM")
        return res_lst is None
         
    def verif_codes_et_montants(self, nabm_version=43):
        """Test de la valeur des codes.
possible si MOD02
-> True si valeur anomale, sinon False."""
        if self.invoice.model_type !='MOD02':
            print("Vérification du montant impossible.")
            # raise ValueError('Verification du montant impossible')
            return True # A améliorer.
        else:
            sql = """SELECT I.code, I.nb_letters, I.letter, N.coef
                     FROM inv.invoice_list AS I
                     LEFT JOIN {} AS N
                     ON I.code=N.id
                     WHERE I.nb_letters <> N.coef
                     OR I.letter <>N.lettre
                     """.format(self.nabm_table)
            self.ref.con.row_factory = sqlite3.Row
            cur = self.ref.con.cursor()
            cur.execute(sql)
            noerror = True
            for row in cur:
                print(row['code'], row['nb_letters'], row['coef'])
                print("Erreur : dans l'acte {} remplacer la valeur {} par la valeur {}"\
                      .format(row['code'],row['nb_letters'],row['coef'] ))
                noerror = False
            return noerror

    def verif_actes_trop_repetes(self, nabm_version=43):
        """Test de codes répétés.

-> True si pas d'anomalie, False sinon."""
        noerror = True
        # self.prt_buf("Certains codes sont-ils présents plus d'une fois ?");
        req="""SELECT  code, count(code) AS 'occurence', N.MaxCode
               FROM inv.invoice_list
               LEFT JOIN {ref_name} AS N ON inv.invoice_list.code = N.id
               GROUP BY code    
               HAVING occurence> 1""".format(ref_name=self.nabm_table)
        
        # self.ref instance d'objet qui contient le connecteur con.
        self.ref.con.row_factory = sqlite3.Row
        cur = self.ref.con.cursor()
        cur.execute(req)
        for row in cur:
            print(row['code'], row['occurence'], row['MaxCode'])
            if row['occurence']> int(row['MaxCode']):
                noerror = False
            advice('Supprimer un ou des codes : '+ row['code'])            
        return noerror

    
    def _print_order_by_value(self, act_lst, max_allowed):
        """Calculate acts ordered by value."""
    
        req = """
        SELECT
           N.id, N.coef, N.libelle AS 'libelle_NABM'
        FROM {table} AS N
        WHERE N.id in ({my_list}) 
        ORDER BY N.coef DESC
        """.format(table=self.nabm_table, my_list=', '.join(act_lst))    

        res_lst = self.affiche_etude_select(req,
                                            comment=' classées par valeurs')
        col0 = [ ligne[0] for ligne in res_lst ]
        trois_plus_chers = col0[0:max_allowed]
        print("Conseil : garder"  + str(trois_plus_chers))

    def print_recommandation_erreur_hepatites(self, act_lst):
        """Affiche une solution pour la règle des séro hépatites."""
        # print("Suggestion de correction pour les sérologies hépatites.")
               
        advice("Suggestion de correction pour les sérologies hépatites.");
        self._print_order_by_value(act_lst, 3)

    def print_recommandation_erreur_proteines(self, act_lst):
        """Affiche une solution pour la règle des protéines."""
        advice("Suggestion de correction pour les sérologies hépatites.")
        self._print_order_by_value(act_lst, 2)
        
    def verif_hepatites_B(self):
        """Test s'il n'y a pas plus de 3 codes de la liste des hépatites.

Renvoie True si oui, et False s'il y a plus de 3 codes."""
        
        # code_lst = self.get_list_of_actes() # PAS EFFICIENT.
        # print("liste étudiée", self.invoice.act_list)
        response = lib_nabm.detecter_plus_de_trois_sero_hepatite_b(
            self.invoice.act_list)
        # ATTENTION:  response = (bool, liste)
        if response[0] :
            # print("La règle des hépatites n'est pas enfreinte")
            return True
        else:
            print("Règles de hépatites non respectée : {}".format(response[1]))
            self.print_recommandation_erreur_hepatites(response[1])
            return False 
        
    def verif_proteines(self):
        """Test s'il n'y a pas plus de 2 codes de la liste des protéines.

Renvoie True si oui, et False s'il y a plus de 2 codes."""
        
        # code_lst = self.get_list_of_actes() # PAS EFFICIENT.
        response = lib_nabm.detecter_plus_de_deux_proteines(
            self.invoice.act_list)
        # ATTENTION:  response = (bool, liste)
        if response[0] :
            # print("La règle des protéines n'est pas enfreinte")
            return True   
        else:
            print("Règles de protéines non respectée : {}".format(response[1]))
            self.print_recommandation_erreur_proteines(response[1])
            return False
        
    def verif_compatibilites(self):
        """Test la présence d'incompabilités.
Retourne True si aucune, et False s'il y a des incompatibilités."""
        noerror = True
        sql = """SELECT I.code, INC.incompatible_code
                 FROM inv.invoice_list AS I
                 JOIN {} AS INC
                 ON I.code=INC.id
                 """.format(self.incompatibility_table)
        self.ref.con.row_factory = sqlite3.Row
        cur = self.ref.con.cursor()
        cur.execute(sql)
        for row in cur:
            # print(row['code'], row['incompatible_code'])
            # PEU EFFICIENT : lancer une seconde requête.
            # PEU EFFICIENT : la bases des incompatilibités est mal codée :
            # les codes sont en format string alors que la table nabm a des
            # au format numérique.
            
            cur2 = self.ref.con.cursor()
            sql2 = """SELECT * FROM inv.invoice_list
WHERE code = '{}' """ .format(str(row['incompatible_code']).rjust(4,"0"))
            cur2.execute(sql2)
            for row2 in cur2:
                print("\n          ***** Erreur d'incompatibilité    ****")
                for a in row2:
                    sys.stdout.write(str(a)+" ")
                print()
                noerror = False
        return noerror    
        
    def _rech_code(self): 
        """Recherche de codes particulier.

Pour bien tester, j'ai besoin d'actes dont le max soit de
         1, 2 et 3, voire plus."""

        # (nabm_table, incompatibilities_table) = lib_nabm.get_name_of_nabm_tables(43)
        self.prt_buf("quelques codes avec MaxCode > 0");
        sql = """Select id, Libelle, MaxCode  from {ref_name}
        WHERE MaxCode > 5 """. format(ref_name=self.nabm_table)
        self.ref.execute_sql(sql)
        self.prt_buf(self.ref.resultat_req())
        # Je retiens comme exemples :
        # (557, 'LITHIUM (LI , LITHIEMIE , LI SERIQUE , LI ERYTHROCYTAIRE) (SANG)', 2)
        # (1374, 'VITAMINE B 12 (DOSAGE) (SANG)', 1),
        # (1137, 'C-PEPTIDE (SANG)', 3)
        # (703, 'INSULINE LIBRE (SANG)', 3)
        # (1154, 'TEST DIRECT DE COOMBS (ANTIGLOBULINE SPECIFIQUE)', 4)
        # (274, "MYCOBACTERIE : SENSIBILITE VIS A VIS D'UN ANTIBIO PAR ANTIBIO", 5)

    def _sql_divers(self): 
        """Recherche de codes particulier.

Pour bien tester, j'ai besoin d'actes dont le max soit de
         1, 2 et 3, voire plus."""

        # (nabm_table, incompatibilities_table) = lib_nabm.get_name_of_nabm_tables(43)
        self.prt_buf("SQL Divers");
        sql = """Select * from nabm WHERE id='1610' """
        self.ref.execute_sql(sql)
        self.prt_buf(self.ref.resultat_req())
        # Je retiens comme exemples :
        # (557, 'LITHIUM (LI , LITHIEMIE , LI SERIQUE , LI ERYTHROCYTAIRE) (SANG)', 2)
        # (1374, 'VITAMINE B 12 (DOSAGE) (SANG)', 1),
        # (1137, 'C-PEPTIDE (SANG)', 3)
        # (703, 'INSULINE LIBRE (SANG)', 3)
        # (1154, 'TEST DIRECT DE COOMBS (ANTIGLOBULINE SPECIFIQUE)', 4)
        # (274, "MYCOBACTERIE : SENSIBILITE VIS A VIS D'UN ANTIBIO PAR ANTIBIO", 5)


def get_affiche_liste_codes(code_liste):
    """Utilisaire qui retour une liste de codes épurée.

    >>> get_affiche_liste_codes(['9105', '1104', '1610', '0126', ])
    '9105 1104 1610 0126'
    """
    return(" ".join([code for code in code_liste]))
        

DEBUG = False

@lib_smart_stdout.record_if_true(filename='erreur.txt')
def model_etude_OK(act_lst, model_type='MOD01'):
    """Un modèle un initial."""
    # lib_nabm.Nabm().expertise_liste(a, nabm_version=43)
    # 3 représentations : la facture, la référence, les Test entre facture
    # et référence.
    # Déclaration et initilisation de la facture:
    # Le test de la facture nécessite une base de facture, une base de nabm
    # et une version de nomenclature.
    main_conclusion = True
    title("                                 ====== > LANCEMENT EXPERTISE ")
    if DEBUG:
        print("ACTES etudiés", act_lst)
    act_ref = lib_nabm.Nabm()
    invoice = lib_invoice.Invoice( model_type=model_type)
    invoice.load_invoice_list(act_lst )
    # invoice.show_data()
    
    T = TestInvoiceAccordingToReference(invoice, act_ref.NABM_DB,
                                        nabm_version=43)
    T.attach_invoice_database()

    print("Debut tests")
    title("Affichage")
    T.affiche_liste_et_somme_theorique()

    title("Vérifie si tous les codes sont dans la NABM")    
    resp1 = T.verif_tous_codes_dans_nabm()
    if DEBUG:
        print("Réponse du test :", resp1)
    T.affiche_conclusion_d_un_test(resp1)
    main_conclusion = main_conclusion and resp1

    title("Vérifie si certains actes ne sont pas trop répétés : ")
    resp2 = T.verif_actes_trop_repetes()
    if DEBUG:
        print("Conclusion du test : {}".format(resp2))
    T.affiche_conclusion_d_un_test(resp2)
    main_conclusion = main_conclusion and resp2

    title("Vérifie si la règles des hépatites est respectée : ")
    resp3 = T.verif_hepatites_B()
    if DEBUG:
        print("Conclusion du test : {}".format(resp3))
    T.affiche_conclusion_d_un_test(resp3)
    main_conclusion = main_conclusion and resp3

    title("Vérifie si la règles des protéines est respectée : ")
    resp4 = T.verif_proteines()
    if DEBUG:
        print("Conclusion du test : {}".format(resp4))
    T.affiche_conclusion_d_un_test(resp4)
    main_conclusion = main_conclusion and resp4

    title("Montants")
    resp5 = T.verif_codes_et_montants()
    if DEBUG:
        print("Conclusion du test : {}".format(resp5))
    T.affiche_conclusion_d_un_test(resp5)
    
    main_conclusion = main_conclusion and resp5
    print(main_conclusion, resp5)

    title("Incompatilibités : ")
    resp6 = T.verif_compatibilites()

    T.affiche_conclusion_d_un_test(resp6)    
    main_conclusion = main_conclusion and resp6
    print(main_conclusion, resp6)
##    title("RECHERCHER SQL")
##    T._sql_divers()
    
    title("Conclusion générale")
    T.affiche_conclusion_d_un_test(main_conclusion)
    return not main_conclusion

    #T.conclude(main_conclusion)

@lib_smart_stdout.record_if_true(filename='erreur.txt')
def model_etude_1(act_lst, model_type='MOD01'):
    """Une xexpertise mieux présentée."""

    main_conclusion = True
    print()
    print("                                 ====== > LANCEMENT EXPERTISE ")
    print_version_and_date()
    if DEBUG:
        print("ACTES etudiés", act_lst)
    act_ref = lib_nabm.Nabm()
    invoice = lib_invoice.Invoice(model_type=model_type)
    invoice.load_invoice_list(act_lst)
    # invoice.show_data()

    T = TestInvoiceAccordingToReference(invoice, act_ref.NABM_DB,
                                        nabm_version=43)
    T.attach_invoice_database()

    print("Debut tests")
    title("Affichage")
    T.affiche_liste_et_somme_theorique()
    title("Vérifications")
    print("Vérifie si tous les codes sont dans la NABM", end='')    
    resp1 = T.verif_tous_codes_dans_nabm()
    if DEBUG:
        print("Réponse du test :", resp1)
    T.affiche_conclusion_d_un_test(resp1)
    main_conclusion = main_conclusion and resp1

    print("Vérifie si certains actes ne sont pas trop répétés", end='')
    resp2 = T.verif_actes_trop_repetes()
    if DEBUG:
        print("Conclusion du test : {}".format(resp2))
    T.affiche_conclusion_d_un_test(resp2)
    main_conclusion = main_conclusion and resp2

    print("Vérifie si la règles des hépatites est respectée", end='')
    resp3 = T.verif_hepatites_B()
    if DEBUG:
        print("Conclusion du test : {}".format(resp3))
    T.affiche_conclusion_d_un_test(resp3)
    main_conclusion = main_conclusion and resp3

    print("Vérifie si la règles des protéines est respectée", end='')
    resp4 = T.verif_proteines()
    if DEBUG:
        print("Conclusion du test : {}".format(resp4))
    T.affiche_conclusion_d_un_test(resp4)
    main_conclusion = main_conclusion and resp4

    print("Montants", end='')
    resp5 = T.verif_codes_et_montants()
    if DEBUG:
        print("Conclusion du test : {}".format(resp5))
    T.affiche_conclusion_d_un_test(resp5)
    
    main_conclusion = main_conclusion and resp5
    
    print("Incompatilibités", end='')
    resp6 = T.verif_compatibilites()
    T.affiche_conclusion_d_un_test(resp6)    
    main_conclusion = main_conclusion and resp6
    
    print("Conclusion générale", end='')
    T.affiche_conclusion_d_un_test(main_conclusion)
    return not main_conclusion

    #T.conclude(main_conclusion)


def _demo_1_for_simple_list():
    """Exemple d'utilisation.
On définit une liste python de codes, on en choisit un (a), on teste.
"""
    title("DEMO 1")
    import data_for_tests

    # On peut aussi utiliser les listes déja programmées comme en dédiésant
    model_1 = data_for_tests.acts_ok
    # model_1 a = lib_nabm.PROT_LST_REF
    # model_1 = data_for_tests.data_for_tests.acts_prots_false_hep_b_false_and_unknown_1517_1518
    # model_1 a = data_for_tests.acts_with_more_than_3_hep_B_serologies
    model_etude_1(model_1, model_type='MOD01')

def _demo_2_data_from_synergy():
    """Données extraites de synergy.

Une démonstration.
La facture est sur le modèle suivant dit 'MOD02'.
Chaque ligne de facture contient le numéro de dossier, nom d'acte, la lettre type,
le nombre de lettres.
La facture vient par exmeple du programme syn_odbc_connexion.py
    
"""
    title("DEMO 2")
    import data_for_tests
    model_2 = data_for_tests.FACT2
    model_etude_1(model_2, model_type='MOD02')


def _demo_3_several_record_form_synergy():
    """ Traitement de plusieurs factures de suite.

But : Eviter de refermer la base si possible."""
    title("DEMO 3 : several_record_form_synergy")
    import data_for_tests    
    model_etude_1(data_for_tests.FACT1, model_type='MOD02')
    model_etude_1(data_for_tests.FACT1_ERR_0578, model_type='MOD02')
    model_etude_1(data_for_tests.FACT2, model_type='MOD02')
    model_etude_1(data_for_tests.FACT3, model_type='MOD02')
    model_etude_1(data_for_tests.FACT3_INCOMP, model_type='MOD02')
   
def print_version_and_date():
    """Print version and execution datetime"""
    version = "Programme : " + os.path.basename(__file__)
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), end='   ')
    print(version)

def saisie_manuelle():
    """Demande une saisie manuelle et l'expertise."""
    
    print("Mode de saisie : manuel")
    saisie = input("Saisir une liste de codes séparés par des espaces ")
    # saisie.replace("  "," ")
    act_lst = [ code.rjust(4,'0') for code in saisie.split(" ") if code not in ('', ' ')]
    print(act_lst)
    model_etude_1(act_lst)
def _test():
    """Execute doctests."""
    import doctest
    (failures, tests) = doctest.testmod(verbose=False)
    print("{} tests performed, {} failed.".format(tests, failures))

if __name__=='__main__':

    #_test()
    #_demo_1_for_simple_list()
    # _demo_2_data_from_synergy()
    _demo_3_several_record_form_synergy()
    # saisie_manuelle()
    pass
    

