<?php

$action = $_GET['action'];
if ($action == 'write') {
    $led = $_GET['led'];
    $color = explode(',', $_GET['color']);

    echo shell_exec("sudo python3 ./Scripts/led-state.py write ${led} ${color[0]} ${color[1]} ${color[2]}");
}
else if ($action == 'update') {
    $leds = $_GET['leds'];

    echo shell_exec("sudo python3 ./Scripts/led-state.py update '${leds}'");
    //echo "sudo python3 ./Scripts/led-state.py update '${leds}'";

}
