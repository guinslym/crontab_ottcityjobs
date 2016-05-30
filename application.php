<?php

//create db
//file: create_db.php


   $dbhost = 'localhost';
   $dbuser = 'root';
   $dbpass = 'root';
   $conn = mysql_connect($dbhost, $dbuser, $dbpass);
   mysql_select_db('ottawa');

   if(! $conn ) {
      die('Could not connect: ' . mysql_error());
   }

   echo 'Connected successfully';


//load File
//Loading the content in JSON
$string = file_get_contents("full.json");
$data = json_decode($string, true);

//fetch all row
$sql = 'SELECT JOBREF FROM jobs';

$retval = mysql_query( $sql, $conn );
if(! $retval )
{
  die('Could not get data: ' . mysql_error());
}

mysql_set_charset("utf8");
$stack = array();
while($row = mysql_fetch_array($retval, MYSQL_ASSOC))
{
    //echo "JOBREF :{$row['job_ref']} \n";
    //array_push($stack, $row['job_ref']);;
    $stack[$row['JOBREF']] = $row['JOBREF'];


}

//loop through the json file
$obj = $data;
for($i=0; $i<count($obj); $i++) {

    $job_ref = ($obj[$i]["JOBREF"]);
    $job_url = ($obj[$i]["JOBURL"]);
    $name = $obj[$i]["NAME"];
    $position = $obj[$i]["POSITION"];
    $salary_max = $obj[$i]["SALARYMAX"];
    $salary_min = $obj[$i]["SALARYMIN"];
    $expiry_date = $obj[$i]["EXPIRYDATE"];
    $post_date = $obj[$i]["POSTDATE"];
    $company_desc = $obj[$i]["COMPANY_DESC"];
    $education_and_exp = $obj[$i]["EDUCATIONANDEXP"];
    $knowledge = $obj[$i]["KNOWLEDGE"];
    $job_summary = $obj[$i]["JOB_SUMMARY"];

    //there is a difference between
    //mysql_real_escape_string
    //and
    //mysqli_real_escape_string
    //mysqli will be deprecated in php 5.5
    //https://stackoverflow.com/questions/25636975/warning-mysqli-real-escape-string-expects-exactly-2-parameters-1-given-wh
    $position = mysql_real_escape_string($position);
    $company_desc = mysql_real_escape_string($company_desc);
    $education_and_exp = mysql_real_escape_string($education_and_exp);
    $knowledge = mysql_real_escape_string($knowledge);
    $job_summary = mysql_real_escape_string($job_summary);
    $language_certificates = mysql_real_escape_string($language_certificates);
	   //echo $job_ref . " ". $job_url . " ". $position. "\n";
		$value_to_insert = "('".$job_ref."','".$job_url."','".$name."','".$position."','".$company_desc."','".$education_and_exp."','".$knowledge."','".$job_summary."','".$language_certificates."')";
		//$sql .= "INSERT INTO jobs (job_ref,job_url) VALUES ($job_ref, $job_url)";


    if (array_key_exists($job_ref, $stack)) {
        echo "\nL'élément ". $job_ref ." existe dans le tableau\n";
    }
    else{
      //insert it into db
      $sql = "INSERT INTO jobs (JOBREF, JOBURL, NAME, POSITION, COMPANYDESC, EDUCATIONANDEXP, KNOWLEDGE, JOBSUMMARY, LANGUAGECERTIFICATES ) VALUES".$value_to_insert;


      if (mysql_query($sql) === TRUE) {
          echo "\nNew records ".$job_ref ." created successfully\n";
      } else {
          echo "Error: " . $sql . "<br>" . $conn->error;
      }

    }



}//end for loop through json



// delete the table contents
echo "\ndelete table\n";
$sql = 'DELETE FROM jobs';

if (mysql_query($sql) === TRUE) {
    echo "\nDeleting the content of the database\n";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

echo "Deleting full.json";
unlink('full.json');

//close the connection
mysql_close($conn);
 ?>
