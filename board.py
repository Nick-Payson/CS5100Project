from piece import Piece
from square import Square
from copy import deepcopy


def piece_to_str(p: Piece) -> str:
    if p is None:
        return "__"
    else:
        return p.color + str(p.size)


class ABoardState:  # todo change board state calls to use this abstract class, make the methods

    def __str__(self):
        pass

    def won(self, c: str) -> bool:
        pass

    def can_place_piece(self, row: int, col: int, p: Piece) -> bool:
        pass

    def place_piece_at(self, row: int, col: int, p: Piece) -> bool:
        pass

    def get_piece_at(self, row: int, col: int) -> Piece:
        pass

    def remove_piece_at(self, row: int, col: int) -> Piece:
        pass

    def get_board_strings(self) -> [str]:
        pass

    def __deepcopy__(self, memodict={}):
        pass

    def doTheHash(self, blue_to_move):  # todo __eq__() too
        # hash itself with move boolean
        pass

    def produce_symmetry(self, symmetry_type: str):
        pass


class BoardState(ABoardState):
    "represents board state"
    board: [Square]

    def __init__(self, top_string: str, middle_string: str, bottom_string: str,
                 squares=None):  # will do all three layers

        if squares is not None:
            self.board = squares
        else:

            self.board = [[Square(), Square(), Square()],
                          [Square(), Square(), Square()],
                          [Square(), Square(), Square()]]
            strings = [bottom_string, middle_string, top_string]
            for s in strings:
                rows = s.split("\n")
                for i in range(3):
                    row = rows[i]
                    pieces = row.split(" ")
                    for j in range(3):
                        if pieces[j] != "__":
                            self.board[i][j].add_piece(Piece(c=pieces[j][0:1:1], s=int(pieces[j][1:2:1])))

    def __str__(self) -> str:
        the_str = "--------\n"
        for row in range(3):
            for col in range(3):
                the_str = the_str + self.board[row][col].__str__() + " "
            the_str = the_str + "\n"
        the_str = the_str + "--------\n"
        return the_str

    def doTheHash(self, blue_to_move):
        board_strings = self.get_board_strings()
        return hash(board_strings[0] + board_strings[1] + board_strings[2] + str(blue_to_move))

    def won(self, c: str) -> bool:
        # c = "o" or "b", should be one character color representing string
        for row in range(3):
            rowWin = True
            colWin = True
            for col in range(3):
                if str(self.board[row][col])[0:1:1] != c:
                    rowWin = False
                if str(self.board[col][row])[0:1:1] != c:
                    colWin = False
            if rowWin or colWin:
                return True

        diagonal_win = True
        other_diagonal_win = True
        for i in range(3):
            if str(self.board[i][i])[0:1:1] != c:
                diagonal_win = False
            if str(self.board[i][2 - i])[0:1:1] != c:
                other_diagonal_win = False
        return diagonal_win or other_diagonal_win

    def can_place_piece(self, row: int, col: int, p: Piece) -> bool:
        return self.board[row][col].can_add_piece(p)

    def place_piece_at(self, row: int, col: int, p: Piece) -> bool:
        return self.board[row][col].add_piece(p)

    def get_piece_at(self, row: int, col: int) -> Piece:
        return self.board[row][col].get_top_piece()

    def remove_piece_at(self, row: int, col: int) -> Piece:
        return self.board[row][col].remove_top_piece()

    def get_board_strings(self) -> [str]:

        new_board_strings = ["", "", ""]

        for s in range(3):
            layer_string = ""
            for i in range(3):
                for j in range(3):
                    the_piece = self.board[i][j].get_piece_with_size(s)
                    if the_piece is not None:
                        add_str = str(the_piece) + " "
                    else:
                        add_str = "__ "
                    layer_string += add_str
                if i != 2:
                    layer_string += "\n"
            new_board_strings[s] = layer_string

        return new_board_strings

    def __deepcopy__(self, memodict={}):
        new_squares = []
        for i in range(3):
            row: [Square] = []
            for j in range(3):
                row.append(self.board[i][j].__deepcopy__())
            new_squares.append(row)

        return BoardState("", "", "", new_squares)

    def produce_symmetry(self, symmetry_type: str):
        # return a new board with the chosen symmetry_type
        old_top_left = self.board[0][0]
        old_top_middle = self.board[0][1]
        old_top_right = self.board[0][2]
        old_mid_left = self.board[1][0]
        old_middle = self.board[1][1]
        old_mid_right = self.board[1][2]
        old_bot_left = self.board[2][0]
        old_bot_middle = self.board[2][1]
        old_bot_right = self.board[2][2]

        if symmetry_type == "Initial":
            # initial board hash: type = "Initial"
            new_top_left = old_top_left.__deepcopy__()
            new_top_middle = old_top_middle.__deepcopy__()
            new_top_right = old_top_right.__deepcopy__()
            new_mid_left = old_mid_left.__deepcopy__()
            new_middle = old_middle.__deepcopy__()
            new_mid_right = old_mid_right.__deepcopy__()
            new_bot_left = old_bot_left.__deepcopy__()
            new_bot_middle = old_bot_middle.__deepcopy__()
            new_bot_right = old_bot_right.__deepcopy__()
        elif symmetry_type == "Flip X":
            # flip board across vertical axis: type = "Flip X"
            new_top_left = old_top_right.__deepcopy__()
            new_top_middle = old_top_middle.__deepcopy__()
            new_top_right = old_top_left.__deepcopy__()
            new_mid_left = old_mid_right.__deepcopy__()
            new_middle = old_middle.__deepcopy__()
            new_mid_right = old_mid_left.__deepcopy__()
            new_bot_left = old_bot_right.__deepcopy__()
            new_bot_middle = old_bot_middle.__deepcopy__()
            new_bot_right = old_bot_left.__deepcopy__()
        elif symmetry_type == "Flip Y":
            # flip board across horizontal axis: type = "Flip Y"
            new_top_left = old_bot_left.__deepcopy__()
            new_top_middle = old_bot_middle.__deepcopy__()
            new_top_right = old_bot_right.__deepcopy__()
            new_mid_left = old_mid_left.__deepcopy__()
            new_middle = old_middle.__deepcopy__()
            new_mid_right = old_mid_right.__deepcopy__()
            new_bot_left = old_top_left.__deepcopy__()
            new_bot_middle = old_top_middle.__deepcopy__()
            new_bot_right = old_top_right.__deepcopy__()
        elif symmetry_type == "Rotate 90":
            # rotate 90 degrees clockwise: type = "Rotate 90"
            new_top_left = old_bot_left.__deepcopy__()
            new_top_middle = old_mid_left.__deepcopy__()
            new_top_right = old_top_left.__deepcopy__()
            new_mid_left = old_bot_middle.__deepcopy__()
            new_middle = old_middle.__deepcopy__()
            new_mid_right = old_top_middle.__deepcopy__()
            new_bot_left = old_bot_right.__deepcopy__()
            new_bot_middle = old_mid_right.__deepcopy__()
            new_bot_right = old_top_right.__deepcopy__()
        elif symmetry_type == "Rotate 180":
            # rotate 180 degrees clockwise: type = "Rotate 180"
            new_top_left = old_bot_right.__deepcopy__()
            new_top_middle = old_bot_middle.__deepcopy__()
            new_top_right = old_bot_left.__deepcopy__()
            new_mid_left = old_mid_right.__deepcopy__()
            new_middle = old_middle.__deepcopy__()
            new_mid_right = old_mid_left.__deepcopy__()
            new_bot_left = old_top_right.__deepcopy__()
            new_bot_middle = old_top_middle.__deepcopy__()
            new_bot_right = old_top_left.__deepcopy__()
        elif symmetry_type == "Rotate 270":
            # rotate 270 degrees clockwise: type = "Rotate 270"
            new_top_left = old_top_right.__deepcopy__()
            new_top_middle = old_mid_right.__deepcopy__()
            new_top_right = old_bot_right.__deepcopy__()
            new_mid_left = old_top_middle.__deepcopy__()
            new_middle = old_middle.__deepcopy__()
            new_mid_right = old_bot_middle.__deepcopy__()
            new_bot_left = old_top_left.__deepcopy__()
            new_bot_middle = old_mid_left.__deepcopy__()
            new_bot_right = old_bot_left.__deepcopy__()
        elif symmetry_type == "Diagonal Flip y=x":
            # diagonal flip across y=x: type = "Diagonal Flip y=x"
            new_top_left = old_bot_right.__deepcopy__()
            new_top_middle = old_mid_right.__deepcopy__()
            new_top_right = old_top_right.__deepcopy__()
            new_mid_left = old_bot_middle.__deepcopy__()
            new_middle = old_middle.__deepcopy__()
            new_mid_right = old_top_middle.__deepcopy__()
            new_bot_left = old_bot_left.__deepcopy__()
            new_bot_middle = old_mid_left.__deepcopy__()
            new_bot_right = old_top_left.__deepcopy__()
        elif symmetry_type == "Diagonal Flip y=-x":
            # diagonal flip across y=-x: "Diagonal Flip y=-x"
            new_top_left = old_top_left.__deepcopy__()
            new_top_middle = old_mid_left.__deepcopy__()
            new_top_right = old_bot_left.__deepcopy__()
            new_mid_left = old_top_middle.__deepcopy__()
            new_middle = old_middle.__deepcopy__()
            new_mid_right = old_bot_middle.__deepcopy__()
            new_bot_left = old_top_right.__deepcopy__()
            new_bot_middle = old_mid_right.__deepcopy__()
            new_bot_right = old_bot_right.__deepcopy__()
        else:
            return Exception("Invalid symmetry type: " + symmetry_type)
        new_squares = [[new_top_left, new_top_middle, new_top_right],
                       [new_mid_left, new_middle, new_mid_right],
                       [new_bot_left, new_bot_middle, new_bot_right]]
        return BoardState(top_string="", middle_string="", bottom_string="", squares=new_squares)


