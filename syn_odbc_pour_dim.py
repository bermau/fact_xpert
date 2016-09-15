
# Extraction DIM
"""Fonction pour extraire une pseudo fichier CSV pour le DIM."""


import syn_odbc_connexion

def req_main_results_from_id_A_REVOIR(id=None):
    """Essai pour le DIM : principaux résultats de chimie et hémato.

- retrouver des résultats depuis une ID.
- Comme on ne veut que que quelques résultats, je filtre sur certains
chapitres.

Cette fonction est appelée par self.essai_flux_pour_dim().
"""
    cnxn = pyodbc.connect(Cf.CONNEXION_BASE_PROD)
    cursor = cnxn.cursor()
    output=[]
    print("id reçu" , id)
    cursor.execute("""SELECT P.REFHOSPNUMBER,DT.TESTCODE, DT.SHORTTEXT, T.RESVALUE, DT.UNITS, R.REQDATE
FROM TESTS T, REQUESTS R, PATIENTS P, DICT_TESTS DT
WHERE R.PATID=P.PATID
AND R.ACCESSNUMBER= ?
AND DT.CHAPID in (12,14,16,22,23,24,25,28)
AND R.REQUESTID=T.REQUESTID
AND DT.TESTID=T.TESTID
AND T.RESVALUE IS NOT NULL""", id  )

    rows = cursor.fetchall()  # lit toute la suite
    cursor.close()
    return rows

def essai_flux_pour_dim():
    """Création d'un fichier CSV d'essai pour le DIM."""
    import lib_utilitaires_synergy
    date = '60110'
    debut = 1627
    fin = 1636
    nom_fichier = 'res_' + date + str(debut).rjust(5,'0') + '_' \
                  + date + str(fin-1).rjust(5,'0') + '.csv'
    print("Le fichier de sortie sera : {}".format(nom_fichier))
    
    la_liste = lib_utilitaires_synergy.get_range_of_id(date,debut,fin)
    print(la_liste)
    with open(nom_fichier, 'w', encoding='utf-8') as fichier:
        for dossier in la_liste:
            print("je traite le dossier : {}".format(dossier))
            # les_res=req_results_from_id(id=dossier)
            les_res = req_main_results_from_id(id=dossier)
            for line in les_res:
                a= str(line[0]), str(line[1]), str(line[2]),str(line[3]), \
                   str(line[4]),line[5].strftime('%Y%m%d')
                b= ";".join(a)
                print(b)
                fichier.write(b + "\n")


if __name__=='__main__':
    CONNEXION = syn_odbc_connexion.MyODBC_to_infocentre()
    #_test()
    
    essai_flux_pour_dim()
    # _demo_etude_facturation_d_un_jour("01/09/2016")
    del(CONNEXION)
