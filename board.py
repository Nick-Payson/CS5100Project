from piece import Piece
from square import Square


class BoardState:
    "represents board state"
    board: [Square]

    def __init__(self, top_string: str, middle_string: str, bottom_string: str, squares=None):  # will do all three layers

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
