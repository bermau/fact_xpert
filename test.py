#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Unittest fact_xpert."""

# Les 4 lignes suivantes sont issues du fichier parent de ce script
# Fonctionne sous Python  3.4.2 sous Linux Debian 8.1
# Fonctionne sous Python  3.4.3 sous Windows Seven
# ce fichier doit être compris dans /tests/ qui est situé avec les exécutables
# 
# v1 : jan 2016 : le test est fonctionnel sous Linux comme sous Windows
# v2 : mars 2016 : support une nouvelle architecture : /bin/, /test/, /input/,
# /output/

# 
import unittest, os, sys, pdb

dirname=os.path.dirname(__file__) # __file__ n'est pas défini sous IDLE 2.7. 
# if dirname=='':
#     dirname='.'
dirname=os.path.realpath(dirname)
updir=os.path.split(dirname)[0]
if updir not in sys.path:
    # updir=updir+r'/bin/'
    print("Ajout de {} à la variable PATH".format(updir)) 
    sys.path.append(updir)
                    
# à partir de maintenant on peut rechercher les modules situés
# au dessus de ce script
from facturation import *
from lib_nabm import *

# On définit une classe contenant les différents tests.
class CalculsTest(unittest.TestCase):
    """Cette classe contient les méthodes qui, si elles conmmencent par le mot
test, sont des tests unitaires."""
        
    @classmethod    
    def setUpClass(self):
        """Crée l'environnement. Initialise des listes d'actes."""
        self.a_inconnus_512_1245_2145 = ['9105', '1104', '1610', '0126', '1127', '0174', '9005',
    '0996','0552', '1208', '0593', '0578', '0512','0352', '0353',
    '1245', '1806', '1207', '9105', '4340', '1465', '0322',
    '0323','2145', '4332', '4355', '4362', '4362']
        self.actes_repetes = ['9105', '1104', '1610', '0126', '1127', '0174', '9005',
    '0996','0552', '1208', '0593', '0578', '0352', '0353',
     '1806', '1207', '9105', '4340', '1465', '0322',
    '0323', '4332', '4355', '4362', '4362']
        self.actes_ok = ['0323', '9105', '1208']
        self.actes_inconnu_1515 = ['0323', '9105', '1515', '1208']
        self.actes_703_repete_plus_de_3_fois = [ '0323','0703', '9105','0703', '1208','0703', '0703',]

        print("Setting Up Class environment")

    def setUp(self):
       """Crée l'environnemnt en ouvrant l'application et insère une chaine dans la premier fenetre"""
       print("SetUp environment")
       actes_ok = ['0323', '9105', '1208']
       
    def XX_tearDown(self):
        print("Tearing down environment.\n")

    def test_1_always_true(self):
        """.....Test toujours vrai."""
        self.assertTrue( True )

    def test_2_nabm1(self):
        """.....règle sur séro hépatites B."""
        self.assertFalse(detecter_plus_de_trois_sero_hepatite_b([
            '1806','1805','0323', '0353', '0354']))

    def test_3_nabm2(self):
        """.....Extraction de lignes de facturation depuis un écran VIS."""
        self.assertEqual(self.actes_ok, ['0323', '9105', '1208'])

    def test_4_name(self):
        """.....Facture selon le module facturation."""
        act_ref = Nabm()
        # Déclaration et initilisation de la facture:
        invoice = Invoice()
        invoice.load_invoice_list(self.actes_ok)
        # invoice.show_data()
        # Le test de la facture nécessite une base de facture, une base de nabm
        # et une version de nomenclature.
    
        T = TestInvoiceAccordingToReference(invoice.INVOICE_DB, act_ref.NABM_DB,
                                            nabm_version=43)
        T.attach_invoice_database()
        title("Test 1")
        T.inv_test1()
        title("Test 1 Version2")
        self.assertTrue(T.inv_in_nabm(nabm_version=43))

    def test_5_name(self):
        """.....Facture selon le module facturation acte inconnu."""
        act_ref = Nabm()
        # Déclaration et initilisation de la facture:
        invoice = Invoice()
        invoice.load_invoice_list(self.actes_inconnu_1515)
        # invoice.show_data()
        # Le test de la facture nécessite une base de facture, une base de nabm
        # et une version de nomenclature.
    
        T = TestInvoiceAccordingToReference(invoice.INVOICE_DB, act_ref.NABM_DB,
                                            nabm_version=43)
        T.attach_invoice_database()
        title("Test 1")
        T.inv_test1()
        title("Test 1 Version2")
        self.assertFalse(T.inv_in_nabm(nabm_version=43))
 
def test_suite():
    """retourne la liste des tests à traiter."""
    
    tests = [ unittest.makeSuite(CalculsTest) ]
    return unittest.TestSuite(tests)  
        
if __name__ == '__main__':
    """Programme de test de vérification de la NABM."""
    # rep=os.getcwd() 
    # print (os.path.dirname(rep))
    # os.chdir(r'..\bin')

    # import trt_vis_de_synergy
    # from filecmp import cmp    # pour comparer des fichiers.
    
    # lancer les unittest
    suite = unittest.TestLoader().loadTestsFromTestCase(CalculsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
