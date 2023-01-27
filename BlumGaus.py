"""   

- Generally, coordinates/positions are 'A3', 'B3',...
- board[coord] returns the piece at coord
- Try to always have a move to do (just take a random one at the beginning with update_move)

- IMPORTANT: ALWAYS USE COPIES OF THE GAME BOARD, YOU DO NOT HAVE TO USE DEEPCOPY ANYMORE,
             THIS IS SHOWN IN MR. NOVICE
             
- You can get the board from the gui via gui.chessboard

- DO NOT CHANGE OR ADD THE PARAMS OF THE GENERATE FUNCTION OR ITS NAME!



        -------------------- Useful methods  ---------------------------------------

-------------------- Board methods:

# converts coordinates in the form '(x,y)' (tuple) to 'A4' (string)
def letter_notation(self,coord)

# converts coordinates in the from 'A4' (string) to '(x,y)' (tuple)
def number_notation(self, coord):

# looks through the whole board to check for the king, outputs pos of king like this 'A5' (string)
def get_king_position(self, color):

# get the enemy, color is "white" or "black"
def get_enemy(self, color):

# manually check from the king if other pieces can attack it
# output is boolean
def is_in_check(self, color, debug=False):

def is_in_checkmate(self, color):

# returns a list of all valid moves in the format [('A1','A4'),..], left: from, right: to
def generate_valid_moves(self, color):

# returns a list of all possible moves in the format [('A1','A4'),..], left: from, right: to
def all_possible_moves(self, color):

# checks for limit turn count and checkmate, returns boolean (won/not won)
def check_winning_condition(self,color,end_game=False,print_result=False,gui = None):

# filter out invalid moves for moves of a color, returns list of valid moves
def is_in_check_after_move_filter(self,moves):

# returns boolean (still in check after p1->p2)
def is_in_check_after_move(self, p1, p2):

# time left for choosing move (in seconds)
def get_time_left(self):

# executes move without checking
# !   You have to manually change to the next player 
# with board.player_turn=board.get_enemy(board.player_turn) after this !
def _do_move(self, p1, p2):

# Pretty print board
def pprint(self):

# update the move that will be done (has to be a tuple (from, to))
def update_move(self,move):


---------------GUI methods

# performs the selected move (should ideally be at the end of generate function)
def perform_move(self):


--------------- Piece methods


# returns the landing positions, if the piece were at pos
# ! only landing positions !
def possible_moves(pos)

"""
import time
import random
import math
from copy import deepcopy, copy
from typing import List

from agents import *


