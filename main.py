# This is a sample Python script.
import evaluationBoards
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from board import BoardState
from game import GameState, Agent
from gameAgents import HumanAtKeyboard, MinimaxAgent, AlphaBetaMinimaxAgent, RandomAgent
from timedProcess import TimedProcess, TimedProcessSeries
import os
import sys

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
        the_game.applyAction(move, agent_to_move.color)
        print("agent " + agent_to_move.color + " took action " + str(move))
        print(str(the_game.board))
        moves_completed += 1

    # game stats, could probably log these / save to file
    # todo time used stats
    print("Game over:\nblue won? " + str(the_game.blueWin()) + "\norange won? " + str(the_game.orangeWin()) +
          "\nnum moves: " + str(moves_completed) + "\nfinal board: \n" + str(the_game.board))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Set the python hash seed to a constant value for reproducible hashing between runs
    if not os.environ.get('PYTHONHASHSEED') or os.environ["PYTHONHASHSEED"] != '3':
        print("set hash to 3")
        os.environ['PYTHONHASHSEED'] = '3'
        os.execv(sys.executable, ['python3'] + sys.argv)
    board = evaluationBoards.TTW_BOARD
    empty_board = evaluationBoards.START_BOARD

    # print(board)
    h = HumanAtKeyboard(evaluationBoards.TTW_ORANGE_PIECES, "o")
    m = MinimaxAgent(evaluationBoards.TTW_BLUE_PIECES, "b", 2)
    ab = AlphaBetaMinimaxAgent(evaluationBoards.START_BLUE_PIECES, "b", 2)
    ab_1 = AlphaBetaMinimaxAgent(evaluationBoards.START_ORANGE_PIECES, "o", 1)
    r = RandomAgent(evaluationBoards.START_ORANGE_PIECES, "o")
    game = GameState(blue=ab, orange=h, blue_to_move=True, board=board)
    #game2 = GameState(blue=ab, orange=r, blue_to_move=True, board=empty_board)
    ab.setEvalFunction(Agent.topLayerWeightedSizeEvaluationFunction)
    ab_1.setEvalFunction(Agent.topLayerWeightedSizeEvaluationFunction)
    m.setEvalFunction(Agent.winConditionEvaluationFunction)

    #print(ab.getAction(game2))

    play_game(blue=ab, orange=ab_1, the_board=empty_board, agent_to_move=True)

    # todo make sure agents have the right pieces
    # print(ab.getAction(game))
    # a.getAction(game)

    #tp = TimedProcess(_object=ab, f="getAction", params={"gameState": game})
    #tp.run()
    #print(tp.getTime())

    # print(evaluationBoards.CROWDED_BOARD)
    # print(str(game.get_symmetries()))

    #tps = TimedProcessSeries(_object=ab, f="getAction", params=[{"gameState": game}] * 2)
    #tps.run()
    #print(tps.getAverageTime())



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
