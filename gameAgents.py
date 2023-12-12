import copy
import random
import pickle
import os
from os import path
from game import Agent, GameState
from board import BoardState
from piece import Piece


class HumanAtKeyboard(Agent):
    "An agent that takes human input from the keyboard for commands"

    def __init__(self, pieces, c: str):
        super().__init__(pieces, color=c)

    def getAction(self, state: GameState):
        board: BoardState = state.board
        got_valid_action = False
        r1, r2, c1, c2 = -4, -4, -4, -4  # give them all invalid values for now
        while not got_valid_action:
            print(board)
            print("Enter an action like \'r1,c1 r2,c2\', to place a new piece use -1,-1 for r1,c1 for small,\n"
                  "-2,-2 for r1,c1 for medium, and -3,-3 for r1,c1 for large: ")
            action_str = input()
            if self.is_valid_action(action_str):
                got_valid_action = True
            start_coords = action_str.split(" ")[0]
            r1 = int(start_coords.split(",")[0])
            c1 = int(start_coords.split(",")[1])
            end_coords = action_str.split(" ")[1]
            r2 = int(end_coords.split(",")[0])
            c2 = int(end_coords.split(",")[1])
        return [(r1, c1), (r2, c2)]

    def is_valid_action(self, a: str):
        """Action formatted as: r1,c1 r2,c2"""
        try:
            start_coords = a.split(" ")[0]
            r1 = int(start_coords.split(",")[0])
            c1 = int(start_coords.split(",")[1])
            end_coords = a.split(" ")[1]
            r2 = int(end_coords.split(",")[0])
            c2 = int(end_coords.split(",")[1])
        except Exception:
            print("Invalid action. Try again.")
            return False

        if r1 >= 0:
            return 0 < r1 < 3 and 0 < c1 < 3 and 0 < r2 < 3 and 0 < c2 < 3
        else:
            return r1 - c1 == 0 and -3 <= r1 < 0

    def __deepcopy__(self, memodict={}):
        new_human_agent: HumanAtKeyboard = super().__deepcopy__()
        return new_human_agent


class RandomAgent(Agent):
    "An agent that chooses its move randomly among all possible moves"

    def __init__(self, pieces, c: str):
        super().__init__(pieces, color=c)

    def getAction(self, gameState: GameState):
        if gameState.blueToMove:
            agent = gameState.blue
        else:
            agent = gameState.orange
        possible_actions = gameState.getLegalActions(agent.color)
        return random.choice(possible_actions)

    def __deepcopy__(self, memodict={}):
        new_agent: RandomAgent = super().__deepcopy__()
        return new_agent


class MinimaxAgent(Agent):
    """
    A basic minimax agent
    """

    def __init__(self, pieces, c: str, depth: int, evaluationFunction=lambda x: 0):
        self.depth = depth
        super().__init__(pieces, color=c, evaluationFunction=evaluationFunction)

    def getAction(self, gameState: GameState):

        value, move = self.max_agent(state=gameState, depth=0)
        return move

    def max_agent(self, state: GameState, depth: int):
        # print("start of max")
        if depth >= self.depth or state.isOver():
            return self.evaluationFunction.__call__(self, state=state), None

        best_val = float('-inf')
        chosen_move = None
        if state.blueToMove:
            agent = state.blue
        else:
            agent = state.orange
        possible_actions = state.getLegalActions(agent.color)
        for act in possible_actions:
            new_state = state.generateSuccessor(agent.color, action=act)
            value, action = self.min_agent(state=new_state, depth=depth)
            if value > best_val or chosen_move is None:
                best_val = value
                chosen_move = act

        return best_val, chosen_move

    def min_agent(self, state: GameState, depth: int):
        if depth >= self.depth or state.isOver():
            return self.evaluationFunction.__call__(self, state=state), None

        best_val = float('inf')
        if state.blueToMove:
            agent = state.blue
        else:
            agent = state.orange
        possible_actions = state.getLegalActions(agent.color)
        for act in possible_actions:

            new_state = state.generateSuccessor(agent.color, action=act)

            value, action = self.max_agent(state=new_state, depth=depth + 1)

            if value < best_val:
                best_val = value

        return best_val, None

    def __deepcopy__(self, memodict={}):
        new_eval_function = self.evaluationFunction
        new_pieces = copy.deepcopy(self.pieces)
        return MinimaxAgent(pieces=new_pieces, evaluationFunction=new_eval_function, c=self.color, depth=self.depth)


