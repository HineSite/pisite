<?php

class Led
{
    public $id;
    public $r = 0;
    public $g = 0;
    public $b = 0;
    public $a = .1;

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

    public static function deserialize(string $data): ?Led
    {
        $parts = explode(',', $data);
        if (count($parts) != 5)
            return null;

        return new Led(
            (is_numeric($parts[0]) ? intval($parts[0]) : null),
            intval($parts[1]),
            intval($parts[2]),
            intval($parts[3]),
            floatval($parts[4])
        );
    }

    public static function fromArray(array $data): ?Led
    {
        return new Led(
            (is_numeric($data[0]) ? intval($data[0]) : null),
            intval($data[1]),
            intval($data[2]),
            intval($data[3]),
            floatval($data[4])
        );
    }
}
