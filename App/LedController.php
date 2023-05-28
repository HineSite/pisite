<?php

require_once "./led.php";

class LedController
{
    private static string $_writeAddress = '/tmp/led-socket-write';  // socket used to listen for write requests
    private static string $_readAddress = '/tmp/led-socket-read';  // socket used to listed for read requests
    private static int $_chunkSite = 2048;

    private bool $_debug = false;
    private string $_eof = "";

    public function __construct(bool $debug = false)
    {
        $this->_debug = $debug;
        $this->_eof = (php_sapi_name() === 'cli' ? PHP_EOL : "<br>");
    }

    private function connect(string $address, string $message): string | null
    {
        $socket = null;
        try {
            $socket = fsockopen("unix://{$address}", error_code: $errorCode, error_message: $errorMessage);
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

    private function read(string $message): array | null
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

    public function set(Led $led): bool
    {
        return $this->write($led->serialize());
    }

    public function clear(): bool
    {
        return $this->write('clear');
    }

    public function get(int $id): Led | null
    {
        $leds = $this->read(strval($id));
        if (empty($leds))
            return null;

        return $leds[0];
    }

    public function get_all(): array
    {
        return $this->read('');
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
