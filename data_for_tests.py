#!/bin/env/python3
# file: data_test.py
# Set of data for tests.

# 
acts_ok = ['0323', '9105', '1208']

acts_unknown_512_1245_2145 = [
    '9105', '1104', '1610', '0126',
    '1127', '0174', '9005',
    '0996','0552', '1208', # err
    '0593', '0578', '0512','0352', '0353',
    '1245', # err
    '1806', '1207', '9105', '4340', '1465', '0322',
    '0323', '2145', # err
    '4332', '4355', '4362', '4362']

acts_repeated = [
    '9105', '1104', '1610', '0126', '1127', '0174', '9005',
    '0996','0552', '1208', '0593', '0578', '0352', '0353',
     '1806', '1207', '9105', '4340', '1465', '0322',
    '0323', '4332', '4355', '4362', '4362']

acts_unknown_1515 = ['0323', '9105', '1515', '1208']

acts_703_more_than_thrice = [ '0323','0703', '9105', '0703',
                                    '1208','0703', '0703',]

acts_703_more_than_thrice_plus_unknown = [ '0323', #hep
                            '0703', '0703', '9105',
                            '1806', # prot
                            '1789', # inc              
                            '1208','0703', '0703',]

acts_with_more_than_3_hep_B_serologies = ['0323', # hep
                                      '9105', '1208',
                                      '1806', # prot
                                      '1805', # prot
                                      '0353', # hep
                                      '0354', # hep
                                      '0351', # hep                                    '
                                     ]

actes_avec_plus_de_2_prots = ['0323', '9105', '1208'] # FAUX

acts_prots_false_hep_b_false_and_unknown_1517_1518 = [
    '0322', # hep
    '0323', # hep
    '9105',
    '0352', # hep
    '0354', # hep
    '0354', # hep répétée
    '0324', # prot
    '1208',
    '1518', # inc
    '1808', # prot
    '1813', # prot
    '1517' # inc
    ,
    ] 

# Jeux de données dites cumulées.


FACT1 = (('5305051750', '9105', '9105', 5, 'B'),
           ('5305051750', '1610', 'SIONO', 24, 'B'),
           ('5305051750', '9005', 'FPREA', 16, 'B'),
           ('5305051750', '9004', 'SUPW', 26, 'B'),
           ('5305051750', '0593', 'FUC', 8, 'B'),
           ('5305051750', '0578', 'SCALC', 7, 'B'),
           ('5305051750', '0552', 'GLYIO', 5, 'B'))

FACT1_ERR_0578 = (('5305051750', '9105', '9105', 5, 'B'),
           ('5305051750', '1610', 'SIONO', 24, 'B'),
           ('5305051750', '9005', 'FPREA', 16, 'B'),
           ('5305051750', '9004', 'SUPW', 26, 'B'),
           ('5305051750', '0593', 'FUC', 8, 'B'),
           ('5305051750', '0578', 'SCALC', 10, 'B'), # err
           ('5305051750', '0552', 'GLYIO', 5, 'B'))

FACT1_CA_578_rep = (('5305051750', '9105', '9105', 5, 'B'),
           ('5305051750', '1610', 'SIONO', 24, 'B'),
           ('5305051750', '9005', 'FPREA', 16, 'B'),
           ('5305051750', '0578', 'SCALC', 7, 'B'), #
           ('5305051750',              '1612', 'XXXX', 7, 'B'), ##
           ('5305051750', '9004', 'SUPW', 26, 'B'),
           ('5305051750', '0593', 'FUC', 8, 'B'),
           ('5305051750',              '1612', 'XXXX', 7, 'B'), ##         
           ('5305051750', '0578', 'SCALC', 7, 'B'), # 
           ('5305051750', '0552', 'GLYIO', 5, 'B'))


FACT2 = [('5305012345', '9105', '9105', 5, 'B'),
 ('5305012345', '9004', 'SUPW', 26, 'B'),
 ('5305012345', '1610', 'SIONO', 24, 'B'),
 ('5305012345', '1104', 'NUM', 29, 'B'),
 ('5305012345', '9005', 'FPREA', 16, 'B'),
 ('5305012345', '0578', 'SCALC', 7, 'B'),
 ('5305012345', '0593', 'FUC', 8, 'B'),
 ('5305012345', '0552', 'GLYIO', 5, 'B')]

FACT3 = [('5305065478', '9105', '9105', 5, 'B'),
 ('5305065478', '0127', 'AVK', 20, 'B'),
 ('5305065478', '9005', 'FPREA', 16, 'B')]

