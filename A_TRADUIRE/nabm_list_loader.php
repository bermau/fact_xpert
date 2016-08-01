<?php
/* -----------------------------------------
Cette page permet de charger rapidement la table nabm_liste
Ce programme insère des données dans le fichier '$table_name'"
# progrès recherché : tester la validité des données entrantes.
--------------------------------------------- */
require ("library/start.php");
require ("library/sql.php");
require ("library/al_report_class.php");
$g_debug=false;
$table_name ='`nabm_sheet`';   # nom du fichier de la base
$title="Charger une liste de codes NABM";
$the_report = new ALReport();
$the_report->short_title='AL-codes charger';
// récupérer la liste des codes transmise par la méthode post.
$code_list_with_space_str=@stripslashes($_REQUEST['code_list_with_space_str']);
Debug($code_list_with_space_str,"\$code_list_with_space_str");
// 	echo $code_list_with_space_str;
// On pourrait vérifier que la suite de codes est correcte.
// $number_mask='[[digit]]+';
// $code_list_array_mask="[[:digit;]]+,";

// DANS CE PROG IL Y A PLUSIEURS VARIABLES A NE PAS CONFONDRE : 
// $code_list_with_space_str
// $code_list_array
// $code_list_str (une liste intermédiaire)
# Ici, il faut vérifier que la chaîne saisie est conforme et la préparer. 
#  strips excess whitespace
$code_list_with_space_str=trim($code_list_with_space_str);
$code_list_with_space_str=preg_replace('/\s\s+/',' ',$code_list_with_space_str);
$code_list_array=explode(' ',$code_list_with_space_str);

Debug($code_list_array, "\$code_list_array");
// Pris par le temps, je ne vais utiliser qu'une partie des caractéristiques de al_report.
if ( ! $the_report->display_mode_is_valid() or empty($code_list_array))
	{
		EchoInitHtml($the_report->short_title);
		EchoTitle("Saisir une liste de codes de la nomenclature",'','');
		EchoExplanation("Les données doivent être séparées par un espace ou un retour à la ligne.");
		$init_str=InitString($table_name);
		echo "<FORM ACTION=\"".$_SERVER['PHP_SELF']."\" METHOD=\"POST\">";
		echo "Liste de codes : <textarea name=\"code_list_with_space_str\" cols =\"60\" rows = \"5\">$init_str</textarea>
		<br>";
		$the_report->EchoChooseDisplay();
		echo "</FORM>\n";
		EchoEndHtml();
	}
	else // les variables entrées sont correctes.
	{
// 		$g_debug=true;
		EchoInitHtml($the_report->short_title);
		EchoTitle("Chargement d'une liste de codes de la nomenclature",'','');
// Première requête : Vider la table 
		EchoTitle2("Vidage de la table $table_name");
		$req1="TRUNCATE TABLE $table_name";
		if ($res=SendSql($req1))
		{
			echo "OK";
		}
		else
		{
			EchoError("Impossible de vider $table_name");
		};
// Seconde requête : remplir la table
		EchoTitle2 ("Transfert des données dans la table de codes  NABM ($table_name)<br>");
		Debug("Calcul de la liste à mettre dans la requête SQL");
		$list_for_value='('.implode($code_list_array, '),(').')';
		Debug( "Voici la liste à charger : $list_for_value<br>");
		$req2="INSERT INTO $table_name (code) VALUES $list_for_value";
		Debug($req2,"Requête");
		If ($res2=SendSql($req2))
		{
			echo "OK<br>";
		}
			else
		{	
			EchoError ("Echec lors du chargement de $table_name");
		}		
	}
	
//
// The following function returns a string of the data from table  `nabm_sheet`. Data are separated by a space ` `.
function InitString ($table_name)
{	
	$codes_array=array();
	$req="SELECT  code from $table_name ORDER BY id";
	if($res=SendSql($req))
	{
		while ($line=mysql_fetch_array($res))
		{
			$codes_array[]=$line['code'];
		}
		$liste_of_codes=implode($codes_array,' ');
		return $liste_of_codes;
	}
	else {
	EchoError( "in ".__FILE__.' ligne : '.__LINE__) ;
	}
}	
?>
