<?php

class LedController
{
    private static string $_writeAddress = '/tmp/led-socket-write';  // socket used to listen for write requests
    private static string $_readAddress = '/tmp/led-socket-read';  // socket used to listed for read requests

    private function connect(string $address, string $message): string | null
    {
        $socket = fsockopen("udp://{$address}", error_code: $errorCode, error_message: $errorMessage);
        if (!$socket) {
            echo "socket connection error error on {$address}. Error ($errorCode): {$errorMessage}";
            return null;
        } else {
            fwrite($socket, $message);

            $response = stream_get_contents($socket);

            fclose($socket);
        }

        return $response;
    }

    private function write(string $message): bool
    {
        $response = $this->connect(LedController::$_writeAddress, $message);
        return !($response == null);
    }

    private function read(string $message): array | null
    {
        $response = $this->connect(LedController::$_readAddress, $message);
        if (!$response)
            return null;

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
}
