import copy

from piece import Piece
from board import ABoardState

class GameState:  # Doing this to bypass the fact that Agent and GameState depend on each other
    pass


class Agent:
    """
    An agent must define a getAction method, represents a player in the Gobblet Gobblers game
    Blue player is agent 0
    Orange player is agent 1
    """

    def __init__(self, pieces, color="b", evaluationFunction=lambda x: 0):
        self.color = color  # color of the pieces
        self.evaluationFunction = evaluationFunction
        if pieces is not None:
            self.pieces = pieces  # list of piece objects for the agent to place
        else:
            self.pieces = []
            for i in range(3):
                piece_list = []
                for j in range(2):
                    piece_list.append(Piece(c=self.color, s=i + 1))
                self.pieces.append(piece_list)

    def getColor(self):
        return self.color

    def setEvalFunction(self, evaluationFunction):
        self.evaluationFunction = evaluationFunction

    def setPieces(self, pieces: [[Piece]]):
        self.pieces = pieces

    def setColor(self, color: str):
        self.color = color

    def getAction(self, gameState: GameState):
        """
        The Agent will receive a GameState and
        must return an action formatted as [(coordinates of piece to be moved), (coordinates of new location)]
        (-1, -1) will correspond to a new piece of size one
        (-2, -2) will correspond to a new piece of size two
        (-3, -3) will correspond to a new piece of size three
        """

    def zeroEvaluationFunction(self, state: GameState) -> float:
        """
        Always return 0
        """
        return 0

    def winConditionEvaluationFunction(self, state: GameState) -> float:
        """
        Return infinite value for win or loss, 0 otherwise
        """
        if state.blueWin():
            if self.color == "b":
                return float("inf")
            return float("-inf")
        elif state.orangeWin():
            if self.color == "o":
                return float("inf")
            return float("-inf")
        return 0

    def topLayerEvaluationFunction(self, state: GameState) -> float:
        wc = self.winConditionEvaluationFunction(state=state)
        if wc != 0:
            return wc

        sum_pieces = 0
        for i in range(3):
            for j in range(3):
                p = state.board.get_piece_at(i,j)
                if p is None:
                    val = 0
                else:
                    val = 1
                    if p.get_color() != self.color:
                        val *= -1
                sum_pieces += val
        return sum_pieces

    def topLayerWeightedSizeEvaluationFunction(self, state: GameState) -> float:
        wc = self.winConditionEvaluationFunction(state=state)
        if wc != 0:
            return wc

        sum_pieces = 0
        for i in range(3):
            for j in range(3):
                p = state.board.get_piece_at(i,j)
                if p is None:
                    val = 0
                else:
                    val = p.get_size()
                    if p.get_color() != self.color:
                        val *= -1
                sum_pieces += val
        return sum_pieces

    def threatBasedEvaluationFunction(self, state: GameState) -> float: #todo change to work with bitboard representation too
        wc = self.winConditionEvaluationFunction(state=state)
        if wc != 0:
            return wc

        return state.board.threatBasedEval(self.color)

    def topLayerPieceLocationEvaluationFunction(self, state: GameState) -> float:
        wc = self.winConditionEvaluationFunction(state=state)
        if wc != 0:
            return wc

        location_weights = [[0.9, 0.8, 0.9], [0.8, 1, 0.8], [0.9, 0.8, 0.9]]

        sum_pieces = 0
        for i in range(3):
            for j in range(3):
                p = state.board.get_piece_at(i, j)
                if p is None:
                    val = 0
                else:
                    val = p.get_size()
                    if p.get_color() != self.color:
                        val *= -1
                val *= location_weights[i][j]
                sum_pieces += val
        return sum_pieces


    def handEvaluationFunction(self, state: GameState) -> float:
        wc = self.winConditionEvaluationFunction(state=state)
        if wc != 0:
            return wc

        value = 0
        for i in range(3):
            for p in self.pieces[i]:
                if p is not None:
                    value -= p.size
        return value

    def threatAndLocationEvalFunction(self, state: GameState) -> float:
        wc = self.winConditionEvaluationFunction(state=state)
        if wc != 0:
            return wc

        return (self.threatBasedEvaluationFunction(state=state)
                + self.topLayerPieceLocationEvaluationFunction(state=state))

    def threatLocationHandEvalFunction(self, state: GameState) -> float:
        wc = self.winConditionEvaluationFunction(state=state)
        if wc != 0:
            return wc

        return (self.threatBasedEvaluationFunction(state=state)
                + self.topLayerPieceLocationEvaluationFunction(state=state) + self.handEvaluationFunction(state=state))

    def __deepcopy__(self, memodict={}):
        new_color = self.color
        new_eval_function = self.evaluationFunction
        new_pieces = copy.deepcopy(self.pieces)
        return Agent(pieces=new_pieces, color=new_color, evaluationFunction=new_eval_function)

