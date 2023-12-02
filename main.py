# This is a sample Python script.
from copy import deepcopy

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


def play_game(blue, orange, the_board, agent_to_move: bool, print_info: bool = False):
    move_cap = 30
    moves_completed = 0
    the_game = GameState(blue=blue, orange=orange, blue_to_move=agent_to_move, board=the_board)

    while not the_game.isOver() and moves_completed < move_cap:

        if the_game.blueToMove:
            agent_to_move: Agent = blue
        else:
            agent_to_move: Agent = orange

        the_actions = the_game.getLegalActions(agent_to_move.color)
        move = agent_to_move.getAction(the_game)
        if print_info:
            print("agent " + agent_to_move.color + " took action " + str(move) + " with available pieces: " + str(
                agent_to_move.pieces))
            print("legal actions were: " + str(the_actions))
            print(str(the_game.board))

        the_game.applyAction(move, agent_to_move.color)

        moves_completed += 1

    # game stats, could probably log these / save to file
    # todo time used stats?
    if print_info:
        print("Game over:\nblue won? " + str(the_game.blueWin()) + "\norange won? " + str(the_game.orangeWin()) +
              "\nnum moves: " + str(moves_completed) + "\nfinal board: \n" + str(the_game.board))

    # return data about who won, moves taken, time used?
    return [the_game.blueWin(), the_game.orangeWin(), moves_completed]


def simulate_games(blue: Agent, orange: Agent, num_games):
    results = {"blue wins": 0, "orange wins": 0}
    sum_moves_completed = 0

    for i in range(num_games):
        print("playing game number " + str(i + 1))
        blue.setPieces(pieces=deepcopy(evaluationBoards.START_BLUE_PIECES))
        blue.setColor("b")
        orange.setPieces(pieces=deepcopy(evaluationBoards.START_ORANGE_PIECES))
        orange.setColor("o")

        game_results = play_game(blue=blue, orange=orange, agent_to_move=True,
                                 the_board=deepcopy(evaluationBoards.START_BOARD))
        if game_results[0]:
            results["blue wins"] += 1
        elif game_results[1]:
            results["orange wins"] += 1

        sum_moves_completed += game_results[2]

    num_games = float(num_games)
    blue_wp = results["blue wins"] / num_games
    blue_wp = math.floor(blue_wp * 1000) / 1000
    orange_wp = results["orange wins"] / num_games
    orange_wp = math.floor(orange_wp * 1000) / 1000
    average_moves = sum_moves_completed / num_games
    average_moves = math.floor(average_moves * 1000) / 1000
    draw_p = (num_games - results["blue wins"] - results["orange wins"]) / num_games
    draw_p = math.floor(draw_p * 1000) / 1000

    return [blue_wp, draw_p, orange_wp, average_moves]


def simulate_games_for_agents(agents: [Agent], names: [str], games_per_agent):
    all_data = {}

    for a, n in zip(agents, names):
        print("Running games for " + n)
        sim_game_data = simulate_games(blue=RandomAgent(c="b", pieces=None), orange=a, num_games=games_per_agent)

        loss_rate, draw_rate, win_rate, average_game_duration = sim_game_data
        all_data[n] = ("win rate: " + str(win_rate), "loss rate: " + str(loss_rate), "draw rate: " + str(draw_rate),
                       "average game duration (total moves): " + str(average_game_duration))

    return all_data


def time_moves_for_agent(agent: Agent, boards: [BoardState], board_names: [str], blue_pieces: [[[Piece]]],
                         orange_pieces: [[[Piece]]], color_to_move_booleans: [bool]):
    agent_data = []
    for i in range(len(boards)):
        if color_to_move_booleans[i]:  # agent should be blue
            agent.setColor("b")
            agent.setPieces(blue_pieces[i])
            game = GameState(blue=agent, orange=RandomAgent(orange_pieces[i], "o"), blue_to_move=True, board=boards[i])

        else:  # agent is orange
            agent.setColor("o")
            agent.setPieces(orange_pieces[i])
            game = GameState(blue=RandomAgent(blue_pieces[i], "b"), orange=agent, blue_to_move=False, board=boards[i])

        tps = TimedProcess(_object=agent, f="getAction", params={"gameState": game})
        tps.run()
        the_time = tps.getTime()
        the_time = math.floor(the_time * 1000) / 1000
        agent_data.append((board_names[i], "time: " + str(the_time)))

    return agent_data


