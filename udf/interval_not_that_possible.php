#! /usr/bin/env php
<?php

while (FALSE !== ($line = fgets(STDIN))) {
   $input = json_decode($line);
   $formation = $input->{"relations_formationtemporal_global.t0.formation"};
   $interval1 = $input->{"relations_formationtemporal_global.t0.interval"};
   $interval2 = $input->{"relations_formationtemporal_global.t1.interval"};

   $components1 = explode("|", $interval1);
   $components2 = explode("|", $interval2);

   $small1 = floatval($components1[2]);
   $large1 = floatval($components1[1]);
   $small2 = floatval($components2[2]);
   $large2 = floatval($components2[1]);

   if($small1 > $large2 + 50){
   	  $output = array('formation' => $formation, 'interval1' => $interval1, 'interval2' => $interval2);
   	  echo json_encode($output) . "\n";
   }

   if($small2 > $large1 + 50){
   	  $output = array('formation' => $formation, 'interval1' => $interval1, 'interval2' => $interval2);
   	  echo json_encode($output) . "\n";
   }
   
   if(max($large1, $large2) - min($small1, $small2) > 50 && ($large2-$small2) < 50 && ($large1-$small1) < 50 ){
        $output = array('formation' => $formation, 'interval1' => $interval1, 'interval2' => $interval2);
        echo json_encode($output) . "\n";
   }
   

}

?>