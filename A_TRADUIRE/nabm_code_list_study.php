<?php
/* -----------------------------------------
Cette page permet de savoir si une liste de codes d'analyses comporte des incompatibilités selon la NABM (ceci n'a d'intérêt que dans les pays où s'applique la nabm, c'est-à-dire en France principalement). Il est vraisemblable que des systèmes analogues existent dans d'autres pays.
Cette page est en théorie indépendante du lms.

mai 2016 : on peut transmettre dans l'url la version de la nabm à utiliser.

TODO : $prev_nabm est mal initialisée

--------------------------------------------- */
// NOTE : lors de l'écriture de la page, les idées de tests me sont venu au fur et à mesure de son utilisation. Chaque test comporte une requete, portant un numéro. En pratique le test 7 est effectué avant le test 2.  Je n'ai pas renommé les tests/requête. 
// amélioration : rendre cette table indépendante du système Sylam/Codat.
require ("library/start.php");
require ("library/sql.php");
require ("library/al_report_class.php");

// Récupérer le numéro de nabm transmis sur l'url

global $nabm, $incompatibility;
if (isset($_REQUEST['nabm_version'])) $nabm_version=$_REQUEST['nabm_version'];

if ((isset($nabm_version)) and (! empty($nabm_version)))
{
  EchoExplanation("La NABM demandée est la version numéro : $nabm_version");
  $nabm='nabm'.$nabm_version;
  $incompatibility='incompatibility'.$nabm_version;
}
else {
  $nabm='`nabm`';
  $incompatibility='`incompatibility`';
}


# require ("library/lms.php"); // afin que cette page soit indépendant du lms (laboratory management system)
$sheet_name ='`nabm_sheet`';
$prev_nabm='`nabm42`';  # name of the previous NABM table.


EchoInitHtml("NABM audit");
EchoTitle("Etude de la table de code",'index','');
EchoExplanation("AmaziliaLab va rechercher certaines incohérences dans la liste des codes de la table saisie précédemment");
EchoExplanation("Pour imposer une version de NABM, compléter l'adresse avec ?nabm_version=XX , où XX est le numéro de NABM.");
// Test 1)
//Tous les actes existent-ils ? 
EchoTitle2("Tous les actes existent-ils dans la NABM ?");
$req1="select nabm_sheet.id, nabm_sheet.code, $nabm.libelle AS 'libelle_NABM', $nabm.coef
FROM $nabm
RIGHT JOIN nabm_sheet 
ON nabm_sheet.code=$nabm.id";
if ($res1=SendSql($req1))
{
	AutoTabOut($res1);
}
mysql_free_result($res1);
EchoExplanation("Un libellé manquant signifie probablement que votre liste de codes contient un code qui a disparu de la nomenclature.");

// test9)10)11 : Quelle est la somme de la feuille. Je dois créer une table intermédiaire, tempora1ire, que je détruis après.
EchoTitle2("Quelle est la somme des codes de la feuille");
$req9="CREATE TEMPORARY TABLE tmp3 SELECT nabm_sheet.id, nabm_sheet.code, $nabm.coef
FROM $nabm
RIGHT JOIN nabm_sheet 
ON nabm_sheet.code=$nabm.id;
";
$res9=SendSql($req9);

$req10="select SUM(coef) from tmp3";
if ($res10=SendSql($req10))
{
	AutoTabOut($res10);
}

$req11="drop TABLE IF EXISTS tmp3";
if ($res11=SendSql($req11))
{
	echo "Table temporaire détruite<br>";
} 
// mysql_free_result($res9);
mysql_free_result($res10);
// mysql_free_result($res11);

EchoExplanation("Vérifier que la somme ci-dessus correspond à votre facture");

// Test8)
// Si un code n'existe pas dans la NABM actuelle, on le cherche dans l'ancienne NABM.
if (ALineIsEmpty())
{
	EchoTitle2("ATTENTION : certains codes n'existent pas dans la NABM actuelle");
	EchoTitle2("Existaient-ils dans la NABM précédente");
$req8="select nabm_sheet.id, nabm_sheet.code, $prev_nabm.libelle AS 'libelle_NABM_precedente'
FROM $prev_nabm
RIGHT JOIN nabm_sheet 
ON nabm_sheet.code=$prev_nabm.id";
if ($res8=SendSql($req8))
{
	AutoTabOut($res8);
}
mysql_free_result($res8);
}

// Test 7) Des codes sont-ils présents plus d'une fois ?

EchoTitle2("Certains codes sont-ils présents plus d'une fois ?");
$req7="select  nabm_sheet.code AS code_NABM, count(nabm_sheet.code) AS 'occurence' 
FROM nabm_sheet GROUP BY code";
if ($res7=SendSql($req7))
{
// 	AutoTabOut($res7/*);*/
	TabWithLinks($res7,'code_NABM','nabm.php','id');
}
mysql_free_result($res7);
EchoExplanation("Si un code est présent plus d'une fois, vous devez vérifier que le nombre maximum de codes est correct");



