# This is a sample Python script.
import evaluationBoards
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from board import BoardState
from piece import Piece
from game import GameState, Agent
from gameAgents import HumanAtKeyboard, MinimaxAgent, AlphaBetaMinimaxAgent, RandomAgent, TranspositionAgent
from timedProcess import TimedProcess, TimedProcessSeries
import os
import sys
import math


def play_game(blue, orange, the_board, agent_to_move: bool):
    move_cap = 30
    moves_completed = 0
    the_game = GameState(blue=blue, orange=orange, blue_to_move=agent_to_move, board=the_board)

    while not the_game.isOver() and moves_completed < move_cap:

        if the_game.blueToMove:
            agent_to_move: Agent = blue
        else:
            agent_to_move: Agent = orange

        move = agent_to_move.getAction(the_game)
        a_pieces = agent_to_move.pieces
        the_game.applyAction(move, agent_to_move.color)
        print("agent " + agent_to_move.color + " took action " + str(move) + " with available pieces: " + str(a_pieces))
        #print("legal actions: " + str(the_game.getLegalActions(agent_to_move.color)))
        print(str(the_game.board))
        moves_completed += 1

    # game stats, could probably log these / save to file
    # todo time used stats
    print("Game over:\nblue won? " + str(the_game.blueWin()) + "\norange won? " + str(the_game.orangeWin()) +
          "\nnum moves: " + str(moves_completed) + "\nfinal board: \n" + str(the_game.board))


def time_moves_for_agent(agent: Agent, boards: [BoardState], board_names: [str], blue_pieces: [[[Piece]]], orange_pieces: [[[Piece]]], color_to_move_booleans: [bool]):
    agent_data = []
    for i in range(len(boards)):
        if color_to_move_booleans[i]: #agent should be blue
            agent.setColor("b")
            agent.setPieces(blue_pieces[i])
            game = GameState(blue=agent, orange=RandomAgent(orange_pieces[i], "o"), blue_to_move=True, board=boards[i])

        else: # agent is orange
            agent.setColor("o")
            agent.setPieces(orange_pieces[i])
            game = GameState(blue=RandomAgent(blue_pieces[i], "b"), orange=agent, blue_to_move=False, board=boards[i])

        tps = TimedProcess(_object=agent, f="getAction", params={"gameState": game})
        tps.run()
        the_time = tps.getTime()
        the_time = math.floor(the_time*1000)/1000
        agent_data.append((board_names[i], "time: " + str(the_time)))

    return agent_data


