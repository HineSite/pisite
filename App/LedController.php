<?php

require_once "./Led.php";

class LedController
{
    private static $_writeAddress = './Scripts/led-socket-write';  // socket used to listen for write requests
    private static $_readAddress = './Scripts/led-socket-read';  // socket used to listed for read requests

    private $_debug = false;
    private $_eof = "";

    public function __construct(bool $debug = false)
    {
        $this->_debug = $debug;
        $this->_eof = (php_sapi_name() === 'cli' ? PHP_EOL : "<br>");
    }

    private function connect(string $address, string $message): ?string
    {
        $socket = null;
        try {
            $socket = fsockopen("unix://{$address}", -1, $errorCode, $errorMessage);
            if (!$socket) {
                $this->debug("Socket error on {$address}. Error ($errorCode): {$errorMessage}");
            } else {
                fwrite($socket, $message . PHP_EOL);

                $response = stream_get_contents($socket);

                fclose($socket);

                return $response ?? '';
            }
        }
        catch (Exception $ex) {
            $this->debug("Socket exception on {$address}. Message: " . $ex->getMessage(), $ex->getTraceAsString());
        }
        finally {
            if (is_resource($socket)) {
                fclose($socket);
            }
        }

        return null;
    }

    private function write(string $message): bool
    {
        $this->debug("Sending write request to server: {$message}");

        $response = $this->connect(self::$_writeAddress, $message);
        if ($response === null) {
            $this->debug('No response from server');
            return false;
        }

        return true;
    }

    private function read(string $message): ?array
    {
        $this->debug("Sending read request to server: {$message}");

        $response = $this->connect(self::$_readAddress, $message);
        if (!$response) {
            $this->debug('No response from server');
            return null;
        }

        $this->debug("Server response: {$response}");

        $leds = [];
        $parts = explode('|', $response);
        foreach($parts as $part) {
            $led = Led::deserialize($part);
            $leds[] = $led;
        }

        return $leds;
    }

    public function set(array $leds): bool
    {
        $message = '';
        foreach ($leds as $led) {
            if (strlen($message) > 0) {
                $message .= '|';
            }

            $message .= $led->serialize();
        }

        return $this->write($message);
    }

    public function clear(): bool
    {
        return $this->write('clear');
    }

    public function get(int $id): ?Led
    {
        $leds = $this->read(strval($id));
        if (empty($leds))
            return null;

        return $leds[0];
    }

    public function readAll(): ?array
    {
        return $this->read('all');
    }

    private function debug(string $message, string $stacktrace = null)
    {
        if ($this->_debug) {
            echo $message . $this->_eof;
            if ($stacktrace) {
                echo 'Stacktrace: ' . $stacktrace . $this->_eof;
            }
        }
    }
}