FACT3_INCOMP = [('5305065478', '9105', '9105', 5, 'B'),
 ('5305065478', '0127', 'AVK', 20, 'B'),
 ('5305065478', '9005', 'FPREA', 16, 'B'),
 ('5305065478', '0126', 'TP', 20, 'B'),]



FACT4 = [('5305012487', '9105', '9105', 5, 'B'),
 ('5305012487', '9004', 'SUPW', 26, 'B'),
 ('5305012487', '0570', 'SELEC', 53, 'B'),
 ('5305012487', '9005', 'FPREA', 16, 'B'),
 ('5305012487', '1806', 'ALBIM', 7, 'B'),
 ('5305093584', '5231', 'LPFHE', 200, 'B'),
 ('5305093584', '0221', 'LPCCR', 25, 'B'),
 ('5305093584', '9106', '9106', 5, 'B')]



FACT5 = [('5305046967', '9105', '9105', 5, 'B'),   
 ('5305046967', '7335', 'TNTUS', 65, 'B'),
 ('5305046967', '1104', 'NUM', 29, 'B'), 
 ('5305046967', '1577', 'HBA1C', 28, 'B'),
 ('5305046967', '0996', 'CTHB', 26, 'B'),
 ('5305046967', '1610', 'SIONO', 24, 'B'),
 ('5305046967', '1127', 'TCAMA', 20, 'B'),
 ('5305046967', '0127', 'AVK', 20, 'B'),
 ('5305046967', '9005', 'FPREA', 16, 'B'),
 ('5305046967', '1821', 'BNP', 78, 'B'),
 ('5305046967', '0593', 'FUC', 8, 'B'),
 ('5305046967', '0514', 'SPAL', 7, 'B'),
 ('5305046967', '1601', 'SBILT', 8, 'B'),
 ('5305046967', '0552', 'GLYIO', 5, 'B'),
 ('5305046967', '0578', 'SCALC', 7, 'B'),
 ('5305046967', '1817', 'PREAL', 20, 'B'),
 ('5305046967', '1804', 'SCRP', 9, 'B'),
 ('5305046967', '1208', 'TSH', 30, 'B'),
 ('5305046967', '0516', 'STGP', 7, 'B'),
 ('5305046967', '0517', 'STGO', 7, 'B'),
 ('5305047015', '9105', '9105', 5, 'B'),
 ('5305047015', '7335', 'TNTUS', 65, 'B'),
 ('5305047050', '9105', '9105', 5, 'B'),
 ('5305047050', '7335', 'TNTUS', 65, 'B')]

FACT6_PROT_ERR_MONTANT_ERR = [('0132366757', '9105', '9105', 5, 'B'), # Pour tester règle prot
('0132366757', '3784', 'ACVHC', 55, 'B'), # date en  dec 2015 vers 42
('0132366757', '0323', 'CHB', 55, 'B'),
('0132366757', '0322', 'GHB', 52, 'B'),
('5122465750', '0388', 'VIH12', 52, 'B'),
('0132366757', '1104', 'NUM', 29, 'B'),
('5122465750', '1610', 'SIONO', 27, 'B'),
('5122465750', '1109', 'RETIC', 20, 'B'),
('5122465750', '9005', 'FPREA', 15, 'B'),
('5122465750', '1819', 'TRF', 14, 'B'), #
('5122465750', '0983', 'PTH', 60, 'B'),
('5122465750', '0593', 'FUC', 8, 'B'),
('5122465750', '0514', 'SPAL', 7, 'B'),
('5122465750', '0563', 'SPHOS', 7, 'B'),
('5122465750', '0578', 'SCALC', 7, 'B'),
('5122465750', '0548', 'SFER', 7, 'B'),
('5122465750', '0552', 'GLYIO', 5, 'B'),
('5122465750', '0532', 'SACUR', 7, 'B'),
('5122465750', '0519', 'SGGT', 7, 'B'),
('5122465750', '1817', 'PREAL', 20, 'B'), #
('5122465750', '1806', 'ALBIM', 10, 'B'), # 
('5122465750', '1213', 'SFERR', 33, 'B'),
('5122465750', '0522', 'TRANS', 11, 'B'),
('5122468866', '9105', '9105', 5, 'B'),
('5122468866', '0162', 'IM43', 200, 'B'),
('1258745392', '9105', '9105', 5, 'B'),
('1258745392', '1610', 'SIONP', 27, 'B'),
('1258745392', '9005', 'FPREA', 15, 'B'),
('1258745392', '0593', 'FUC', 8, 'B')]

