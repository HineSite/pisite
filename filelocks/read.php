<?php

$filename = "./test.txt";
$filename = "/tmp/test.txt";

$handle = fopen($filename, 'r');

echo "waiting for lock\n";
flock($handle,  LOCK_SH);

echo "locked\n";
echo "read: " . fread($handle, filesize($filename));

sleep(5);

flock($handle, LOCK_UN);
fclose($handle);
echo "unlocked\n";

