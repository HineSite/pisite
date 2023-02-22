<?php

$filename = "./test.txt";
$filename = "/tmp/test.txt";

$handle = fopen($filename, 'c');

echo "waiting for lock\n";
flock($handle, LOCK_EX);

echo "locked\n";
sleep(5);

ftruncate($handle, 0);
fwrite($handle, "php\n");

flock($handle, LOCK_UN);
fclose($handle);
echo "unlocked\n";

