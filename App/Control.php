<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

$submitAction = $_POST['SubmitAction'];
if ($submitAction === "restart") {
  echo "restarting<br>";
  echo shell_exec("sudo python3 ./Scripts/shutdown.py");
  echo shell_exec("sudo shutdown -r 0");
}
else if ($submitAction === "shutdown") {
  echo "shutting down<br>";
  echo shell_exec("sudo python3 ./Scripts/shutdown.py");
  echo shell_exec("sudo shutdown -h 0");
}


header('Location: ' . $_SERVER['HTTP_REFERER']);

//echo "Ic Ur Ip: " . $_SERVER['REMOTE_ADDR'];