FACT6_PROT_ERR_HEP_ERR_MONTANT_ERR = [('0132366757', '9105', '9105', 5, 'B'), # Pour tester règle prot
('0132366757', '3784', 'ACVHC', 55, 'B'), # date en  dec 2015 vers 42
('0132366757', '0323', 'CHB', 55, 'B'),
('0132366757', '0322', 'GHB', 52, 'B'),

('0132366757', '0354', 'VI2', 70, 'B'),
('0132366757', '0353', 'VI1', 70, 'B'),


('5122465750', '0388', 'VIH12', 52, 'B'),
('0132366757', '1104', 'NUM', 29, 'B'),
('5122465750', '1610', 'SIONO', 27, 'B'),
('5122465750', '1109', 'RETIC', 20, 'B'),
('5122465750', '9005', 'FPREA', 15, 'B'),
('5122465750', '1819', 'TRF', 14, 'B'), #
('5122465750', '0983', 'PTH', 60, 'B'),
('5122465750', '0593', 'FUC', 8, 'B'),
('5122465750', '0514', 'SPAL', 7, 'B'),
('5122465750', '0563', 'SPHOS', 7, 'B'),
('5122465750', '0578', 'SCALC', 7, 'B'),
('5122465750', '0548', 'SFER', 7, 'B'),
('5122465750', '0552', 'GLYIO', 5, 'B'),
('5122465750', '0532', 'SACUR', 7, 'B'),
('5122465750', '0519', 'SGGT', 7, 'B'),
('5122465750', '1817', 'PREAL', 20, 'B'), #
('5122465750', '1806', 'ALBIM', 10, 'B'), # 
('5122465750', '1213', 'SFERR', 33, 'B'),
('5122465750', '0522', 'TRANS', 11, 'B'),
('5122468866', '9105', '9105', 5, 'B'),
('5122468866', '0162', 'IM43', 200, 'B'),
('1258745392', '9105', '9105', 5, 'B'),
('1258745392', '1610', 'SIONP', 27, 'B'),
('1258745392', '9005', 'FPREA', 15, 'B'),
('1258745392', '0593', 'FUC', 8, 'B')]


# Un exemple pour améliorer la présentation.
PLUSIEURS_ERREURS = [('6099028079', '9105', '9105', 5, 'B'),
('6099028079', '1387', 'FOLAT', 45, 'B'),
('6099028079', '1374', 'VIB12', 45, 'B'),
('6099028079', '1139', '25OHD', 40, 'B'),
('6099028079', '1104', 'NUM', 29, 'B'),
('6099028079', '1577', 'HBA1C', 28, 'B'),
('6099028079', '0996', 'CTHB', 26, 'B'),
('6099028079', '1610', 'SIONO', 24, 'B'),
('6099028079', '9005', 'FPREA', 16, 'B'),
('6099028079', '1819', 'TRF', 14, 'B'),
('6099028079', '0593', 'FUC', 8, 'B'),
('6099028079', '0983', 'PTH', 60, 'B'),
('6099028079', '0552', 'GLYIO', 5, 'B'),
('6099028079', '0514', 'SPAL', 7, 'B'),
('6099028079', '0548', 'SFER', 7, 'B'),
('6099028079', '0532', 'SACUR', 7, 'B'),
('6099028079', '0563', 'SPHOS', 7, 'B'),
('6099028079', '0578', 'SCALC', 7, 'B'),
('6099028079', '0519', 'SGGT', 7, 'B'),
('6099028079', '1817', 'PREAL', 20, 'B'),
('6099028079', '1806', 'ALBIM', 7, 'B'),
('6099028079', '1208', 'TSH', 30, 'B'),
('6099028079', '1213', 'SFERR', 30, 'B'),
('6099028079', '0522', 'TRANS', 10, 'B'),
('6090123456', '9105', '9105', 5, 'B'),
('6090123456', '1387', 'CHP25', 45, 'B'),
('6090123456', None, 'CHR16', 82, 'BHN'),
('6090123456', '0584', 'CHP28', 7, 'B'),
('6090123456', '1818', 'CHR10', 35, 'B')]

# Data de Glims
# obtention par

GLIMS_01_MOD2 = """
   B     0514       PHOSPHATASES ALCALINES (PH. AL       7.0 B       1.89 
   B     0519       GAMMA GLUTAMYL TRANSFERASE (GA       7.0 B       1.89 
   B     0522       TRANSAMINASES (ALAT ET ASAT; T      10.0 B       2.70 
   B     0552       SANG : GLUCOSE (GLYCEMIE)            5.0 B       1.35 
   B     0593       SANG : UREE ET CREATININE            8.0 B       2.16 
   B     1104       HEMOGRAMME Y COMPRIS PLAQUETTE      29.0 B       7.83 
   B     1601       SANG : BILIRUBINE (BIL)              8.0 B       2.16 
   B     1610       SANG : IONOGRAMME COMPLET (NA       24.0 B       6.48 
   B     1804       CRP (PROTEINE C REACTIVE) (DOS       9.0 B       2.43 
   B     1806       ALBUMINE (DOSAGE) (SANG)             7.0 B       1.89 
   B     9005       FORFAIT DE PRISE EN CHARGE PRE      16.0 B       4.32 
   B     9105       FORFAIT DE SECURITE POUR ECHAN       5.0 B       1.35 
"""

