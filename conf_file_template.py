# file : conf_file.py
# Fichier de configuration exemple
# à adapter

# Connexion à la base principale
# Exemple pour SQL Server.
CONNEXION_BASE_PROD = 'DRIVER={SQL Server};SERVER=nom_du_serveur;\
PORT=le_port;DATABASE=nom_de_la_base;UID=qq_un;PWD=machin'

# Nom de la bases sqlite contenant la nabm.
# Les versions sont nabm41, 42 et 43.
NABM_DB = "nabm_db.sqlite"   
# Version à utiliser si rien de précisé
NABM_DEFAULT_VERSION=43

# Où enregistrer les résultats
EXPORT_REP = "rapports"
