<?php

require_once "./LedController.php";

$EOL = (php_sapi_name() === 'cli' ? PHP_EOL : "<br>");

function debug($message) {
    global $EOL;
    echo $message . $EOL;
}

debug('Testing LedController...');
debug('Warning: The led control server must be restarted before each test');

$controller = new LedController(true);

# get pre-initialized led
$led = $controller->get(28);
if ($led->r != 0 || $led->g != 0 || $led->b != 0 || $led->a != .1) {
    debug('Pre-initialized failed, got led: ' . $led->toString());
    exit;
}


# create new led, update the set, then get the led back.
$led = new Led(28, 102, 0, 102, .3);
if ($controller->set($led) == false) {
    debug('Led update returned false');
    exit;
}

$led = $controller->get(28);
if ($led->r != 102 || $led->g != 0 || $led->b != 102 || $led->a != .3) {
    debug('Led update failed, got led: ' . $led->toString());
    exit;
}

$led = $controller->readAll();
if (count($led) != 50 || $led[28]->id != 28) {
    debug("Read all leds returned unexpected results: " . json_encode($led));
    exit;
}


# clear the colors and recheck
if ($controller->clear() == false) {
    debug('clear command returned false');
}

$led = $controller->get(28);
if ($led->r != 0 || $led->g != 0 || $led->b != 0 || $led->a != .1) {
    debug('Failed to clear colors, got led: ' . $led->toString());
    exit;
}

debug('LedController Passed...');


debug('All tests passed');