class AlphaBetaMinimaxAgent(Agent):
    """
    Minimax Agent with added AB pruning
    """

    def __init__(self, pieces, c: str, depth: int, evaluationFunction=lambda x: 0):
        self.depth = depth
        super().__init__(pieces, color=c, evaluationFunction=evaluationFunction)

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using AB pruning
        """

        a = float('-inf')
        b = float('inf')
        value, move = self.ab_max_agent(state=gameState, depth=0, a=a, b=b)
        return move

    def ab_min_agent(self, state: GameState, depth: int, a: float, b: float):
        if depth >= self.depth or state.isOver():
            return self.evaluationFunction.__call__(self, state=state), None

        best_val = float('inf')
        if state.blueToMove:
            agent = state.blue
        else:
            agent = state.orange

        possible_actions = state.getLegalActions(agentColor=agent.color)
        for act in possible_actions:

            new_state = state.generateSuccessor(agentColor=agent.color, action=act)

            value, action = self.ab_max_agent(state=new_state, depth=depth + 1, a=a, b=b)

            if value < best_val:
                best_val = value

            if best_val < a:
                return best_val, act
            b = min(b, best_val)

        return best_val, None

    def ab_max_agent(self, state: GameState, depth: int, a: float, b: float):
        if depth >= self.depth or state.isOver():
            return self.evaluationFunction.__call__(self, state=state), None

        value = float('-inf')
        chosen_move = None
        if state.blueToMove:
            agent = state.blue
        else:
            agent = state.orange
        possible_actions = state.getLegalActions(agentColor=agent.color)
        #if depth == 0:
            #print("ab max board:\n" + str(state.board))
            #print(possible_actions)
            #print("evals to" + str(self.evaluationFunction.__call__(self, state=state)))
        for act in possible_actions:
            """if depth == 0:
                print("evaluating action " + str(act))"""
            new_state = state.generateSuccessor(agentColor=agent.color, action=act)
            next_value, action = self.ab_min_agent(state=new_state, depth=depth, a=a, b=b)
            """if depth == 0:
                print("generated:" + str(next_value))"""

            if next_value > value or chosen_move is None:
                value = next_value
                chosen_move = act

            if value > b:
                return b, act
            a = max(a, value)

        return value, chosen_move

    def __deepcopy__(self, memodict={}):

        new_eval_function = self.evaluationFunction
        new_pieces = copy.deepcopy(self.pieces)
        return AlphaBetaMinimaxAgent(pieces=new_pieces, evaluationFunction=new_eval_function, c=self.color,
                                     depth=self.depth)


class TranspositionAgent(Agent):
    """
    Minimax Agent with added AB pruning
    additionally using transposition tables to avoid re-computing symmetrical boards
    """

    def __init__(self, pieces, c: str, depth: int, evaluationFunction=lambda x: 0, storage_file_name: str = "moveStorage", moveDictionary = {}):
        self.depth = depth
        self.storage_file_name = storage_file_name
        self.storage_file_path = './' + storage_file_name + '.pkl'
        self.moveDictionary = moveDictionary
        # will store tuples at each key like
        # moveDictionary[hashedGameState] = (move, depthExploredPastIt, bestValueAfterMoveToDepthPastIt)
        super().__init__(pieces, color=c, evaluationFunction=evaluationFunction)

    def initializeFromFile(self):
        if not os.path.isfile(self.storage_file_path):
            with open(self.storage_file_path, 'wb') as fp:
                pickle.dump({}, fp)

        with open(self.storage_file_path, 'rb') as fp:
            self.moveDictionary = pickle.load(fp)
    def dumpToFile(self):
        with open(self.storage_file_path, 'wb') as fp:
            pickle.dump(self.moveDictionary, fp)

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using AB pruning
        """

        a = float('-inf')
        b = float('inf')
        value, move = self.ab_max_agent(state=gameState, depth=0, a=a, b=b)
        return move

    def ab_min_agent(self, state: GameState, depth: int, a: float, b: float):
        if depth >= self.depth or state.isOver():
            return self.evaluationFunction.__call__(self, state=state), None

        best_val = float('inf')
        if state.blueToMove:
            agent = state.blue
        else:
            agent = state.orange

        possible_actions = state.getLegalActions(agentColor=agent.color)
        for act in possible_actions:

            new_state = state.generateSuccessor(agentColor=agent.color, action=act)

            value, action = self.ab_max_agent(state=new_state, depth=depth + 1, a=a, b=b)

            if value < best_val:
                best_val = value

            if best_val < a:
                return best_val, act
            b = min(b, best_val)

        return best_val, None

    def ab_max_agent(self, state: GameState, depth: int, a: float, b: float):
        if depth >= self.depth or state.isOver():
            return self.evaluationFunction.__call__(self, state=state), None

        lookup_move = self.moveDictionary.get(hash(state), None)
        if lookup_move is not None:
            #print("looked up a move")
            # found a move already computed for this position
            looked_up_move_depth = lookup_move[1]
            looked_up_move = lookup_move[0]
            looked_up_move_value = lookup_move[2]

            if looked_up_move_depth >= self.depth - depth:
                #print("used a looked up move")
                # the move was computed with at least the depth we are computing it to with this call
                return looked_up_move_value, looked_up_move

        value = float('-inf')
        chosen_move = None
        if state.blueToMove:
            agent = state.blue
        else:
            agent = state.orange
        possible_actions = state.getLegalActions(agentColor=agent.color)
        # print("board: " + str(state.board))
        for act in possible_actions:
            # print("evaluating action " + str(act))
            new_state = state.generateSuccessor(agentColor=agent.color, action=act)
            next_value, action = self.ab_min_agent(state=new_state, depth=depth, a=a, b=b)

            if next_value > value or chosen_move is None:
                value = next_value
                chosen_move = act

            if value > b:
                return b, act
            a = max(a, value)

        self.add_symmetries_to_dictionary(state=state, the_move=chosen_move, best_value=value, depth=depth)
        return value, chosen_move

    def add_symmetries_to_dictionary(self, state: GameState, the_move, best_value: float, depth: int):
        symmetries = state.get_symmetries()

        for _sym in symmetries:
            h = _sym[0]
            sym_type = _sym[1]
            new_move = self.alter_move_for_symmetry(the_move, sym_type)

            lookup_move = self.moveDictionary.get(h, None)
            if lookup_move is not None:
                # found a move already computed for this position
                looked_up_move_depth = lookup_move[1]

                if looked_up_move_depth < self.depth - depth:
                    # we computed the move to deeper than it was already computed
                    self.moveDictionary[h] = (new_move, self.depth - depth, best_value)
            else:
                self.moveDictionary[h] = (new_move, self.depth - depth, best_value)

        return

    def alter_move_for_symmetry(self, the_move, symmetry_type: str):
        start_row = the_move[0][0]
        start_col = the_move[0][1]
        end_row = the_move[1][0]
        end_col = the_move[1][1]

        if symmetry_type == "Initial":
            return the_move
        elif symmetry_type == "Flip X":
            coordinate_pairs = {(-3, -3): (-3, -3), (-2, -2): (-2, -2), (-1, -1): (-1, -1),
                                (0, 0): (0, 2), (0, 1): (0, 1), (0, 2): (0, 0),
                                (1, 0): (1, 2), (1, 1): (1, 1), (1, 2): (1, 0),
                                (2, 0): (2, 2), (2, 1): (2, 1), (2, 2): (2, 0)}
        elif symmetry_type == "Flip Y":
            coordinate_pairs = {(-3, -3): (-3, -3), (-2, -2): (-2, -2), (-1, -1): (-1, -1),
                                (0, 0): (2, 0), (0, 1): (2, 1), (0, 2): (2, 2),
                                (1, 0): (1, 0), (1, 1): (1, 1), (1, 2): (1, 2),
                                (2, 0): (0, 0), (2, 1): (0, 1), (2, 2): (0, 2)}
        elif symmetry_type == "Rotate 90":
            coordinate_pairs = {(-3, -3): (-3, -3), (-2, -2): (-2, -2), (-1, -1): (-1, -1),
                                (0, 0): (0, 2), (0, 1): (1, 2), (0, 2): (2, 2),
                                (1, 0): (0, 1), (1, 1): (1, 1), (1, 2): (2, 1),
                                (2, 0): (0, 0), (2, 1): (1, 0), (2, 2): (2, 0)}
        elif symmetry_type == "Rotate 180":
            coordinate_pairs = {(-3, -3): (-3, -3), (-2, -2): (-2, -2), (-1, -1): (-1, -1),
                                (0, 0): (2, 2), (0, 1): (2, 1), (0, 2): (2, 0),
                                (1, 0): (1, 2), (1, 1): (1, 1), (1, 2): (1, 0),
                                (2, 0): (0, 2), (2, 1): (0, 1), (2, 2): (0, 0)}
        elif symmetry_type == "Rotate 270":
            coordinate_pairs = {(-3, -3): (-3, -3), (-2, -2): (-2, -2), (-1, -1): (-1, -1),
                                (0, 0): (2, 0), (0, 1): (1, 0), (0, 2): (0, 0),
                                (1, 0): (2, 1), (1, 1): (1, 1), (1, 2): (1, 0),
                                (2, 0): (2, 2), (2, 1): (1, 2), (2, 2): (0, 2)}
        elif symmetry_type == "Diagonal Flip y=x":
            coordinate_pairs = {(-3, -3): (-3, -3), (-2, -2): (-2, -2), (-1, -1): (-1, -1),
                                (0, 0): (2, 2), (0, 1): (1, 2), (0, 2): (0, 2),
                                (1, 0): (2, 1), (1, 1): (1, 1), (1, 2): (0, 1),
                                (2, 0): (2, 0), (2, 1): (1, 0), (2, 2): (0, 0)}
        elif symmetry_type == "Diagonal Flip y=-x":
            coordinate_pairs = {(-3, -3): (-3, -3), (-2, -2): (-2, -2), (-1, -1): (-1, -1),
                                (0, 0): (0, 0), (0, 1): (1, 0), (0, 2): (2, 0),
                                (1, 0): (0, 1), (1, 1): (1, 1), (1, 2): (2, 1),
                                (2, 0): (0, 2), (2, 1): (1, 2), (2, 2): (2, 2)}
        else:
            return Exception("unrecognized symmetry type: " + symmetry_type)

        new_start_row, new_start_col = coordinate_pairs[(start_row, start_col)]
        new_end_row, new_end_col = coordinate_pairs[(end_row, end_col)]

        return [(new_start_row, new_start_col), (new_end_row, new_end_col)]

    def __deepcopy__(self, memodict={}):

        new_eval_function = self.evaluationFunction
        new_pieces = copy.deepcopy(self.pieces)
        #Don't copy the dictionary because we want the agent to add to it from all game tree paths
        return TranspositionAgent(pieces=new_pieces, evaluationFunction=new_eval_function, c=self.color,
                                     depth=self.depth, storage_file_name=self.storage_file_name, moveDictionary=self.moveDictionary)

