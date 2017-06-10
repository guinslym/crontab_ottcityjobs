<?php

$emplois = array("http://www.ottawacityjobs.ca/en/data/", "http://www.ottawacityjobs.ca/fr/data/"); 

foreach ($emplois as $value) {
	if (strpos($value, 'en') !== false) {
	    $version =  'data-en.json';
	}else{
		$version =  'data-fr.json';
	}

	$json = file_get_contents($value);
	$obj = json_decode($json);

	$today_date = date_parse(date(DATE_RFC2822));
	$year = $today_date['year'];
	$mois = $today_date['month'];
	$day = $today_date['day'];
 	$filename = strval($year). '-'. strval($mois) . '-'. strval($day). '-'.$version;
	$fp = fopen($filename, 'w');
	fwrite($fp, json_encode($obj, JSON_PRETTY_PRINT));
	fclose($fp);
	print($filename."\n");
}

