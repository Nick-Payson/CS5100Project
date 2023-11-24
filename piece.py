class Piece:
    "a gobbler"
    color: str
    size: int

    def __init__(self, c: str, s: int):
        self.color = c
        self.size = s

    def get_color(self) -> str:
        return self.color

    def get_size(self) -> int:
        return self.size

    def __str__(self) -> str:
        return self.color + str(self.size)

    def __deepcopy__(self, memodict={}):
        return Piece(self.color, self.size)