GLIMS_02_MOD2 = """
   B     0127       INR : TEMPS DE QUICK EN CAS DE      20.0 B       5.40 
   B     0552       SANG : GLUCOSE (GLYCEMIE)            5.0 B       1.35 
   B     0593       SANG : UREE ET CREATININE            8.0 B       2.16 
   B     1610       SANG : IONOGRAMME COMPLET (NA       24.0 B       6.48 
   B     9005       FORFAIT DE PRISE EN CHARGE PRE      16.0 B       4.32 
   B     9105       FORFAIT DE SECURITE POUR ECHAN       5.0 B       1.35
"""
GLIMS_01_MOD_00 = """Demande : 1234567
Patient : MONNOM  ESTPERSONNE  
Parti paye par  CENTRE HOSPITALIER LE PUY EN VELAY

================================================================================
   B     0514       PHOSPHATASES ALCALINES (PH. AL       7.0 B       1.89 
   B     0519       GAMMA GLUTAMYL TRANSFERASE (GA       7.0 B       1.89 
===============================================================================
  Nb. de B :    14
  Nb. de BHN :    0
  Nb. de KB :     0
  Nb. de TB :     0
  Nb. de PB :     0
  Nb. de EUR :    0
  Nb. de 100% :   0
"""

GLIMS_01_MOD_XX = """Demande : 1745885
Patient : JADEFE  RETRELEFER  
Parti paye par  CENTRE HOSPITALIER LE PUY EN VELAY

================================================================================
   B     0514       PHOSPHATASES ALCALINES (PH. AL       7.0 B       1.89 
   B     0519       GAMMA GLUTAMYL TRANSFERASE (GA       7.0 B       1.89 
   B     0522       TRANSAMINASES (ALAT ET ASAT; T      10.0 B       2.70 
   B     0552       SANG : GLUCOSE (GLYCEMIE)            5.0 B       1.35 
   B     0593       SANG : UREE ET CREATININE            8.0 B       2.16 
   B     1104       HEMOGRAMME Y COMPRIS PLAQUETTE      29.0 B       7.83 
   B     1601       SANG : BILIRUBINE (BIL)              8.0 B       2.16 
   B     1610       SANG : IONOGRAMME COMPLET (NA       24.0 B       6.48 
   B     1804       CRP (PROTEINE C REACTIVE) (DOS       9.0 B       2.43 
   B     1806       ALBUMINE (DOSAGE) (SANG)             7.0 B       1.89 
   B     9005       FORFAIT DE PRISE EN CHARGE PRE      16.0 B       4.32 
   B     9105       FORFAIT DE SECURITE POUR ECHAN       5.0 B       1.35 
===============================================================================
  Nb. de B :    135
  Nb. de BHN :    0
  Nb. de KB :     0
  Nb. de TB :     0
  Nb. de PB :     0
  Nb. de EUR :    0
  Nb. de 100% :   0
"""

# Même exemple mais nettoyé
GLIMS_01_MOD_XX_corr = """
   B     0514       PHOSPHATASES ALCALINES (PH. AL       7.0 B       1.89 
   B     0519       GAMMA GLUTAMYL TRANSFERASE (GA       7.0 B       1.89 
   B     0522       TRANSAMINASES (ALAT ET ASAT; T      10.0 B       2.70 
   B     0552       SANG : GLUCOSE (GLYCEMIE)            5.0 B       1.35 
   B     0593       SANG : UREE ET CREATININE            8.0 B       2.16 
   B     1104       HEMOGRAMME Y COMPRIS PLAQUETTE      29.0 B       7.83 
   B     1601       SANG : BILIRUBINE (BIL)              8.0 B       2.16 
   B     1610       SANG : IONOGRAMME COMPLET (NA       24.0 B       6.48 
   B     1804       CRP (PROTEINE C REACTIVE) (DOS       9.0 B       2.43 
   B     1806       ALBUMINE (DOSAGE) (SANG)             7.0 B       1.89 
   B     9005       FORFAIT DE PRISE EN CHARGE PRE      16.0 B       4.32 
   B     9105       FORFAIT DE SECURITE POUR ECHAN       5.0 B       1.35 
"""
