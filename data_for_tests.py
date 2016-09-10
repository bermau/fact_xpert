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

acts_703_more_than_thrice_plus_unknown = [ '0323','0703', '9105',
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
