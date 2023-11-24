from piece import Piece

class Square:
    "a square on the board"
    pieces: [Piece] # three pieces, last one is largest
    max_current_size: int

    def __init__(self, p: [Piece] = [None, None, None]):
        self.pieces = [None, None, None]
        self.max_current_size = 0
        for _p in p:
            if _p is not None:
                self.add_piece(_p)

    def get_pieces(self) -> [Piece]:
        return self.pieces

    def add_piece(self, p: Piece):
        self.pieces[p.size - 1] = p
        self.max_current_size = p.size

    def can_add_piece(self, p: Piece) -> bool:
        return p.size > self.max_current_size

    def get_top_piece(self) -> Piece:
        p = None
        for i in range(3):
            if self.pieces[i] is not None:
                p = self.pieces[i]
        return p

    def get_piece_with_size(self, size: int) -> Piece:
        return self.pieces[size]

    def remove_top_piece(self) -> Piece:
        for i in range(3):
            if self.pieces[2 - i] is not None:
                p = self.pieces[2 - i]
                self.pieces[2 - i] = None
                return p
        return None

    def __str__(self) -> str:
        p = self.get_top_piece()
        if p is not None:
            return str(p)
        return "__"

    def __deepcopy__(self, memodict={}):
        pieces = []
        for p in self.pieces:
            if p is None:
                pieces.append(None)
            else:
                pieces.append(p.__deepcopy__())
        return Square(p=pieces)