class BitBoardState(ABoardState):

    def __init__(self, top_string: str, middle_string: str, bottom_string: str, o_top_board=None, o_middle_board=None,
                 o_bottom_board=None, b_top_board=None, b_middle_board=None, b_bottom_board=None):
        if o_top_board is not None:  # should use all six if using any non-string
            self.orange_board = [o_bottom_board, o_middle_board, o_top_board]
            self.blue_board = [b_bottom_board, b_middle_board, b_top_board]
            # board is bottom, middle, top
            return

        self.orange_board = [0b000_000_000] * 3
        self.blue_board = [0b000_000_000] * 3

        strings = [bottom_string, middle_string, top_string]
        for level in range(3):
            s = strings[level]
            rows = s.split("\n")

            for i in range(3):
                row = rows[i]
                pieces = row.split(" ")

                for j in range(3):
                    index = (3 * i + j)
                    string_rep = "0b"

                    if "b" in pieces[j]:
                        for x in range(9):
                            if x == index:
                                string_rep += "1"
                            else:
                                string_rep += "0"

                        # todo make sure right string generated and board strings stay in binary format
                        self.blue_board[level] = self.blue_board[level] | int(string_rep, 2)

                    elif "o" in pieces[j]:
                        for x in range(9):
                            if x == index:
                                string_rep += "1"
                            else:
                                string_rep += "0"

                        self.orange_board[level] = self.orange_board[level] | int(string_rep, 2)

    def __str__(self) -> str:
        the_str = "--------\n"
        for row in range(3):
            for col in range(3):
                index = (3 * row + col)
                p = self.get_piece_at(row, col)
                the_str = the_str + piece_to_str(p=p) + " "
            the_str = the_str + "\n"
        the_str = the_str + "--------\n"
        return the_str

    def won(self, c: str) -> bool:

        if c == "b":
            good_board = self.blue_board
            bad_board = self.orange_board
        else:
            good_board = self.orange_board
            bad_board = self.blue_board

        c_pieces = 0b000000000
        c_pieces = c_pieces | good_board[0]  # add small good pieces
        c_pieces = c_pieces ^ (c_pieces & bad_board[1])  # remove pieces covered by middle bad pieces
        c_pieces = c_pieces | good_board[1]  # add middle good pieces
        c_pieces = c_pieces ^ (c_pieces & bad_board[2])  # remove pieces covered by large bad pieces
        c_pieces = c_pieces | good_board[2]  # add large good pieces

        win_conditions = [0b111000000, 0b000111000, 0b000000111,
                          0b100100100, 0b010010010, 0b001001001,
                          0b100010001, 0b001010100]

        for w in win_conditions:
            if c_pieces & w == w:
                return True

        return False

    def can_place_piece(self, row: int, col: int, p: Piece) -> bool:
        s = p.size
        index = (3 * row + col)
        string_rep = "0b"
        for i in range(9):
            if index == i:
                string_rep += "1"
            else:
                string_rep += "0"

        for i in range(s - 1, 3):
            if self.blue_board[i] & int(string_rep, 2) != 0:  # matching piece location with unacceptable size
                return False
            if self.orange_board[i] & int(string_rep, 2) != 0:
                return False

        return True

    def place_piece_at(self, row: int, col: int, p: Piece):
        # old was: self.board[row][col].add_piece(p)
        s = p.size
        c = p.color
        index = (3 * row + col)
        string_rep = "0b"
        for i in range(9):
            if index == i:
                string_rep += "1"
            else:
                string_rep += "0"
        if c == "b":
            self.blue_board[s - 1] = self.blue_board[s - 1] | int(string_rep, 2)
        if c == "o":
            self.orange_board[s - 1] = self.orange_board[s - 1] | int(string_rep, 2)
        return

    def get_piece_at(self, row: int, col: int) -> Piece:
        # old was self.board[row][col].get_top_piece()
        index = (3 * row + col)
        string_rep = "0b"
        for i in range(9):
            if index == i:
                string_rep += "1"
            else:
                string_rep += "0"

        for size in range(3):
            if self.orange_board[2 - size] & int(string_rep, 2) != 0:
                return Piece(c="o", s=3 - size)
            if self.blue_board[2 - size] & int(string_rep, 2) != 0:
                return Piece(c="b", s=3 - size)

        return None

    def remove_piece_at(self, row: int, col: int) -> Piece:
        # old was self.board[row][col].remove_top_piece()
        index = (3 * row + col)
        string_rep = "0b"
        for i in range(9):
            if index == i:
                string_rep += "1"
            else:
                string_rep += "0"

        for size in range(3):
            if self.orange_board[2 - size] & int(string_rep, 2) != 0:
                self.orange_board[2 - size] = self.orange_board[2 - size] ^ int(string_rep, 2)
                return Piece(c="o", s=3 - size)
            if self.blue_board[2 - size] & int(string_rep, 2) != 0:
                self.blue_board[2 - size] = self.blue_board[2 - size] ^ int(string_rep, 2)
                return Piece(c="b", s=3 - size)

        return None

    def get_board_strings(self) -> [str]:
        new_board_strings = ["", "", ""]
        for s in range(3):
            layer_string = ""
            for i in range(3):
                for j in range(3):
                    string_rep = "0b"
                    index = (3 * i + j)
                    for q in range(9):
                        if index == q:
                            string_rep += "1"
                        else:
                            string_rep += "0"

                    the_piece = None
                    if self.orange_board[s] & int(string_rep, 2) != 0:
                        the_piece = Piece(c="o", s=s + 1)
                    if self.blue_board[s] & int(string_rep, 2) != 0:
                        the_piece = Piece(c="b", s=s + 1)

                    add_str = piece_to_str(the_piece) + " "
                    layer_string += add_str
                if i != 2:
                    layer_string += "\n"
            new_board_strings[s] = layer_string
        return new_board_strings

    def __deepcopy__(self, memodict={}):
        new_orange_top = deepcopy(self.orange_board[2])
        new_orange_middle = deepcopy(self.orange_board[1])
        new_orange_bottom = deepcopy(self.orange_board[0])
        new_blue_top = deepcopy(self.blue_board[2])
        new_blue_middle = deepcopy(self.blue_board[1])
        new_blue_bottom = deepcopy(self.blue_board[0])

        return BitBoardState(top_string="", middle_string="", bottom_string="",
                             o_top_board=new_orange_top, o_middle_board=new_orange_middle,
                             o_bottom_board=new_orange_bottom, b_bottom_board=new_blue_bottom,
                             b_middle_board=new_blue_middle, b_top_board=new_blue_top)

    def doTheHash(self, blue_to_move):
        return hash((self.blue_board[0], self.blue_board[1], self.blue_board[2],
                     self.orange_board[0], self.orange_board[1], self.orange_board[2],
                     blue_to_move))

    def produce_symmetry(self, symmetry_type: str):
        ot = deepcopy(self.orange_board[2])
        om = deepcopy(self.orange_board[1])
        ob = deepcopy(self.orange_board[0])
        bt = deepcopy(self.blue_board[2])
        bm = deepcopy(self.blue_board[1])
        bb = deepcopy(self.blue_board[0])

        # initial board hash: type = "Initial"
        n_ot = ot
        n_om = om
        n_ob = ob
        n_bt = bt
        n_bm = bm
        n_bb = bb
        if symmetry_type == "Initial":
            pass
        elif symmetry_type == "Flip X":
            # flip board across vertical axis: type = "Flip X"
            n_ot = self.bitboardFlipX(ot)
            n_om = self.bitboardFlipX(om)
            n_ob = self.bitboardFlipX(ob)
            n_bt = self.bitboardFlipX(bt)
            n_bm = self.bitboardFlipX(bm)
            n_bb = self.bitboardFlipX(bb)

        elif symmetry_type == "Flip Y":
            # flip board across horizontal axis: type = "Flip Y"
            n_ot = self.bitboardFlipY(ot)
            n_om = self.bitboardFlipY(om)
            n_ob = self.bitboardFlipY(ob)
            n_bt = self.bitboardFlipY(bt)
            n_bm = self.bitboardFlipY(bm)
            n_bb = self.bitboardFlipY(bb)

        elif symmetry_type == "Rotate 90":
            # rotate 90 degrees clockwise: type = "Rotate 90"
            n_ot = self.bitboardRotate90(ot)
            n_om = self.bitboardRotate90(om)
            n_ob = self.bitboardRotate90(ob)
            n_bt = self.bitboardRotate90(bt)
            n_bm = self.bitboardRotate90(bm)
            n_bb = self.bitboardRotate90(bb)
        elif symmetry_type == "Rotate 180":
            # rotate 180 degrees clockwise: type = "Rotate 180"
            for i in range(2):
                n_ot = self.bitboardRotate90(n_ot)
                n_om = self.bitboardRotate90(n_om)
                n_ob = self.bitboardRotate90(n_ob)
                n_bt = self.bitboardRotate90(n_bt)
                n_bm = self.bitboardRotate90(n_bm)
                n_bb = self.bitboardRotate90(n_bb)

        elif symmetry_type == "Rotate 270":
            # rotate 270 degrees clockwise: type = "Rotate 270"
            for i in range(3):
                n_ot = self.bitboardRotate90(n_ot)
                n_om = self.bitboardRotate90(n_om)
                n_ob = self.bitboardRotate90(n_ob)
                n_bt = self.bitboardRotate90(n_bt)
                n_bm = self.bitboardRotate90(n_bm)
                n_bb = self.bitboardRotate90(n_bb)

        elif symmetry_type == "Diagonal Flip y=x":
            # diagonal flip across y=x: type = "Diagonal Flip y=x"
            n_ot = self.bitboardFlip_y_eq_x(ot)
            n_om = self.bitboardFlip_y_eq_x(om)
            n_ob = self.bitboardFlip_y_eq_x(ob)
            n_bt = self.bitboardFlip_y_eq_x(bt)
            n_bm = self.bitboardFlip_y_eq_x(bm)
            n_bb = self.bitboardFlip_y_eq_x(bb)

        elif symmetry_type == "Diagonal Flip y=-x":
            # diagonal flip across y=-x: "Diagonal Flip y=-x"
            n_ot = self.bitboardFlip_y_eq_neg_x(ot)
            n_om = self.bitboardFlip_y_eq_neg_x(om)
            n_ob = self.bitboardFlip_y_eq_neg_x(ob)
            n_bt = self.bitboardFlip_y_eq_neg_x(bt)
            n_bm = self.bitboardFlip_y_eq_neg_x(bm)
            n_bb = self.bitboardFlip_y_eq_neg_x(bb)

        else:
            return Exception("Invalid symmetry type: " + symmetry_type)

        return BitBoardState(top_string="", middle_string="", bottom_string="",
                             o_top_board=n_ot, o_middle_board=n_om, o_bottom_board=n_ob,
                             b_top_board=n_bt, b_middle_board=n_bm, b_bottom_board=n_bb)

    def bitboardFlipX(self, bitboard):
        left_col = bitboard & 0b100100100
        mid_col = bitboard & 0b010010010
        right_col = bitboard & 0b001001001
        new_right = left_col >> 2
        new_left = right_col << 2

        return 0b000000000 | new_left | new_right | mid_col

    def bitboardFlipY(self, bitboard):
        top_row = bitboard & 0b111000000
        mid_row = bitboard & 0b000111000
        bot_row = bitboard & 0b000000111
        new_top = bot_row << 6
        new_bot = top_row >> 6

        return 0b000000000 | new_top | new_bot | mid_row

    def bitboardRotate90(self, bitboard):
        top_left = bitboard & 0b100000000
        top_mid = bitboard & 0b010000000
        top_right = bitboard & 0b001000000
        mid_left = bitboard & 0b000100000
        mid_mid = bitboard & 0b000010000
        mid_right = bitboard & 0b000001000
        bot_left = bitboard & 0b000000100
        bot_mid = bitboard & 0b000000010
        bot_right = bitboard & 0b000000001

        ntl = bot_left << 6
        ntm = mid_left << 2
        ntr = top_left >> 2
        nml = bot_mid << 4
        nmr = top_mid >> 4
        nbl = bot_right << 2
        nbm = mid_right >> 2
        nbr = top_right >> 6

        return 0b000000000 | ntl | ntm | ntr | nml | mid_mid | nmr | nbl | nbm | nbr

    def bitboardFlip_y_eq_x(self, bitboard):
        top_left = bitboard & 0b100000000
        top_mid = bitboard & 0b010000000
        top_right = bitboard & 0b001000000
        mid_left = bitboard & 0b000100000
        mid_mid = bitboard & 0b000010000
        mid_right = bitboard & 0b000001000
        bot_left = bitboard & 0b000000100
        bot_mid = bitboard & 0b000000010
        bot_right = bitboard & 0b000000001

        ntl = bot_right << 8
        ntm = mid_right << 4
        ntr = top_right
        nml = bot_mid << 4
        nmr = top_mid >> 4
        nbl = bot_left
        nbm = mid_left >> 4
        nbr = top_left >> 8

        return 0b000000000 | ntl | ntm | ntr | nml | mid_mid | nmr | nbl | nbm | nbr

    def bitboardFlip_y_eq_neg_x(self, bitboard):
        top_left = bitboard & 0b100000000
        top_mid = bitboard & 0b010000000
        top_right = bitboard & 0b001000000
        mid_left = bitboard & 0b000100000
        mid_mid = bitboard & 0b000010000
        mid_right = bitboard & 0b000001000
        bot_left = bitboard & 0b000000100
        bot_mid = bitboard & 0b000000010
        bot_right = bitboard & 0b000000001

        ntl = top_left
        ntm = mid_left << 2
        ntr = bot_left << 4
        nml = top_mid >> 2
        nmr = bot_mid << 2
        nbl = top_right >> 4
        nbm = mid_right >> 2
        nbr = bot_right

        return 0b000000000 | ntl | ntm | ntr | nml | mid_mid | nmr | nbl | nbm | nbr
