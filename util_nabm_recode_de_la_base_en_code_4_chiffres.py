# correction de la base nabm sqlite : remplacer le id integer en code CHAR(4)
# code pour les tables nabm et nabmXX
# code pour les incompatibility et incompatibilityXX

# exemple : le code numérique 3 est à remplacer par la chaine "0003".
from  lib_sqlite import *

# l'idée générale est la suivnte : 
sql_generique="""
BEGIN TRANSACTION;
CREATE TEMPORARY TABLE t1_backup(a,b);
INSERT INTO t1_backup SELECT a,b FROM t1;
DROP TABLE t1;
CREATE TABLE t1(a,b);
INSERT INTO t1 SELECT a,b FROM t1_backup;
DROP TABLE t1_backup;  
COMMIT;
"""

##def script_sql():
def get_sql_for_nabm_table(table):
    """Retourne le SQL pour recoder la table nabm"""    
    sql = """
    -- J'ai utilisé Sqlite manager :
    -- On crée la nouvelle base avec un id de type TEXT :

    BEGIN TRANSACTION;

    CREATE   TABLE "{table_name}_corr" 
    ("code" TEXT PRIMARY KEY  NOT NULL  DEFAULT ('0') ,
    "chapitre" int(11) DEFAULT (NULL) ,
    "sous_chapitre" int(11) DEFAULT (NULL) 
    ,"lettre" char(3) DEFAULT (NULL) ,"coef" int(11) DEFAULT (NULL) ,"date_creation" 
    date DEFAULT (NULL) ,"libelle" varchar(255) DEFAULT (NULL) ,"entente" tinyint(1) 
    DEFAULT (NULL) ,"Remb100" tinyint(1) DEFAULT (NULL) ,"MaxCode" int(11) NOT NULL  
    DEFAULT ('0') ,"ReglSpec" char(2) NOT NULL  DEFAULT ('') ,"RefMed" int(11) 
    DEFAULT ('0') ,"Reserve" tinyint(1) DEFAULT (NULL) ,"IniBio" tinyint(1) DEFAULT 
    (NULL) ,"Tech" int(11) DEFAULT ('0') ,"RMO" smallint(1) DEFAULT (NULL) ,"Sang" 
    tinyint(1) DEFAULT (NULL) ,"DateEffet" date DEFAULT (NULL) ,"Rem" text) ;


    -- On insère toutes les données sans changement, sauf la première colonne qui
    -- reçoit une chaîne de caractères.

    INSERT INTO "{table_name}_corr" 

    SELECT
    printf("%04d", id), 
    chapitre,
    sous_chapitre,
    lettre,
    coef,
    date_creation,
    libelle,
    entente,
    Remb100,
    MaxCode,
    ReglSpec,
    RefMed,
    Reserve,
    IniBio,
    Tech,
    RMO,
    Sang,
    DateEffet,
    Rem
    FROM "{table_name}" ;

    -- on renomme 

    -- ALTER TABLE "{table_name}_corr" RENAME TO "{table_name}_mod" ;

    COMMIT ; 
    """.format(table_name=table)
    
    return sql


def get_sql_for_incompatibility_table(table):
    """Retourne le SQL pour recoder la table de type incompatibility"""    
    sql = """
    -- J'ai utilisé Sqlite manager pour créer le SQL
    -- On crée la nouvelle base avec un id de type TEXT :

    BEGIN TRANSACTION;

    CREATE TABLE "{table_name}_corr" (
    "code" TEXT  NOT NULL DEFAULT '0000',
    "incompatible_code" TEXT  NOT NULL DEFAULT '0000',
    PRIMARY KEY ("code","incompatible_code")
    );

    -- On insère toutes les données sans changement, sauf la première colonne qui
    -- reçoit une chaîne de caractères.

    INSERT INTO "{table_name}_corr" 

    SELECT
    printf("%04d", id), 
    printf("%04d", incompatible_code)
    FROM "{table_name}" ;

    COMMIT ; 
    """.format(table_name=table)
    print(sql)
    return sql

def get_sql_for_rename_tables(table):
    """retorune le sql pour renommer les tables et recoder"""    
    sql = """
    BEGIN TRANSACTION;
    ALTER TABLE "{table_name}" RENAME TO "{table_name}_old" ;
    ALTER TABLE "{table_name}_corr" RENAME TO "{table_name}" ;

    COMMIT ; 
    """.format(table_name=table)
    print(sql)
    return sql

if __name__ == '__main__': 

    con = sqlite3.connect("nabm_db.sqlite")
    try:
        with con:
            for name in ["incompatibility", "incompatibility41",
                         "incompatibility42", "incompatibility43"]:
                print("Traitement de la table : ", name)
                # dé-diéser les lignes à exécuter.
                # con.executescript(get_sql_for_nabm_table(name))
                # con.executescript(get_sql_for_incompatibility_table(name))
                #con.executescript(get_sql_for_rename_tables(name))
    except Exception as err:
        print("SQL Error is :\n%s" % err)