def get_agent_runtime_data(agents: [Agent], names: [str], boards: [BoardState], board_names: [str], blue_pieces: [[[Piece]]], orange_pieces: [[[Piece]]], color_to_move_booleans: [bool]):
    all_data = {}
    for a, n in zip(agents, names):
        print("Running agent " + n)
        agent_data = time_moves_for_agent(agent=a, boards=boards, board_names=board_names, blue_pieces=blue_pieces, orange_pieces=orange_pieces, color_to_move_booleans=color_to_move_booleans)
        all_data[n] = agent_data

    return all_data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Set the python hash seed to a constant value for reproducible hashing between runs
    if not os.environ.get('PYTHONHASHSEED') or os.environ["PYTHONHASHSEED"] != '3':
        print("set hash to 3")
        os.environ['PYTHONHASHSEED'] = '3'
        #os.execv(sys.executable, ['python3'] + sys.argv)
    board = evaluationBoards.TTW_BOARD
    empty_board = evaluationBoards.START_BOARD

    # print(board)
    h = HumanAtKeyboard(evaluationBoards.START_BLUE_PIECES, "b")
    #m = MinimaxAgent(evaluationBoards.TTW_BLUE_PIECES, "b", 2)
    ab = AlphaBetaMinimaxAgent(evaluationBoards.START_BLUE_PIECES, "b", 2)
    #ab_1 = AlphaBetaMinimaxAgent(evaluationBoards.START_ORANGE_PIECES, "o", 1)
    t = TranspositionAgent(evaluationBoards.START_ORANGE_PIECES, "o", 2, storage_file_name="testing")
    r = RandomAgent(evaluationBoards.START_BLUE_PIECES, "b")
    #game = GameState(blue=ab, orange=h, blue_to_move=True, board=board)
    #game2 = GameState(blue=ab, orange=r, blue_to_move=True, board=empty_board)
    game3 = GameState(blue=r, orange=t, blue_to_move=True, board=empty_board)
    ab.setEvalFunction(Agent.topLayerWeightedSizeEvaluationFunction)
    #ab_1.setEvalFunction(Agent.topLayerWeightedSizeEvaluationFunction)
    t.setEvalFunction(Agent.topLayerWeightedSizeEvaluationFunction)
    #m.setEvalFunction(Agent.winConditionEvaluationFunction)

    #game3.applyAction([(-3,-3), (1,1)], "b")
    #t.add_symmetries_to_dictionary(state=game3, the_move=[(-2,-2), (0,0)], best_value=4, depth=0)
    #print(t.moveDictionary)
    #print("done")
    #game3.get_symmetries()
    #print("aaaaa")
    #print(t.getAction(game3))
    #print(str(hash(game3)) + " " + str(hash(game3)))
    #print(hash(game3.board) - hash(game3.board.produce_symmetry("Initial")))
    #play_game(blue=ab, orange=ab_1, the_board=empty_board, agent_to_move=True)
    #play_game(blue=r, orange=t, the_board=empty_board, agent_to_move=False)

    agents = [RandomAgent(None, "b"),
              MinimaxAgent(None, "b", 1, evaluationFunction=Agent.topLayerWeightedSizeEvaluationFunction),
              MinimaxAgent(None, "b", 2, evaluationFunction=Agent.topLayerWeightedSizeEvaluationFunction),
              AlphaBetaMinimaxAgent(None, "b", 1, evaluationFunction=Agent.topLayerWeightedSizeEvaluationFunction),
              AlphaBetaMinimaxAgent(None, "b", 2, evaluationFunction=Agent.topLayerWeightedSizeEvaluationFunction),
              TranspositionAgent(None, "b", 1, evaluationFunction=Agent.topLayerWeightedSizeEvaluationFunction),
              TranspositionAgent(None, "b", 2, evaluationFunction=Agent.topLayerWeightedSizeEvaluationFunction)]

    names = ["Random Move Agent",
             "Minimax, Depth 1",
             "Minimax, Depth 2",
             "Alpha Beta Agent, Depth 1",
             "Alpha Beta Agent, Depth 2",
             "Transposition Agent, Depth 1",
             "Transposition Agent, Depth 2"]
    boards = [evaluationBoards.START_BOARD,
              evaluationBoards.OTW_BOARD,
              evaluationBoards.TTW_BOARD,
              evaluationBoards.CROWDED_BOARD,
              evaluationBoards.SIMPLE_BOARD,
              evaluationBoards.LOW_BOARD,
              evaluationBoards.MID_BOARD,
              evaluationBoards.HIGH_BOARD]
    board_names = ["Starting Board",
                   "One Turn Win Board",
                   "Two Turn Win Board",
                   "Crowded Board",
                   "Simple Board",
                   "Small Pieces Board",
                   "Medium Pieces Board",
                   "Large Pieces Board",]
    blue_pieces = [evaluationBoards.START_BLUE_PIECES,
                   evaluationBoards.OTW_BLUE_PIECES,
                   evaluationBoards.TTW_BLUE_PIECES,
                   evaluationBoards.CROWDED_BLUE_PIECES,
                   evaluationBoards.SIMPLE_BLUE_PIECES,
                   evaluationBoards.LOW_BLUE_PIECES,
                   evaluationBoards.MID_BLUE_PIECES,
                   evaluationBoards.HIGH_BLUE_PIECES]
    orange_pieces = [evaluationBoards.START_ORANGE_PIECES,
                     evaluationBoards.OTW_ORANGE_PIECES,
                     evaluationBoards.TTW_ORANGE_PIECES,
                     evaluationBoards.CROWDED_ORANGE_PIECES,
                     evaluationBoards.SIMPLE_ORANGE_PIECES,
                     evaluationBoards.LOW_ORANGE_PIECES,
                     evaluationBoards.MID_ORANGE_PIECES,
                     evaluationBoards.HIGH_ORANGE_PIECES]
    next_move_booleans = [True, False, True, False, True, True, True, True]

    """the_data = get_agent_runtime_data(agents=agents, names=names, boards=boards, board_names=board_names,
                                      blue_pieces=blue_pieces, orange_pieces=orange_pieces,
                                      color_to_move_booleans=next_move_booleans)

    for i in the_data.keys():
        print(str(i) + " : " + str(the_data[i]))"""

    #play_game(blue=r, orange=t, the_board=empty_board, agent_to_move=True)

    # todo always make sure agents have the right pieces
    # print(ab.getAction(game))
    # a.getAction(game)

    #tp = TimedProcess(_object=t, f="getAction", params={"gameState": game3})
    #tp.run()
    #print(tp.getTime())

    #tp = TimedProcess(_object=ab, f="getAction", params={"gameState": game3})
    #tp.run()
    #print(tp.getTime())

    # print(evaluationBoards.CROWDED_BOARD)
    # print(str(game.get_symmetries()))

    """tps = TimedProcessSeries(_object=ab, f="getAction", params=[{"gameState": game3}] * 2)
    tps.run()
    print(tps.getMinTime())
    print(tps.getAverageTime())"""



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
