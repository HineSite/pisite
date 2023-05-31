<?php
error_reporting(E_ALL);
ini_set('display_errors', '1');

require_once "./LedController.php";

$controller = new LedController();

$action = $_GET['action'];
if ($action == 'write') {
    $ledString = json_decode($_GET['leds']);

    $leds = [];
    if (is_array($ledString[0])) {
        foreach ($ledString as $led) {
            $leds[] = Led::fromArray($led);
        }
    }
    else {
        $leds[] = Led::fromArray($ledString);
    }

    $controller->set($leds);
}
if ($action == 'clear') {
    $controller->clear();
}
else if ($action == 'read') {
    $leds = $controller->readAll();
    echo  json_encode($leds);
}
