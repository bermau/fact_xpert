"""Module de pour sondage (extractions répérés) sur Synergy."""

from syn_odbc_connexion import *

class demo_poll():
    """Démonstration d'un sondage sur plusieurs jours, répétés"""
    CONNEXION = MyODBC_to_infocentre()
    NB_ERREUR=0
    NB_IPP=0
    days = 4
    def __init__(self):
        print("passage par init")
    
    def action(self):
            
        with open(file="sondage.txt", mode='a', encoding='UTF8') as rapport:
            # je prends le premier lundi de la première semaine pleine de chaque
            # mois
            for date_in_month in [#"04/01/2016",
                                  #"01/02/2016",
                                  #"07/03/2016",
                                  #"04/04/2016", "02/05/2016", "06/06/2016",
                                  "04/07/2016",
                                  # "01/08/2016", "05/09/2016",
                                  #"03/10/2016", "07/11/2016", "05/12/2016";
                                  ]:              
                NB_ERREUR = 0
                NB_IPP = 0
                for date in sequence_of_dates(date_in_month, demo_poll.days):
                    demo_etude_facturation_d_un_jour(date,  uf_filter='6048',
                                                      synthesis=True)
                rapport.write("Erreurs tot\t{}\t{}\tpour\t{}\t IPP\n". \
                               format(date_in_month, str(NB_ERREUR), str(NB_IPP)))
    def __del__(self):
        
        del(demo_poll.CONNEXION)


if __name__=='__main__':
    demo_poll().action()

  
