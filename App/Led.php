<?php

class Led
{
    public ?int $id;
    public int $r = 0;
    public int $g = 0;
    public int $b = 0;
    public float $a = .1;

    public function __construct(?int $id = null, int $r = 0, int $g = 0, int $b = 0, float $a = .1)
    {
        $this->id = $id;
        $this->r = $r;
        $this->g = $g;
        $this->b = $b;
        $this->a = $a;
    }

    public function array(): array
    {
        return [
            $this->id,
            $this->r,
            $this->g,
            $this->b,
            $this->a,
        ];
    }

    public function toString(): string
    {
        return "{$this->id}: ({$this->r}, {$this->g}, {$this->b}, {$this->a})";
    }

    public function serialize(): string
    {
        return "{$this->id},{$this->r},{$this->g},{$this->b},{$this->a}";
    }

    public static function deserialize(string $data): Led | null
    {
        $parts = explode(',', $data);
        if (count($parts) != 5)
            return null;

        return new Led(
            id:(is_numeric($parts[0]) ? intval($parts[0]) : null),
            r:intval($parts[1]),
            g:intval($parts[2]),
            b:intval($parts[3]),
            a:floatval($parts[4])
        );
    }

    public static function fromArray(array $data): Led | null
    {
        return new Led(
            id:(is_numeric($data[0]) ? intval($data[0]) : null),
            r:intval($data[1]),
            g:intval($data[2]),
            b:intval($data[3]),
            a:floatval($data[4])
        );
    }
}
