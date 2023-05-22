
class Led:
    id: int = None
    r: int = 0
    g: int = 0
    b: int = 0
    a: float = .1

    def __init__(self, id: int = None, r: int = 0, g: int = 0, b: int = 0, a: float = .1):
        self.id = id
        self.r = r
        self.g = g
        self.b = b
        self.a = a
    # end_init

    def array(self) -> tuple[int, int, int, float]:
        return self.r, self.g, self.b, self.a
    # end_init

    def to_string(self) -> str:
        return '{id}: ({r}, {g}, {b}, {a})'.format(id=self.id, r=self.r, g=self.g, b=self.b, a=self.a)
    # end_init

    def serialize(self) -> str:
        return '{id},{r},{g},{b},{a}'.format(id=self.id, r=self.r, g=self.g, b=self.b, a=self.a)
    # end_init

    @staticmethod
    def deserialize(data: str):
        parts = data.split(',')
        if len(parts) != 5:
            return None

        try:
            return Led(
                id=None if parts[0] == 'None' else int(parts[0]),
                r=int(parts[1]),
                g=int(parts[2]),
                b=int(parts[3]),
                a=float(parts[4])
            )
        except (TypeError, ValueError):
            return None
        # end_try
    # end_init
# end_color