//test 2)
// A quels codes de LMX correspondent ces codes de NABM ?

EchoTitle2("A quels codes de ".LMS_LONGNAME." correspondent ces codes de NABM ?");
EchoExplanation("La table suivante cherche les codes situés dans le fichier lmx_ele");

$req2="SELECT 
	lmx_ele.id AS 'code ELE', 
	nabm_sheet.code, 
        $nabm.libelle AS 'libellé_nabm',
	lmx_ele.id AS LMX_ELE_ID,
	lmx_ele.E_ABBTXT  AS 'LMX_EXE_abrege'
FROM $nabm
RIGHT JOIN nabm_sheet 
ON nabm_sheet.code=$nabm.id
LEFT JOIN lmx_ele
ON lmx_ele.F_COD=nabm_sheet.code";
if ($res2=SendSql($req2))
{
// 	AutoTabOut($res2);
	TabWithLinks($res2,'code ELE','lmx_ele.php',$target_field='id');
}
mysql_free_result($res2);

//test 2bis)
// A quels codes de LMX_GRP correspondent ces codes de NABM ?


EchoExplanation("Même requête en cherchant les codes situés dans le fichier lmx_grp");

$req2="SELECT 
	lmx_grp.id AS 'code GRP', 
	nabm_sheet.code, 
	$nabm.libelle AS 'libellé_nabm',
	lmx_grp.id AS LMX_GRP_ID,
	lmx_grp.E_ABBTXT  AS 'LMX_EXE_abrege'
FROM $nabm
RIGHT JOIN nabm_sheet 
ON nabm_sheet.code=$nabm.id
LEFT JOIN lmx_grp
ON lmx_grp.F_COD=nabm_sheet.code";
if ($res2=SendSql($req2))
{
// 	AutoTabOut($res2);
        TabWithLinks($res2,'code GRP','lmx_grp.php',$target_field='id');
}
mysql_free_result($res2);

// test 3)
// Les  codes de $sheet_name  présentent-ils des incompatibilités ?

EchoTitle2("Les codes de $sheet_name présentent-ils des incompatibilités ?");
EchoExplanation("AmaziliaLab recherche maintenant les codes incompatibles entre eux et leur codage dans votre système".LMS_LONGNAME);

$req3="DROP TABLE IF EXISTS tempo_code";
 if ($res3=SendSql($req3))
{
	echo("Destruction de la table temporaire 'tempo_code'<br>");
}
 
$req4="CREATE TABLE tempo_code select DISTINCT nabm_sheet.code, $incompatibility.incompatible_code 
FROM $incompatibility 
RIGHT JOIN nabm_sheet 
ON nabm_sheet.code=$incompatibility.id";
if ($res4=SendSql($req4))
{
	echo("Création de la table temporaire 'tempo_code' : OK <BR>");
}
// Présentation de la table temporataire
// EchoTitle2("La table temporaire créée est : ");
// if ($res6=SendSql("SELECT * FROM tempo_code")) AutoTabOut($res6);

// Confrontation de la table temporaire et de la table de code 
$req6="SELECT   nabm_sheet.code,
		tempo_code.code AS 'incompatible avec'
	FROM nabm_sheet LEFT JOIN tempo_code  
	ON tempo_code.incompatible_code=nabm_sheet.code";
	
if ($res6=SendSql($req6))
{
	EchoExplanation("La table ci-dessous doit faire apparaître les incompatibilités. Une table vide signifie que les codes sont compatibles.");
	TabWithLinks($res6,'code',"nabm.php",'id');
}



// Test ajouté en mai 2016 : on liste les codes de nomenclature selon l'ordre des chapitres de la nabm

// Test 12)
//Tous les actes existent-ils ? 
EchoTitle2("Liste des codes actes classés par chapitre");
$req12="select nabm_sheet.id, nabm_sheet.code, $nabm.libelle AS 'libelle_NABM', $nabm.coef
FROM $nabm
RIGHT JOIN nabm_sheet 
ON nabm_sheet.code=$nabm.id
ORDER BY $nabm.chapitre,$nabm.sous_chapitre, $nabm.id";
if ($res12=SendSql($req12))
{
        AutoTabOut($res12);
}
mysql_free_result($res12);
EchoExplanation("Ci dessus, un libellé manquant signifie probablement que votre liste de codes contient un code qui a disparu de la nomenclature.");




function ALineIsEmpty()
{
   global $nabm;
	$req8="select nabm_sheet.id, nabm_sheet.code, $nabm.libelle AS 'libelle_NABM'
	FROM $nabm
	RIGHT JOIN nabm_sheet 
	ON nabm_sheet.code=$nabm.id WHERE $nabm.libelle IS NULL";
	if ($res8=SendSql($req8))
	{
		if (mysql_num_rows($res8)>0)  
		{ return true ; } 
		else 
		{ return false ; }
	}
}
?>