class MrBlumGaus:

    def __init__(self, color, delay=0, threshold=3.5):
        self.delay = delay
        self.TIME_THRESHOLD = threshold
        self.color = color
        self.__initPieces__()

        return None

    def __initPieces__(self) -> None:
        """
        initialise of the score values for each piece type, their field bonuses and synergy effects
        and saves them in a dict

        :rtype: None
        """
        self.score = {}
        # pawn
        self.score['p'] = PieceValue(
            figure=10,
            field_1=[
                [4, 5, 5, 5, 5, 4],
                [3, 4, 4, 4, 4, 3],
                [2, 2, 3, 3, 3, 2],
                [1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]
            ],
            field_2=[
                [5, 5, 5, 5, 5, 5],
                [3, 4, 4, 4, 4, 3],
                [2, 2, 3, 3, 3, 2],
                [1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]
            ],
            synergy={'white': 1, 'black': 1})
        # rook
        self.score['r'] = PieceValue(
            figure=50,
            field_1=[
                [2, 2, 2, 2, 2, 2],
                [2, 3, 3, 3, 3, 2],
                [2, 3, 3, 3, 3, 2],
                [2, 2, 2, 2, 2, 2],
                [1, 1, 1, 1, 1, 1],
                [-1, 0, 1, 1, 0, -1]
            ],
            field_2=[
                [2, 2, 2, 2, 2, 2],
                [2, 4, 4, 4, 4, 2],
                [2, 3, 4, 4, 3, 2],
                [2, 2, 2, 2, 2, 2],
                [1, 1, 1, 1, 1, 1],
                [-5, 0, 1, 1, 0, -5]
            ],
            synergy={'white': 0.9, 'black': 0.9})
        # bishop
        self.score['b'] = PieceValue(
            figure=30,
            field_1=[
                [0, 0, 0, 0, 0, 0],
                [0, 4, 4, 4, 4, 0],
                [0, 3, 3, 3, 3, 0],
                [1, 3, 3, 3, 2, 1],
                [1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0]
            ],
            field_2=[
                [0, 0, 0, 0, 0, 0],
                [0, 4, 4, 4, 4, 0],
                [0, 3, 5, 5, 3, 0],
                [1, 3, 5, 5, 2, 1],
                [1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0]
            ],
            synergy={'white': 0.9, 'black': 0.9})
        # knight
        self.score['n'] = PieceValue(
            figure=30,
            field_1=[
                [-2, -3, -3, -3, -3, -2],
                [-1, 3, 3, 3, 3, -1],
                [-1, 3, 3, 3, 3, -1],
                [-1, 2, 2, 2, 2, -1],
                [-1, 1, 1, 1, 1, -1],
                [-1, -3, -3, -3, -3, -1]
            ],
            field_2=[
                [-2, -3, -3, -3, -3, -2],
                [-1, 4, 4, 4, 4, -1],
                [-1, 5, 5, 5, 5, -1],
                [-1, 2, 2, 2, 2, -1],
                [-1, 1, 1, 1, 1, -1],
                [-1, -3, -3, -3, -3, -1]
            ],
            synergy={'white': 1, 'black': 1})
        # king
        self.score['k'] = PieceValue(
            figure=500,
            field_1=[
                [-8, -8, -8, -8, -8, -8],
                [-8, -9, -10, -10, -9, -8],
                [-8, -9, -10, -10, -9, -8],
                [-6, -7, -7, -7, -7, -6],
                [3, 3, 1, 1, 3, 3],
                [3, 5, 2, 2, 5, 3],
            ],
            field_2=[
                [-8, -8, -8, -8, -8, -8],
                [-8, -9, -10, -10, -9, -8],
                [-6, -6, -4, -4, -6, -6],
                [0, 0, 5, 5, 0, 0],
                [2, 2, 4, 4, 2, 2],
                [2, 3, 2, 2, 3, 2],
            ],
            synergy={'white': 1, 'black': 1})

        # the king is dead
        self.score['win'] = 500
        # the King is threaten
        # TODO: everybody should get a value for getting threatening
        self.score['check'] = 20

        return None

    def evaluateGame(self, board) -> int:
        """
        evaluate total score of game state after the moves

        :param board: 2D 6 times 6 array representing board state
        :type board:
        :param player_wins: if player has won
        :type player_wins: bool
        :param enemy_wins: if enemy has won
        :type enemy_wins: bool
        :return:
        :rtype: int
        """
        # print("Evaluation of board started.")
        t1 = time.time()
        score = 0
        team = {'white': -1, 'black': -1, self.color: 1}

        # print("Is in Check")
        if board.is_in_check(self.color):
            score -= self.score['check']

        if board.is_in_check(board.get_enemy(self.color)):
            score += self.score['check']

        # print("Calc score")
        t1 = time.time()
        for coord, figure in board.items():
            if figure is not None:
                fig_type = figure.abbriviation.lower()
                fig_color = figure.color
                # get coords
                xy = [int(coord[1]) - 1, board.axis_y.index(coord[0])]
                # value boards are mirrored at y-axis for white player
                if fig_color == 'white':
                    xy[0] = 5 - xy[0]
                fig_val = self.score[fig_type].figure
                # after 20 turns take the late game board
                if board.fullmove_number < 20:
                    field_val = self.score[fig_type].field_1[xy[0]][xy[1]]
                else:
                    field_val = self.score[fig_type].field_2[xy[0]][xy[1]]
                syn_value = self.score[fig_type].synergy[fig_color]
                score += team[fig_color] * (syn_value * fig_val + field_val)

                if fig_type == 'b' or fig_type == 'r':
                    # second bishop/ rook is 125% worth it
                    self.score[fig_type].synergy[fig_color] = 1.25

        t2 = time.time()
        # print("Checking Score Calc in evaluation: ", t2-t1)

        # print("Evaluation of board ended.")
        # print(score)
        return score

    # prefer moves that beat enemies pieces or that are threaten to be beaten
    def better_moves(self, moves_max, moves_min):
        return [move for move in moves_max if move[1] in [i[0] for i in moves_min] or move[0] in [i[1] for i in moves_min]]
    # rather not try moves that will get you in a bad spot
    def worse_moves(self, moves_max, moves_min):
        return [move for move in moves_max if move[1] in [i[1] for i in moves_min]]


    def generate_next_move(self, gui):

        # print("Next move will now be generated:")
        t_total = time.time()
        board = deepcopy(gui.chessboard)
        maxscore = -math.inf
        bestmoves = []

        # calc yours and the enemies moves
        moves_max = board.generate_valid_moves(board.player_turn)
        moves_min = board.generate_valid_moves(board.get_enemy(self.color))

        # change depth depending on number possible branches
        if len(moves_max) < 7:
            search_depth = 4
        elif len(moves_max) < 10:
            search_depth = 4
        elif len(moves_max) < 12:
            search_depth = 4
        elif len(moves_max) < 20:
            search_depth = 3
        else:
            search_depth = 2
        print('search_depth ', search_depth)
        print('moves_max ', len(moves_max))

        # generate moves, place the better ones at the front
        better_moves = self.better_moves(moves_max, moves_min)
        #worse_moves = self.worse_moves(moves_max, moves_min)
        moves_max = list(set(moves_max) - set(better_moves))# - set(worse_moves))
        random.shuffle(moves_max)
        random.shuffle(better_moves)
        #random.shuffle(worse_moves)
        moves = better_moves + moves_max #+ worse_moves

        if len(moves) > 0:
            # always have one move to to
            gui.chessboard.update_move(moves[0])

            # print("We will test ", len(moves), " main moves.")
            for m in moves:

                # COPY
                _from_fig = board[m[0]]
                _to_fig = board[m[1]]
                player, move_number = board.get_current_state()

                # PERFORM
                board._do_move(m[0], m[1])
                board.switch_players()

                score = self.min_func(gui.chessboard, board, search_depth, maxscore, math.inf)

                # RESET
                board[m[0]] = _from_fig
                board[m[1]] = _to_fig
                board.player_turn = player
                board.fullmove_number = move_number

                if score > maxscore:
                    print('max score', score)
                    maxscore = score
                    bestmoves.clear()
                    bestmoves.append(m)
                    gui.chessboard.update_move(m)
                elif score == maxscore:
                    bestmoves.append(m)

            print('chosen score', maxscore)
            print("total time evrything calculated", time.time() - t_total)
            bestmove = bestmoves[random.randint(0, len(bestmoves) - 1)]
            gui.chessboard.update_move(bestmove)
            gui.perform_move()
        gui.chessboard.engine_is_selecting = False

    def min_func(self, original_board, board, depth, alpha, beta):

        # TODO: avoid threshholds
        if original_board.get_time_left() < self.TIME_THRESHOLD:
            print('threshhold')
            return self.evaluateGame(board)

        # game_ends if player_wins or enemy_wins
        if board.check_winning_condition(self.color): return math.inf
        if board.check_winning_condition(board.get_enemy(self.color)): return -math.inf

        if depth <= 0:
            return self.evaluateGame(board)

        # calc yours and the enemies moves
        moves_max = board.generate_valid_moves(board.player_turn)
        moves_min = board.generate_valid_moves(board.get_enemy(self.color))

        # change depth depending on the number possible branches
        if len(moves_max) < 6:
            depth += 0 #.5
            #print('+0.5 ', depth)
        elif len(moves_max) > 14:
            depth -= 0.5
            #print('-0.5 ', depth)

        # generate moves, place the better ones at the front
        better_moves = self.better_moves(moves_max, moves_min)
        worse_moves = self.worse_moves(moves_max, moves_min)
        moves_max = list(set(moves_max) - set(better_moves) - set(worse_moves))
        random.shuffle(moves_max)
        random.shuffle(better_moves)
        random.shuffle(worse_moves)
        moves = better_moves + moves_max + worse_moves

        minscore = math.inf

        for m in moves:
            # COPY
            _from_fig = board[m[0]]
            _to_fig = board[m[1]]
            player, move_number = board.get_current_state()

            # PERFORM
            board._do_move(m[0], m[1])
            board.switch_players()

            # board.board_states.append(board.to_string())

            score = 0.99 * self.max_func(original_board, board, depth - 1, alpha, beta)

            # RESET
            board[m[0]] = _from_fig
            board[m[1]] = _to_fig
            board.player_turn = player
            board.fullmove_number = move_number

            if score < minscore:
                minscore = score
            if score < beta:
                minscore = score
                beta = score
                if beta <= alpha:
                    # print('alpha,beta,minscore: ', alpha, ': ', beta, ': ', minscore)
                    break

        return minscore

    def max_func(self, original_board, board, depth, alpha, beta):

        # TODO: avoid threshholds
        if original_board.get_time_left() < self.TIME_THRESHOLD:
            print('threshhold')
            return self.evaluateGame(board)

        # game_ends if player_wins or enemy_wins
        if board.check_winning_condition(self.color): return math.inf
        if board.check_winning_condition(board.get_enemy(self.color)): return -math.inf

        if depth <= 0:
            return self.evaluateGame(board)

        # calc yours and the enemies moves
        moves_max = board.generate_valid_moves(board.player_turn)
        moves_min = board.generate_valid_moves(board.get_enemy(self.color))

        if len(moves_max) < 6:
            depth += 0 #.5
            #print('+0.5 ', depth)
        elif len(moves_max) > 14:
            depth -= 0.5
            #print('-0.5 ', depth)

        # generate moves, place the better ones at the front
        better_moves = self.better_moves(moves_max, moves_min)
        worse_moves = self.worse_moves(moves_max, moves_min)
        moves_max = list(set(moves_max) - set(better_moves) - set(worse_moves))
        random.shuffle(moves_max)
        random.shuffle(better_moves)
        random.shuffle(worse_moves)
        moves = better_moves + moves_max + worse_moves

        maxscore = -math.inf

        for m in moves:
            # COPY
            _from_fig = board[m[0]]
            _to_fig = board[m[1]]
            player, move_number = board.get_current_state()

            # PERFORM
            board._do_move(m[0], m[1])
            board.switch_players()

            # board.board_states.append(board.to_string())

            score = 0.99 * self.min_func(original_board, board, depth - 1, alpha, beta)

            # RESET
            board[m[0]] = _from_fig
            board[m[1]] = _to_fig
            board.player_turn = player
            board.fullmove_number = move_number

            if score > maxscore:
                maxscore = score
            if score > alpha:
                maxscore = score
                alpha = score
                if alpha >= beta:
                    break

        return maxscore


class PieceValue:

    def __init__(self, figure: int, field_1, field_2, synergy):
        self.figure = figure
        self.field_1 = field_1
        self.field_2 = field_2
        self.synergy = synergy