# todo more agents: iterative deepening


class MoveSortingAgent(Agent):
    """
    Minimax Agent with added AB pruning
    additionally using transposition tables to avoid re-computing symmetrical boards
    Sorts moves using one-step lookahead to increase the chance AB pruning cuts off branches
    Plays one-move wins without considering other possible moves at that search depth
    """

    def __init__(self, pieces, c: str, depth: int, evaluationFunction=lambda x: 0, storage_file_name: str = "moveStorage", moveDictionary = {}):
        self.depth = depth
        self.storage_file_name = storage_file_name
        self.storage_file_path = './' + storage_file_name + '.pkl'
        self.moveDictionary = moveDictionary
        # will store tuples at each key like
        # moveDictionary[hashedGameState] = (move, depthExploredPastIt, bestValueAfterMoveToDepthPastIt)
        super().__init__(pieces, color=c, evaluationFunction=evaluationFunction)

    def initializeFromFile(self):
        if not os.path.isfile(self.storage_file_path):
            with open(self.storage_file_path, 'wb') as fp:
                pickle.dump({}, fp)

        with open(self.storage_file_path, 'rb') as fp:
            self.moveDictionary = pickle.load(fp)
    def dumpToFile(self):
        with open(self.storage_file_path, 'wb') as fp:
            pickle.dump(self.moveDictionary, fp)

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using AB pruning, transposition tables, and iterative deepening
        """

        a = float('-inf')
        b = float('inf')
        value, move = self.ab_max_agent(state=gameState, depth=0, a=a, b=b)
        return move

    def ab_min_agent(self, state: GameState, depth: int, a: float, b: float):
        if depth >= self.depth or state.isOver():
            return self.evaluationFunction.__call__(self, state=state), None

        best_val = float('inf')
        if state.blueToMove:
            agent = state.blue
        else:
            agent = state.orange

        possible_actions = state.getLegalActions(agentColor=agent.color)
        for act in possible_actions:

            new_state = state.generateSuccessor(agentColor=agent.color, action=act)

            value, action = self.ab_max_agent(state=new_state, depth=depth + 1, a=a, b=b)

            if value < best_val:
                best_val = value

            if best_val < a:
                return best_val, act
            b = min(b, best_val)

        return best_val, None

    def ab_max_agent(self, state: GameState, depth: int, a: float, b: float):
        if depth >= self.depth or state.isOver():
            return self.evaluationFunction.__call__(self, state=state), None

        lookup_move = self.moveDictionary.get(hash(state), None)
        if lookup_move is not None:
            #print("looked up a move")
            # found a move already computed for this position
            looked_up_move_depth = lookup_move[1]
            looked_up_move = lookup_move[0]
            looked_up_move_value = lookup_move[2]

            if looked_up_move_depth >= self.depth - depth:
                #print("used a looked up move")
                # the move was computed with at least the depth we are computing it to with this call
                return looked_up_move_value, looked_up_move

        value = float('-inf')
        chosen_move = None
        if state.blueToMove:
            agent = state.blue
        else:
            agent = state.orange
        possible_actions = state.getLegalActions(agentColor=agent.color)

        #sort available actions here
        action_value_pairs = []
        for act in possible_actions:
            new_state: GameState = state.generateSuccessor(agentColor=agent.color, action=act)

            # play the instant win
            if new_state.isWin(agent.color):
                return float('inf'), act

            new_state_value = self.evaluationFunction.__call__(self, state=new_state)
            action_value_pairs.append((act, new_state_value))
        action_value_pairs.sort(key=lambda x: x[1])
        possible_actions = list(map(lambda x: x[0], action_value_pairs))

        for act in possible_actions:
            # print("evaluating action " + str(act))
            new_state = state.generateSuccessor(agentColor=agent.color, action=act)
            next_value, action = self.ab_min_agent(state=new_state, depth=depth, a=a, b=b)

            if next_value > value or chosen_move is None:
                value = next_value
                chosen_move = act

            if value > b:
                return b, act
            a = max(a, value)

        self.add_symmetries_to_dictionary(state=state, the_move=chosen_move, best_value=value, depth=depth)
        return value, chosen_move

    def add_symmetries_to_dictionary(self, state: GameState, the_move, best_value: float, depth: int):
        symmetries = state.get_symmetries()

        for _sym in symmetries:
            h = _sym[0]
            sym_type = _sym[1]
            new_move = self.alter_move_for_symmetry(the_move, sym_type)

            lookup_move = self.moveDictionary.get(h, None)
            if lookup_move is not None:
                # found a move already computed for this position
                looked_up_move_depth = lookup_move[1]

                if looked_up_move_depth < self.depth - depth:
                    # we computed the move to deeper than it was already computed
                    self.moveDictionary[h] = (new_move, self.depth - depth, best_value)
            else:
                self.moveDictionary[h] = (new_move, self.depth - depth, best_value)

        return

    def alter_move_for_symmetry(self, the_move, symmetry_type: str):
        start_row = the_move[0][0]
        start_col = the_move[0][1]
        end_row = the_move[1][0]
        end_col = the_move[1][1]

        if symmetry_type == "Initial":
            return the_move
        elif symmetry_type == "Flip X":
            coordinate_pairs = {(-3, -3): (-3, -3), (-2, -2): (-2, -2), (-1, -1): (-1, -1),
                                (0, 0): (0, 2), (0, 1): (0, 1), (0, 2): (0, 0),
                                (1, 0): (1, 2), (1, 1): (1, 1), (1, 2): (1, 0),
                                (2, 0): (2, 2), (2, 1): (2, 1), (2, 2): (2, 0)}
        elif symmetry_type == "Flip Y":
            coordinate_pairs = {(-3, -3): (-3, -3), (-2, -2): (-2, -2), (-1, -1): (-1, -1),
                                (0, 0): (2, 0), (0, 1): (2, 1), (0, 2): (2, 2),
                                (1, 0): (1, 0), (1, 1): (1, 1), (1, 2): (1, 2),
                                (2, 0): (0, 0), (2, 1): (0, 1), (2, 2): (0, 2)}
        elif symmetry_type == "Rotate 90":
            coordinate_pairs = {(-3, -3): (-3, -3), (-2, -2): (-2, -2), (-1, -1): (-1, -1),
                                (0, 0): (0, 2), (0, 1): (1, 2), (0, 2): (2, 2),
                                (1, 0): (0, 1), (1, 1): (1, 1), (1, 2): (2, 1),
                                (2, 0): (0, 0), (2, 1): (1, 0), (2, 2): (2, 0)}
        elif symmetry_type == "Rotate 180":
            coordinate_pairs = {(-3, -3): (-3, -3), (-2, -2): (-2, -2), (-1, -1): (-1, -1),
                                (0, 0): (2, 2), (0, 1): (2, 1), (0, 2): (2, 0),
                                (1, 0): (1, 2), (1, 1): (1, 1), (1, 2): (1, 0),
                                (2, 0): (0, 2), (2, 1): (0, 1), (2, 2): (0, 0)}
        elif symmetry_type == "Rotate 270":
            coordinate_pairs = {(-3, -3): (-3, -3), (-2, -2): (-2, -2), (-1, -1): (-1, -1),
                                (0, 0): (2, 0), (0, 1): (1, 0), (0, 2): (0, 0),
                                (1, 0): (2, 1), (1, 1): (1, 1), (1, 2): (1, 0),
                                (2, 0): (2, 2), (2, 1): (1, 2), (2, 2): (0, 2)}
        elif symmetry_type == "Diagonal Flip y=x":
            coordinate_pairs = {(-3, -3): (-3, -3), (-2, -2): (-2, -2), (-1, -1): (-1, -1),
                                (0, 0): (2, 2), (0, 1): (1, 2), (0, 2): (0, 2),
                                (1, 0): (2, 1), (1, 1): (1, 1), (1, 2): (0, 1),
                                (2, 0): (2, 0), (2, 1): (1, 0), (2, 2): (0, 0)}
        elif symmetry_type == "Diagonal Flip y=-x":
            coordinate_pairs = {(-3, -3): (-3, -3), (-2, -2): (-2, -2), (-1, -1): (-1, -1),
                                (0, 0): (0, 0), (0, 1): (1, 0), (0, 2): (2, 0),
                                (1, 0): (0, 1), (1, 1): (1, 1), (1, 2): (2, 1),
                                (2, 0): (0, 2), (2, 1): (1, 2), (2, 2): (2, 2)}
        else:
            return Exception("unrecognized symmetry type: " + symmetry_type)

        new_start_row, new_start_col = coordinate_pairs[(start_row, start_col)]
        new_end_row, new_end_col = coordinate_pairs[(end_row, end_col)]

        return [(new_start_row, new_start_col), (new_end_row, new_end_col)]

    def __deepcopy__(self, memodict={}):

        new_eval_function = self.evaluationFunction
        new_pieces = copy.deepcopy(self.pieces)
        #Don't copy the dictionary because we want the agent to add to it from all game tree paths
        return MoveSortingAgent(pieces=new_pieces, evaluationFunction=new_eval_function, c=self.color,
                                     depth=self.depth, storage_file_name=self.storage_file_name, moveDictionary=self.moveDictionary)


class IterativeDeepeningAgent(Agent):

    def __init__(self, color: str, pieces, internalAgent: Agent, depth: int):
        self.internalAgent = internalAgent
        self.depth = depth
        super().__init__(color=color, pieces=pieces)

    def getAction(self, gameState: GameState):
        best_move = None
        for d in range(1, self.depth + 1):
            best_move = self.internalAgent.getAction(gameState=gameState)

        return best_move

#todo move trim agent, lose optimality but look further ahead
