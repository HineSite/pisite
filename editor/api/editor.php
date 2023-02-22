<?php

$SCRIPTS_DIR = __DIR__ . '/../scripts/';

function getScripts()
{
    global $SCRIPTS_DIR;

    return array_diff(scandir($SCRIPTS_DIR), array('.', '..'));
}

function getScript($filename)
{
    global $SCRIPTS_DIR;

    $handle = fopen($SCRIPTS_DIR . $filename, 'r');
    try {
        return stream_get_contents($handle);
    }
    finally {
        fclose($handle);
    }
}

function saveScript($filename, $text)
{
    global $SCRIPTS_DIR;

    $handle = null;
    try {
        $handle = fopen($SCRIPTS_DIR . $filename, 'w');

        fwrite($handle, $text);
    }
    catch (Exception $ex) {
        return $ex->getMessage();
    }
    finally {
        if ($handle) {
            fclose($handle);
        }
    }

    return "success";
}

function runScript($filename)
{
    global $SCRIPTS_DIR;

    $command = "sudo python3 ${SCRIPTS_DIR}${filename}";

    $stds = array(
        0 => array("pipe", "r"),  // stdin
        1 => array("pipe", "w"),  // stdout
        2 => array("pipe", "w"),  // stderr
    );

    $process = proc_open($command, $stds, $pipes, $SCRIPTS_DIR, null);
    try {
        if (is_resource($process)) {
            $stdout = stream_get_contents($pipes[1]);
            $stderr = stream_get_contents($pipes[2]);

            fclose($pipes[1]);
            fclose($pipes[2]);

            $exit = proc_close($process);

            $results = [
                "stdout" => $stdout,
                "stderr" => $stderr,
                "exit" => $exit
            ];

            return json_encode($results);
        }
        else {
            return "unable to process command: ${command}";
        }
    }
    catch (Exception $ex) {
        return "unable to process command: ${command} | Ex: " . $ex->getMessage();
    }
    finally {
        if (is_resource($pipes[1])) {
            fclose($pipes[1]);
        }

        if (is_resource($pipes[2])) {
            fclose($pipes[2]);
        }

        if (is_resource($process)) {
            proc_close($process);
        }
    }
}

if (isset($_GET['action'])) {
    $action = $_GET['action'];
    if ($action == 'getScript') {
        $filename = $_GET['file'];

        echo getScript($filename);
    }
    else if ($action == 'saveScript') {
        $filename = $_GET['file'];
        $text = file_get_contents('php://input');

        echo saveScript($filename, $text);
    }
    else if ($action == 'runScript') {
        $filename = $_GET['file'];
        $text = file_get_contents('php://input');

        $result = saveScript($filename, $text);
        if ($result != "success") {
            echo $result;
        }
        else {
            echo runScript($filename);
        }
    }
}