def get_agent_runtime_data(agents: [Agent], names: [str], boards: [BoardState], board_names: [str],
                           blue_pieces: [[[Piece]]], orange_pieces: [[[Piece]]], color_to_move_booleans: [bool]):
    all_data = {}
    for a, n in zip(agents, names):
        print("Running agent " + n)
        agent_data = time_moves_for_agent(agent=a, boards=boards, board_names=board_names, blue_pieces=blue_pieces,
                                          orange_pieces=orange_pieces, color_to_move_booleans=color_to_move_booleans)
        all_data[n] = agent_data

    return all_data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Set the python hash seed to a constant value for reproducible hashing between runs
    if not os.environ.get('PYTHONHASHSEED') or os.environ["PYTHONHASHSEED"] != '3':
        print("set hash to 3")
        os.environ['PYTHONHASHSEED'] = '3'
        # os.execv(sys.executable, ['python3'] + sys.argv)
    board = evaluationBoards.TTW_BOARD
    empty_board = evaluationBoards.START_BOARD

    # print(board)
    h = HumanAtKeyboard(evaluationBoards.START_BLUE_PIECES, "b")
    # m = MinimaxAgent(evaluationBoards.TTW_BLUE_PIECES, "b", 2)
    ab = AlphaBetaMinimaxAgent(evaluationBoards.START_BLUE_PIECES, "b", 2)
    # ab_1 = AlphaBetaMinimaxAgent(evaluationBoards.START_ORANGE_PIECES, "o", 1)
    t = TranspositionAgent(evaluationBoards.START_ORANGE_PIECES, "o", 2, storage_file_name="testing")
    r = RandomAgent(evaluationBoards.START_BLUE_PIECES, "b")
    # game = GameState(blue=ab, orange=h, blue_to_move=True, board=board)
    # game2 = GameState(blue=ab, orange=r, blue_to_move=True, board=empty_board)
    game3 = GameState(blue=r, orange=t, blue_to_move=True, board=empty_board)
    ab.setEvalFunction(Agent.topLayerWeightedSizeEvaluationFunction)
    # ab_1.setEvalFunction(Agent.topLayerWeightedSizeEvaluationFunction)
    t.setEvalFunction(Agent.topLayerWeightedSizeEvaluationFunction)
    # m.setEvalFunction(Agent.winConditionEvaluationFunction)

    # game3.applyAction([(-3,-3), (1,1)], "b")
    # t.add_symmetries_to_dictionary(state=game3, the_move=[(-2,-2), (0,0)], best_value=4, depth=0)
    # print(t.moveDictionary)
    # print("done")
    # game3.get_symmetries()
    # print("aaaaa")
    # print(t.getAction(game3))
    # print(str(hash(game3)) + " " + str(hash(game3)))
    # print(hash(game3.board) - hash(game3.board.produce_symmetry("Initial")))
    # play_game(blue=ab, orange=ab_1, the_board=empty_board, agent_to_move=True)
    # play_game(blue=r, orange=t, the_board=empty_board, agent_to_move=False)

    time_measurement_agents = [RandomAgent(None, "b"),
                               MinimaxAgent(None, "b", 1,
                                            evaluationFunction=Agent.topLayerWeightedSizeEvaluationFunction),
                               MinimaxAgent(None, "b", 2,
                                            evaluationFunction=Agent.topLayerWeightedSizeEvaluationFunction),
                               AlphaBetaMinimaxAgent(None, "b", 1,
                                                     evaluationFunction=Agent.topLayerWeightedSizeEvaluationFunction),
                               AlphaBetaMinimaxAgent(None, "b", 2,
                                                     evaluationFunction=Agent.topLayerWeightedSizeEvaluationFunction),
                               TranspositionAgent(None, "b", 1,
                                                  evaluationFunction=Agent.topLayerWeightedSizeEvaluationFunction),
                               TranspositionAgent(None, "b", 2,
                                                  evaluationFunction=Agent.topLayerWeightedSizeEvaluationFunction)]

    time_measurement_agent_names = ["Random Move Agent",
                                    "Minimax, Depth 1",
                                    "Minimax, Depth 2",
                                    "Alpha Beta Agent, Depth 1",
                                    "Alpha Beta Agent, Depth 2",
                                    "Transposition Agent, Depth 1",
                                    "Transposition Agent, Depth 2"]
    time_measurement_boards = [evaluationBoards.START_BOARD,
                               evaluationBoards.OTW_BOARD,
                               evaluationBoards.TTW_BOARD,
                               evaluationBoards.CROWDED_BOARD,
                               evaluationBoards.SIMPLE_BOARD,
                               evaluationBoards.LOW_BOARD,
                               evaluationBoards.MID_BOARD,
                               evaluationBoards.HIGH_BOARD]
    time_measurement_board_names = ["Starting Board",
                                    "One Turn Win Board",
                                    "Two Turn Win Board",
                                    "Crowded Board",
                                    "Simple Board",
                                    "Small Pieces Board",
                                    "Medium Pieces Board",
                                    "Large Pieces Board", ]
    time_measurement_blue_pieces = [evaluationBoards.START_BLUE_PIECES,
                                    evaluationBoards.OTW_BLUE_PIECES,
                                    evaluationBoards.TTW_BLUE_PIECES,
                                    evaluationBoards.CROWDED_BLUE_PIECES,
                                    evaluationBoards.SIMPLE_BLUE_PIECES,
                                    evaluationBoards.LOW_BLUE_PIECES,
                                    evaluationBoards.MID_BLUE_PIECES,
                                    evaluationBoards.HIGH_BLUE_PIECES]
    time_measurement_orange_pieces = [evaluationBoards.START_ORANGE_PIECES,
                                      evaluationBoards.OTW_ORANGE_PIECES,
                                      evaluationBoards.TTW_ORANGE_PIECES,
                                      evaluationBoards.CROWDED_ORANGE_PIECES,
                                      evaluationBoards.SIMPLE_ORANGE_PIECES,
                                      evaluationBoards.LOW_ORANGE_PIECES,
                                      evaluationBoards.MID_ORANGE_PIECES,
                                      evaluationBoards.HIGH_ORANGE_PIECES]
    time_measurement_next_move_booleans = [True, False, True, False, True, True, True, True]

    """the_data = get_agent_runtime_data(agents=time_measurement_agents, names=time_measurement_agent_names,
                                      boards=time_measurement_boards, board_names=time_measurement_board_names,
                                      blue_pieces=time_measurement_blue_pieces,
                                      orange_pieces=time_measurement_orange_pieces,
                                      color_to_move_booleans=time_measurement_next_move_booleans)

    for i in the_data.keys():
        print(str(i) + " : " + str(the_data[i]))"""

    evaluation_function_agents = [AlphaBetaMinimaxAgent(pieces=None, c="o", depth=1,
                                     evaluationFunction=Agent.winConditionEvaluationFunction),
                                  AlphaBetaMinimaxAgent(pieces=None, c="o", depth=1,
                                                        evaluationFunction=Agent.topLayerEvaluationFunction),
                                  AlphaBetaMinimaxAgent(pieces=None, c="o", depth=1,
                                                        evaluationFunction=Agent.topLayerWeightedSizeEvaluationFunction),
                                  AlphaBetaMinimaxAgent(pieces=None, c="o", depth=1,
                                                        evaluationFunction=Agent.threatBasedEvaluationFunction),
                                  AlphaBetaMinimaxAgent(pieces=None, c="o", depth=1,
                                                        evaluationFunction=Agent.topLayerPieceLocationEvaluationFunction)
                                  ]

    evaluation_function_agent_names = ["Win Condition Agent", "Top Layer Evaluation Agent",
                                       "Top Layer Weighted Size Evaluation Agent",
                                       "Threat Evaluation Agent", "Piece Location Agent"]

    eval_function_data = simulate_games_for_agents(agents=evaluation_function_agents, names=evaluation_function_agent_names, games_per_agent=1000)
    for i in eval_function_data.keys():
        print(str(i) + " : " + str(eval_function_data[i]))

    """    random_agent = RandomAgent(pieces=None, c="b")
    wc_agent = AlphaBetaMinimaxAgent(pieces=None, c="o", depth=1,
                                     evaluationFunction=Agent.winConditionEvaluationFunction)
    top_layer_agent = AlphaBetaMinimaxAgent(pieces=None, c="o", depth=1,
                                            evaluationFunction=Agent.topLayerEvaluationFunction)
    top_layer_weighted_size_agent = AlphaBetaMinimaxAgent(pieces=None, c="o", depth=1,
                                                          evaluationFunction=Agent.topLayerWeightedSizeEvaluationFunction)
    threat_agent = AlphaBetaMinimaxAgent(pieces=None, c="o", depth=1,
                                         evaluationFunction=Agent.threatBasedEvaluationFunction)
    piece_location_agent = AlphaBetaMinimaxAgent(pieces=None, c="o", depth=1,
                                                 evaluationFunction=Agent.topLayerPieceLocationEvaluationFunction)

    sim_results = simulate_games(blue=random_agent, orange=top_layer_agent, num_games=200)
    print("blue wins: " + str(sim_results[0]))
    print("orange wins: " + str(sim_results[1]))
    print("moves: " + str(sim_results[2]))"""

    # play_game(blue=r, orange=t, the_board=empty_board, agent_to_move=True)

    # todo always make sure agents have the right pieces
    # print(ab.getAction(game))
    # a.getAction(game)

    # tp = TimedProcess(_object=t, f="getAction", params={"gameState": game3})
    # tp.run()
    # print(tp.getTime())

    # tp = TimedProcess(_object=ab, f="getAction", params={"gameState": game3})
    # tp.run()
    # print(tp.getTime())

    # print(evaluationBoards.CROWDED_BOARD)
    # print(str(game.get_symmetries()))

    """tps = TimedProcessSeries(_object=ab, f="getAction", params=[{"gameState": game3}] * 2)
    tps.run()
    print(tps.getMinTime())
    print(tps.getAverageTime())"""

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