class GameState:
    """
    A GameState specifies the full game state
    """

    def __init__(self, blue: Agent, orange: Agent, blue_to_move: bool, board: ABoardState):
        self.board = board
        self.blue = blue
        self.orange = orange
        self.blueToMove = blue_to_move

    def isOver(self):
        return self.orangeWin() or self.blueWin()
    def blueWin(self):
        return self.board.won(c="b")

    def isWin(self, color: str):
        return self.board.won(c=color)

    def isLose(self, color: str):
        if color == "o":
            return not self.board.won(c="b")
        return not self.board.won(c="o")

    def orangeWin(self):
        return self.board.won(c="o")

    def getBlueAgent(self) -> Agent:
        return self.blue

    def getOrangeAgent(self) -> Agent:
        return self.orange

    def getLegalActions(self, agentColor: str):
        # return a list of legal actions for agent with given index to choose from
        if self.blueWin() or self.orangeWin():
            return []

        moves = []  # will hold a bunch of moves like [(0,0), (1,2)]

        if agentColor == "b":
            agent = self.blue
        else:
            agent = self.orange

        # Moves adding a new piece to the board
        for i in range(3):
            if len(agent.pieces[i]) != 0:  # there is a piece of size i+1
                for row in range(3):
                    for col in range(3):
                        if self.board.can_place_piece(row, col, Piece(agentColor, i + 1)):
                            moves.append([(-(i + 1), -(i + 1)), (row, col)])

        # Moves moving a piece already on the board
        for row in range(3):
            for col in range(3):
                p = self.board.get_piece_at(row, col)
                if p is not None and p.color == agentColor:
                    for new_row in range(3):
                        for new_col in range(3):
                            if row != new_row and col != new_col and self.board.can_place_piece(new_row, new_col, p):
                                moves.append([(row, col), (new_row, new_col)])

        return moves

    def applyAction(self, action, agentColor: str) -> GameState:
        start_row = action[0][0]
        start_col = action[0][1]
        end_row = action[1][0]
        end_col = action[1][1]

        #print("applying action " + str(action) + " for agent " + agentColor)
        if agentColor == "b":
            agent = self.blue
        else:
            agent = self.orange

        if start_row < 0 and start_col < 0:
            piece: Piece = agent.pieces[-(start_col) - 1].pop()
        else:
            piece: Piece = self.board.remove_piece_at(start_row, start_col)
        if not self.board.can_place_piece(end_row, end_col, piece):
            raise Exception('Tried to apply an invalid action')
        self.board.place_piece_at(end_row, end_col, piece)
        self.blueToMove = not self.blueToMove

        return self

    def generateSuccessor(self, agentColor: str, action) -> GameState:
        """
        Returns the successor state after the specified agent takes the action.
        """
        # Check that successors exist
        if self.orangeWin() or self.blueWin():
            raise Exception('Can\'t generate a successor of a terminal state.')

        if self.blueToMove and agentColor == "o":
            raise Exception('Orange tried to move during Blue\'s turn')

        if not self.blueToMove and agentColor == "b":
            raise Exception('Blue tried to move during Orange\'s turn')

        # Copy current state
        state = self.__deepcopy__()

        # apply the action to the copy
        return state.applyAction(action, agentColor)

    def __deepcopy__(self) -> GameState:
        the_board = self.board.__deepcopy__()
        blue = self.blue.__deepcopy__()
        orange = self.orange.__deepcopy__()
        blueToMove = self.blueToMove

        return GameState(blue=blue, orange=orange, blue_to_move=blueToMove, board=the_board)

    def __hash__(self):
        # Hash the game state (board and whose turn it is) for transposition tables
        return self.board.doTheHash(blue_to_move=self.blueToMove)

    def get_symmetries(self):
        # Return a list of hashes for all symmetrical boards for transposition tables, and the type of symmetry
        # formatted like (hash, type)
        symmetry_types = ["Initial", "Flip X", "Flip Y", "Rotate 90", "Rotate 180", "Rotate 270", "Diagonal Flip y=x", "Diagonal Flip y=-x"]
        symmetry_list = []

        for s in symmetry_types:
            board = self.board.produce_symmetry(symmetry_type=s)
            h = board.doTheHash(blue_to_move=self.blueToMove)
            #print(str(board) + " " + str(h))
            symmetry_list.append((h, s))

        return symmetry_list
