from board import BoardState
from piece import Piece

# One Turn Win (otw) Board - a simple board where either player can win on their next move
otw_board_bottom_layer = "__ __ __ \n__ __ __ \n__ o1 b1 "
otw_board_middle_layer = "__ __ b2 \n__ __ __ \n__ __ o2 "
otw_board_top_layer = "__ o3 __ \n__ __ b3 \n__ __ __ "
OTW_BOARD = BoardState(bottom_string=otw_board_bottom_layer,
                       middle_string=otw_board_middle_layer,
                       top_string=otw_board_top_layer)
OTW_ORANGE_PIECES = [[Piece("o", 1)], [Piece("o", 2)], [Piece("o", 3)]]
OTW_BLUE_PIECES = [[Piece("b", 1)], [Piece("b", 2)], [Piece("b", 3)]]


# Starting Board - the blank starting configuration
start_board_bottom_layer = "__ __ __ \n__ __ __ \n__ __ __ "
start_board_middle_layer = "__ __ __ \n__ __ __ \n__ __ __ "
start_board_top_layer = "__ __ __ \n__ __ __ \n__ __ __ "
START_BOARD = BoardState(bottom_string=start_board_bottom_layer,
                         middle_string=start_board_middle_layer,
                         top_string=start_board_top_layer)
START_ORANGE_PIECES = None
START_BLUE_PIECES = None

# Two Turn Win (ttw) Board - blue player can win in two turns if they go next
ttw_board_bottom_layer = "__ __ __ \n__ __ __ \n__ __ __ "
ttw_board_middle_layer = "b2 __ __ \n__ __ __ \n__ __ b2 "
ttw_board_top_layer = "__ __ o3 \n__ o3 __ \n__ __ __ "
TTW_BOARD = BoardState(bottom_string=ttw_board_bottom_layer,
                       middle_string=ttw_board_middle_layer,
                       top_string=ttw_board_top_layer)
TTW_ORANGE_PIECES = [[Piece("o", 1), Piece("o", 1)], [Piece("o", 2), Piece("o", 2)], []]
TTW_BLUE_PIECES = [[Piece("b", 1), Piece("b", 1)], [], [Piece("b", 3), Piece("b", 3)]]

# Crowded Board - Board with a few pieces on it (use with orange to move)
crowded_board_bottom_layer = "o1 __ __ \n__ __ __ \nb1 __ __ "
crowded_board_middle_layer = "__ __ __ \no2 b2 b2 \n__ __ o2 "
crowded_board_top_layer = "b3 o3 o3 \n__ __ __ \n__ b3 __ "
CROWDED_BOARD = BoardState(bottom_string=crowded_board_bottom_layer,
                       middle_string=crowded_board_middle_layer,
                       top_string=crowded_board_top_layer)
CROWDED_ORANGE_PIECES = [[Piece("o", 1)], [], []]
CROWDED_BLUE_PIECES = [[Piece("b", 1)], [], []]

# Simple Board - Board with a couple pieces on it
simple_board_bottom_layer = "__ __ __ \n__ __ __ \no1 __ o1 "
simple_board_middle_layer = "__ __ __ \n__ __ __ \n__ b2 __ "
simple_board_top_layer = "__ __ __ \n__ b3 __ \n__ __ __ "
SIMPLE_BOARD = BoardState(bottom_string=simple_board_bottom_layer,
                       middle_string=simple_board_middle_layer,
                       top_string=simple_board_top_layer)
SIMPLE_ORANGE_PIECES = [[], [Piece("o", 2), Piece("o", 2)], [Piece("o", 3), Piece("o", 3)]]
SIMPLE_BLUE_PIECES = [[Piece("b", 1), Piece("b", 1)], [Piece("b", 2)], [Piece("b", 3)]]

# Low Level Board - Board with some pieces on it, all on low level
low_board_bottom_layer = "__ b1 __ \n__ __ __ \no1 b1 o1 "
low_board_middle_layer = "__ __ __ \n__ __ __ \n__ __ __ "
low_board_top_layer = "__ __ __ \n__ __ __ \n__ __ __ "
LOW_BOARD = BoardState(bottom_string=low_board_bottom_layer,
                       middle_string=low_board_middle_layer,
                       top_string=low_board_top_layer)
LOW_ORANGE_PIECES = [[], [Piece("o", 2), Piece("o", 2)], [Piece("o", 3), Piece("o", 3)]]
LOW_BLUE_PIECES = [[], [Piece("b", 2), Piece("b", 2)], [Piece("b", 3), Piece("b", 3)]]

# Middle Level Board - Board with some pieces on it, all on middle level
mid_board_bottom_layer = "__ __ __ \n__ __ __ \n__ __ __ "
mid_board_middle_layer = "__ b2 __ \n__ __ __ \no2 b2 o2 "
mid_board_top_layer = "__ __ __ \n__ __ __ \n__ __ __ "
MID_BOARD = BoardState(bottom_string=mid_board_bottom_layer,
                       middle_string=mid_board_middle_layer,
                       top_string=mid_board_top_layer)
MID_ORANGE_PIECES = [[Piece("o", 1), Piece("o", 1)], [], [Piece("o", 3), Piece("o", 3)]]
MID_BLUE_PIECES = [[Piece("b", 1), Piece("b", 1)], [], [Piece("b", 3), Piece("b", 3)]]

# High Level Board - Board with some pieces on it, all on high level
high_board_bottom_layer = "__ __ __ \n__ __ __ \n__ __ __ "
high_board_middle_layer = "__ __ __ \n__ __ __ \n__ __ __ "
high_board_top_layer = "o3 __ b3 \n__ __ o3 \n__ b3 __ "
HIGH_BOARD = BoardState(bottom_string=high_board_bottom_layer,
                       middle_string=high_board_middle_layer,
                       top_string=high_board_top_layer)
HIGH_ORANGE_PIECES = [[Piece("o", 1), Piece("o", 1)], [Piece("o", 2), Piece("o", 2)], []]
HIGH_BLUE_PIECES = [[Piece("b", 1), Piece("b", 1)], [Piece("b", 2), Piece("b", 2)], []]

#todo more eval boards, mimic good tic tac toe play?
