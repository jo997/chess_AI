import time
import random
import math
from copy import deepcopy, copy
#from studentagent import *
from BlumGaus import *

class MrRandom:
    
    def __init__(self, delay=0):
        self.delay = delay
        
    def generate_next_move(self,gui):

        board = gui.chessboard
        
        moves = board.generate_valid_moves(board.player_turn)
        if len(moves) > 0:
            a = random.randint(0,len(moves)-1)
            board.update_move(moves[a])
            gui.perform_move()
        board.engine_is_selecting = False

        
class MrNovice:

    def __init__(self,color,delay=0, threshold=5):
        self.delay = delay
        self.TIME_THRESHOLD = threshold
        self.color = color
    
    def evaluateGame(self,board, player_wins, enemy_wins):
        #print("Evaluation of board started.")
        SCORE_WIN    = 1000
        
        SCORE_PAWN   = 10
        SCORE_ROOK   = 50
        SCORE_BISHOP = 30
        SCORE_KNIGHT = 30
        
        SCORE_CHECK     = 5
        
        color = self.color
        score = 0

        #print("Check winning")
        t1 = time.time()
        if player_wins:
            return SCORE_WIN
        elif enemy_wins:
            return -SCORE_WIN
        t2 = time.time()
        #print("Checking winning in evaluation: ", t2-t1)
        
        #print("Is in Check")
        t1 = time.time()
        if board.is_in_check(color):
            score -= SCORE_CHECK
        
        if board.is_in_check(board.get_enemy(color)):
            score += SCORE_CHECK
        
        t2 = time.time()
        #print("Checking Is in Check in evaluation: ", t2-t1)
        
        #print("Calc score")
        t1 = time.time()
        for coord in board.keys():
            if (board[coord] is not None):
                figure = board[coord]
                fig_color = board[coord].color
            
                figurescore = 0
                fig_name = (figure.abbriviation).lower() 
                if fig_name == 'p':
                    figurescore = SCORE_PAWN
                elif fig_name=='r':
                    figurescore = SCORE_ROOK
                elif fig_name=='b':
                    figurescore = SCORE_BISHOP
                elif fig_name=='n':
                    figurescore = SCORE_KNIGHT

                if fig_color == color:
                    score += figurescore
                else:
                    score -= figurescore

        t2 = time.time()
        #print("Checking Score Calc in evaluation: ", t2-t1)            
        
        #print("Evaluation of board ended.")
        return score

    def generate_next_move(self,gui):
        
        #print("Next move will now be generated:")
        
        board = deepcopy(gui.chessboard)
        
        search_depth = 2
        maxscore = -math.inf
        
        bestmoves = []

        #print("First, valid moves are generated.")
        moves = board.generate_valid_moves(board.player_turn)
        random.shuffle(moves)
        
        if len(moves) > 0:
            # always have one move to to
            gui.chessboard.update_move(moves[0])


            #print("We will test ", len(moves), " main moves.")
            for m in moves:

                
                # COPY
                _from_fig = board[m[0]]
                _to_fig = board[m[1]]
                player, move_number = board.get_current_state()        

                # PERFORM
                board._do_move(m[0],m[1])
                board.switch_players()

                #print("We test main move: ", m, " and the board looks like this:")
                #board_copy.pprint()
                #print("Main move test start.")
                
                #board.board_states.append(board.to_string())
                
                score = self.min_func(gui.chessboard,board, search_depth)
                """
                print("\n\n----------------------\n\n")
                print("Main move " + "(" +m[0] + ", " + m[1] + ")" + " with score " + str(score) + " test end.\n\n")
                for state in board.board_states:
                    print(state)
                print("\n\n----------------------\n\n")
                board.board_states.pop()
                """


                 # RESET
                board[m[0]] = _from_fig
                board[m[1]] = _to_fig
                board.player_turn = player
                board.fullmove_number = move_number 
                
                if score > maxscore:
                    print('best score', score)
                    maxscore = score
                    bestmoves.clear()
                    bestmoves.append(m)
                    gui.chessboard.update_move(m)
                elif score == maxscore:
                    bestmoves.append(m)

            print('chosen score', maxscore)
            bestmove = bestmoves[random.randint(0,len(bestmoves)-1)]
            gui.chessboard.update_move(bestmove)
            gui.perform_move()
        gui.chessboard.engine_is_selecting = False
        
    

    def min_func(self,original_board,board,depth):
        
        color = self.color
        
        player_wins = board.check_winning_condition(color)
        enemy_wins = board.check_winning_condition(board.get_enemy(color))
        game_ends = player_wins or enemy_wins 
        
        if ((depth <= 0) or game_ends or (original_board.get_time_left() < self.TIME_THRESHOLD)):
            if original_board.get_time_left() < self.TIME_THRESHOLD: print('threshhold')
            return self.evaluateGame(board,player_wins,enemy_wins)

        moves = board.generate_valid_moves(board.player_turn)
        random.shuffle(moves)

        minscore = math.inf

        for m in moves:
            # COPY
            _from_fig = board[m[0]]
            _to_fig = board[m[1]]
            player, move_number = board.get_current_state()        

            # PERFORM
            board._do_move(m[0],m[1])
            board.switch_players()
            
            #board.board_states.append(board.to_string())
            
            score = 0.99 * self.max_func(original_board,board, depth - 1)

            """
            print("\n\n----------------------\n\n")
            print("Score for this move sequence is: ", score)
            for state in board.board_states:
                print(state)
            print("\n\n----------------------\n\n")
            board.board_states.pop()
            """
            
            # RESET
            board[m[0]] = _from_fig
            board[m[1]] = _to_fig
            board.player_turn = player
            board.fullmove_number = move_number 

            if score < minscore:
                minscore = score
                
        return minscore
    
    def max_func(self,original_board,board,depth):
        
        color = self.color
        
        player_wins = board.check_winning_condition(color)
        enemy_wins = board.check_winning_condition(board.get_enemy(color))
        game_ends = player_wins or enemy_wins 
        
        if ((depth <= 0) or game_ends or (original_board.get_time_left() < self.TIME_THRESHOLD)):
            if original_board.get_time_left() < self.TIME_THRESHOLD: print('threshhold')
            return self.evaluateGame(board,player_wins,enemy_wins)

        moves = board.generate_valid_moves(board.player_turn)
        random.shuffle(moves)

        maxscore = -math.inf

        for m in moves:
            # COPY
            _from_fig = board[m[0]]
            _to_fig = board[m[1]]
            player, move_number = board.get_current_state()        

            # PERFORM
            board._do_move(m[0],m[1])
            board.switch_players()
            
            #board.board_states.append(board.to_string())
            
            score = 0.99 * self.min_func(original_board,board, depth - 1)
            
            """
            print("\n\n----------------------\n\n")
            print("Score for this move sequence is: ", score)
            for state in board.board_states:
                print(state)
            print("\n\n----------------------\n\n")
            board.board_states.pop()
            """
            
            # RESET
            board[m[0]] = _from_fig
            board[m[1]] = _to_fig
            board.player_turn = player
            board.fullmove_number = move_number 

            if score > maxscore:
                maxscore = score
                
        return maxscore


class MrNovicePruning:

    def __init__(self, color, delay=0, threshold=5):
        self.delay = delay
        self.TIME_THRESHOLD = threshold
        self.color = color

    def evaluateGame(self, board, player_wins, enemy_wins):
        # print("Evaluation of board started.")
        SCORE_WIN = 1000

        SCORE_PAWN = 10
        SCORE_ROOK = 50
        SCORE_BISHOP = 30
        SCORE_KNIGHT = 30

        SCORE_CHECK = 5

        color = self.color
        score = 0

        # print("Check winning")
        t1 = time.time()
        if player_wins:
            return SCORE_WIN
        elif enemy_wins:
            return -SCORE_WIN
        t2 = time.time()
        # print("Checking winning in evaluation: ", t2-t1)

        # print("Is in Check")
        t1 = time.time()
        if board.is_in_check(color):
            score -= SCORE_CHECK

        if board.is_in_check(board.get_enemy(color)):
            score += SCORE_CHECK

        t2 = time.time()
        # print("Checking Is in Check in evaluation: ", t2-t1)

        # print("Calc score")
        t1 = time.time()
        for coord in board.keys():
            if (board[coord] is not None):
                figure = board[coord]
                fig_color = board[coord].color

                figurescore = 0
                fig_name = (figure.abbriviation).lower()
                if fig_name == 'p':
                    figurescore = SCORE_PAWN
                elif fig_name == 'r':
                    figurescore = SCORE_ROOK
                elif fig_name == 'b':
                    figurescore = SCORE_BISHOP
                elif fig_name == 'n':
                    figurescore = SCORE_KNIGHT

                if fig_color == color:
                    score += figurescore
                else:
                    score -= figurescore

        t2 = time.time()
        # print("Checking Score Calc in evaluation: ", t2-t1)

        # print("Evaluation of board ended.")
        return score

    def generate_next_move(self, gui):

        # print("Next move will now be generated:")

        board = deepcopy(gui.chessboard)

        search_depth = 4
        maxscore = -math.inf

        bestmoves = []

        # print("First, valid moves are generated.")
        moves = board.generate_valid_moves(board.player_turn)
        random.shuffle(moves)

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

                # print("We test main move: ", m, " and the board looks like this:")
                # board_copy.pprint()
                # print("Main move test start.")

                # board.board_states.append(board.to_string())

                score = self.min_func(gui.chessboard, board, search_depth, maxscore, math.inf)
                """
                print("\n\n----------------------\n\n")
                print("Main move " + "(" +m[0] + ", " + m[1] + ")" + " with score " + str(score) + " test end.\n\n")
                for state in board.board_states:
                    print(state)
                print("\n\n----------------------\n\n")
                board.board_states.pop()
                """

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
            bestmove = bestmoves[random.randint(0, len(bestmoves) - 1)]
            gui.chessboard.update_move(bestmove)
            gui.perform_move()
        gui.chessboard.engine_is_selecting = False

    def min_func(self, original_board, board, depth, alpha, beta):

        color = self.color

        player_wins = board.check_winning_condition(color)
        enemy_wins = board.check_winning_condition(board.get_enemy(color))
        game_ends = player_wins or enemy_wins

        if ((depth <= 0) or game_ends or (original_board.get_time_left() < self.TIME_THRESHOLD)):
            if original_board.get_time_left() < self.TIME_THRESHOLD: print('threshhold')
            return self.evaluateGame(board, player_wins, enemy_wins)

        moves = board.generate_valid_moves(board.player_turn)
        random.shuffle(moves)

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

            """
            print("\n\n----------------------\n\n")
            print("Score for this move sequence is: ", score)
            for state in board.board_states:
                print(state)
            print("\n\n----------------------\n\n")
            board.board_states.pop()
            """

            # RESET
            board[m[0]] = _from_fig
            board[m[1]] = _to_fig
            board.player_turn = player
            board.fullmove_number = move_number

            if score < minscore:
                minscore = score
            if score < beta:
                beta = score
                if beta <= alpha:
                    # print('alpha,beta,minscore: ', alpha, ': ', beta, ': ', minscore)
                    break

        return minscore

    def max_func(self, original_board, board, depth, alpha, beta):

        color = self.color

        player_wins = board.check_winning_condition(color)
        enemy_wins = board.check_winning_condition(board.get_enemy(color))
        game_ends = player_wins or enemy_wins

        if ((depth <= 0) or game_ends or (original_board.get_time_left() < self.TIME_THRESHOLD)):
            if original_board.get_time_left() < self.TIME_THRESHOLD: print('threshhold')
            return self.evaluateGame(board, player_wins, enemy_wins)

        moves = board.generate_valid_moves(board.player_turn)
        random.shuffle(moves)

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

            """
            print("\n\n----------------------\n\n")
            print("Score for this move sequence is: ", score)
            for state in board.board_states:
                print(state)
            print("\n\n----------------------\n\n")
            board.board_states.pop()
            """

            # RESET
            board[m[0]] = _from_fig
            board[m[1]] = _to_fig
            board.player_turn = player
            board.fullmove_number = move_number

            if score > maxscore:
                maxscore = score
            if score > alpha:
                alpha = score
                if alpha >= beta:
                    # print('alpha,beta,minscore: ', alpha, ': ', beta, ': ', maxscore)
                    break

        return maxscore

class MrNovicePruningBetter:

    def __init__(self, color, delay=0, threshold=5):
        self.delay = delay
        self.TIME_THRESHOLD = threshold
        self.color = color

    def evaluateGame(self, board):
        # print("Evaluation of board started.")
        SCORE_WIN = 1000

        SCORE_PAWN = 10
        SCORE_ROOK = 50
        SCORE_BISHOP = 30
        SCORE_KNIGHT = 30

        SCORE_CHECK = 5

        color = self.color
        score = 0

        # print("Is in Check")
        t1 = time.time()
        if board.is_in_check(color):
            score -= SCORE_CHECK

        if board.is_in_check(board.get_enemy(color)):
            score += SCORE_CHECK

        t2 = time.time()
        # print("Checking Is in Check in evaluation: ", t2-t1)

        # print("Calc score")
        t1 = time.time()
        for coord in board.keys():
            if (board[coord] is not None):
                figure = board[coord]
                fig_color = board[coord].color

                figurescore = 0
                fig_name = (figure.abbriviation).lower()
                if fig_name == 'p':
                    figurescore = SCORE_PAWN
                elif fig_name == 'r':
                    figurescore = SCORE_ROOK
                elif fig_name == 'b':
                    figurescore = SCORE_BISHOP
                elif fig_name == 'n':
                    figurescore = SCORE_KNIGHT

                if fig_color == color:
                    score += figurescore
                else:
                    score -= figurescore

        t2 = time.time()
        # print("Checking Score Calc in evaluation: ", t2-t1)

        # print("Evaluation of board ended.")
        return score

    def better_moves(self, moves_max, moves_min):
        return [move for move in moves_max if move[1] in [i[0] for i in moves_min] or move[0] in [i[1] for i in moves_min]]

    def worse_moves(self, moves_max, moves_min):
        return [move for move in moves_max if move[1] in [i[1] for i in moves_min]]


    def generate_next_move(self, gui):

        # print("Next move will now be generated:")

        board = deepcopy(gui.chessboard)


        maxscore = -math.inf

        bestmoves = []

        # print("First, valid moves are generated.")
        moves_max = board.generate_valid_moves(board.player_turn)

        if len(moves_max) < 7:
            search_depth = 4
        elif len(moves_max) < 10:
            search_depth = 4.5
        elif len(moves_max) < 15:
            search_depth = 4
        elif len(moves_max) < 20:
            search_depth = 3.5
        else:
            search_depth = 2.5
        print('len(moves) ', len(moves_max))
        print('search_depth ', search_depth)

        moves_min = board.generate_valid_moves(board.get_enemy(self.color))
        # print(board.fullmove_number)
        # if board.fullmove_number<10:
        if len(moves_max)>11:
            worse_moves = self.worse_moves(moves_max, moves_min)
            moves_max = list(set(moves_max) - set(worse_moves))
            random.shuffle(moves_max)
            random.shuffle(worse_moves)
            moves = moves_max + worse_moves
        else:
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

                # print("We test main move: ", m, " and the board looks like this:")
                # board_copy.pprint()
                # print("Main move test start.")

                # board.board_states.append(board.to_string())

                score = self.min_func(gui.chessboard, board, search_depth, maxscore, math.inf)
                """
                print("\n\n----------------------\n\n")
                print("Main move " + "(" +m[0] + ", " + m[1] + ")" + " with score " + str(score) + " test end.\n\n")
                for state in board.board_states:
                    print(state)
                print("\n\n----------------------\n\n")
                board.board_states.pop()
                """

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
            bestmove = bestmoves[random.randint(0, len(bestmoves) - 1)]
            gui.chessboard.update_move(bestmove)
            gui.perform_move()
        gui.chessboard.engine_is_selecting = False

    def min_func(self, original_board, board, depth, alpha, beta):

        #color = self.color
        if original_board.get_time_left() < self.TIME_THRESHOLD:
            print('threshhold')
            return self.evaluateGame(board)

        if board.check_winning_condition(self.color): return math.inf
        if board.check_winning_condition(board.get_enemy(self.color)): return -math.inf
        #game_ends = player_wins or enemy_wins

        if depth <= 0:
            return self.evaluateGame(board)

        moves_max = board.generate_valid_moves(board.player_turn)
        if len(moves_max) < 6:
            depth += 0.5
        elif len(moves_max) > 14:
            depth -= 0.5
        #print('len(moves_min) ', len(moves_max))
        #print('depth ', depth)

        moves_min = board.generate_valid_moves(board.get_enemy(self.color))
       # print(board.fullmove_number)
       # if board.fullmove_number<10:
        if len(moves_max)>11:
            worse_moves = self.worse_moves(moves_max, moves_min)
            moves_max = list(set(moves_max) - set(worse_moves))
            random.shuffle(moves_max)
            random.shuffle(worse_moves)
            moves = moves_max + worse_moves
        else:
            better_moves = self.better_moves(moves_max, moves_min)
            #worse_moves = self.worse_moves(moves_max, moves_min)
            moves_max = list(set(moves_max) - set(better_moves))# - set(worse_moves))
            random.shuffle(moves_max)
            random.shuffle(better_moves)
            #random.shuffle(worse_moves)
            moves = better_moves + moves_max #+ worse_moves


        #random.shuffle(moves)

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

            """
            print("\n\n----------------------\n\n")
            print("Score for this move sequence is: ", score)
            for state in board.board_states:
                print(state)
            print("\n\n----------------------\n\n")
            board.board_states.pop()
            """

            # RESET
            board[m[0]] = _from_fig
            board[m[1]] = _to_fig
            board.player_turn = player
            board.fullmove_number = move_number

            #if score < minscore:
            #    minscore = score
            if score < beta:
                minscore = score
                beta = score
                if beta <= alpha:
                    # print('alpha,beta,minscore: ', alpha, ': ', beta, ': ', minscore)
                    break

        return minscore

    def max_func(self, original_board, board, depth, alpha, beta):

        if original_board.get_time_left() < self.TIME_THRESHOLD:
            print('threshhold')
            return self.evaluateGame(board)

        if board.check_winning_condition(self.color): return math.inf
        if board.check_winning_condition(board.get_enemy(self.color)): return -math.inf

        if depth <= 0:
            return self.evaluateGame(board)

        moves_max = board.generate_valid_moves(board.player_turn)
        if len(moves_max) < 6:
            depth += 0.5
        elif len(moves_max) > 14:
            depth -= 0.5
        #print('len(moves_max) ', len(moves_max))
        #print('depth ', depth)

        moves_min = board.generate_valid_moves(board.get_enemy(self.color))
        # print(board.fullmove_number)
        # if board.fullmove_number<10:
        if len(moves_max) > 11:
            worse_moves = self.worse_moves(moves_max, moves_min)
            moves_max = list(set(moves_max) - set(worse_moves))
            random.shuffle(moves_max)
            random.shuffle(worse_moves)
            moves = moves_max + worse_moves
        else:
            better_moves = self.better_moves(moves_max, moves_min)
            # worse_moves = self.worse_moves(moves_max, moves_min)
            moves_max = list(set(moves_max) - set(better_moves))  # - set(worse_moves))
            random.shuffle(moves_max)
            random.shuffle(better_moves)
            # random.shuffle(worse_moves)
            moves = better_moves + moves_max  # + worse_moves

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

            """
            print("\n\n----------------------\n\n")
            print("Score for this move sequence is: ", score)
            for state in board.board_states:
                print(state)
            print("\n\n----------------------\n\n")
            board.board_states.pop()
            """

            # RESET
            board[m[0]] = _from_fig
            board[m[1]] = _to_fig
            board.player_turn = player
            board.fullmove_number = move_number

            #if score > maxscore:
            #    maxscore = score
            if score > alpha:
                maxscore = score
                alpha = score
                if alpha >= beta:
                    # print('alpha,beta,minscore: ', alpha, ': ', beta, ': ', maxscore)
                    break

        return maxscore


class MrNovicePruningBetter1:

    def __init__(self, color, delay=0, threshold=5):
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
        self.score['check'] = 200

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
                score += team[fig_color] * (self.score[fig_type].figure + self.score[fig_type].field_1[xy[0]][xy[1]])


        t2 = time.time()
        # print("Checking Score Calc in evaluation: ", t2-t1)

        # print("Evaluation of board ended.")
        # print(score)
        return score

    def better_moves(self, moves_max, moves_min):
        return [move for move in moves_max if move[1] in [i[0] for i in moves_min] or move[0] in [i[1] for i in moves_min]]

    def worse_moves(self, moves_max, moves_min):
        return [move for move in moves_max if move[1] in [i[1] for i in moves_min]]


    def generate_next_move(self, gui):

        # print("Next move will now be generated:")

        board = deepcopy(gui.chessboard)


        maxscore = -math.inf

        bestmoves = []

        # print("First, valid moves are generated.")
        moves_max = board.generate_valid_moves(board.player_turn)

        if len(moves_max) < 7:
            search_depth = 4
        elif len(moves_max) < 10:
            search_depth = 4
        elif len(moves_max) < 15:
            search_depth = 3.5
        elif len(moves_max) < 20:
            search_depth = 3
        else:
            search_depth = 2.5
        print('len(moves) ', len(moves_max))
        print('search_depth ', search_depth)

        moves_min = board.generate_valid_moves(board.get_enemy(self.color))
        # print(board.fullmove_number)
        # if board.fullmove_number<10:
        if len(moves_max)>11:
            worse_moves = self.worse_moves(moves_max, moves_min)
            moves_max = list(set(moves_max) - set(worse_moves))
            random.shuffle(moves_max)
            random.shuffle(worse_moves)
            moves = moves_max + worse_moves
        else:
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

                # print("We test main move: ", m, " and the board looks like this:")
                # board_copy.pprint()
                # print("Main move test start.")

                # board.board_states.append(board.to_string())

                score = self.min_func(gui.chessboard, board, search_depth, maxscore, math.inf)
                """
                print("\n\n----------------------\n\n")
                print("Main move " + "(" +m[0] + ", " + m[1] + ")" + " with score " + str(score) + " test end.\n\n")
                for state in board.board_states:
                    print(state)
                print("\n\n----------------------\n\n")
                board.board_states.pop()
                """

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
            bestmove = bestmoves[random.randint(0, len(bestmoves) - 1)]
            gui.chessboard.update_move(bestmove)
            gui.perform_move()
        gui.chessboard.engine_is_selecting = False

    def min_func(self, original_board, board, depth, alpha, beta):

        #color = self.color
        if original_board.get_time_left() < self.TIME_THRESHOLD:
            print('threshhold')
            return self.evaluateGame(board)

        if board.check_winning_condition(self.color): return math.inf
        if board.check_winning_condition(board.get_enemy(self.color)): return -math.inf
        #game_ends = player_wins or enemy_wins

        if depth <= 0:
            return self.evaluateGame(board)

        moves_max = board.generate_valid_moves(board.player_turn)
        if len(moves_max) < 6:
            depth += 0.5
        elif len(moves_max) > 14:
            depth -= 0.5
        #print('len(moves_min) ', len(moves_max))
        #print('depth ', depth)

        moves_min = board.generate_valid_moves(board.get_enemy(self.color))
       # print(board.fullmove_number)
       # if board.fullmove_number<10:
        if len(moves_max)>11:
            worse_moves = self.worse_moves(moves_max, moves_min)
            moves_max = list(set(moves_max) - set(worse_moves))
            random.shuffle(moves_max)
            random.shuffle(worse_moves)
            moves = moves_max + worse_moves
        else:
            better_moves = self.better_moves(moves_max, moves_min)
            #worse_moves = self.worse_moves(moves_max, moves_min)
            moves_max = list(set(moves_max) - set(better_moves))# - set(worse_moves))
            random.shuffle(moves_max)
            random.shuffle(better_moves)
            #random.shuffle(worse_moves)
            moves = better_moves + moves_max #+ worse_moves


        #random.shuffle(moves)

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

            """
            print("\n\n----------------------\n\n")
            print("Score for this move sequence is: ", score)
            for state in board.board_states:
                print(state)
            print("\n\n----------------------\n\n")
            board.board_states.pop()
            """

            # RESET
            board[m[0]] = _from_fig
            board[m[1]] = _to_fig
            board.player_turn = player
            board.fullmove_number = move_number

            #if score < minscore:
            #    minscore = score
            if score < beta:
                minscore = score
                beta = score
                if beta <= alpha:
                    # print('alpha,beta,minscore: ', alpha, ': ', beta, ': ', minscore)
                    break

        return minscore

    def max_func(self, original_board, board, depth, alpha, beta):

        if original_board.get_time_left() < self.TIME_THRESHOLD:
            print('threshhold')
            return self.evaluateGame(board)

        if board.check_winning_condition(self.color): return math.inf
        if board.check_winning_condition(board.get_enemy(self.color)): return -math.inf

        if depth <= 0:
            return self.evaluateGame(board)

        moves_max = board.generate_valid_moves(board.player_turn)
        if len(moves_max) < 6:
            depth += 0.5
        elif len(moves_max) > 14:
            depth -= 0.5
        #print('len(moves_max) ', len(moves_max))
        #print('depth ', depth)

        moves_min = board.generate_valid_moves(board.get_enemy(self.color))
        # print(board.fullmove_number)
        # if board.fullmove_number<10:
        if len(moves_max) > 11:
            worse_moves = self.worse_moves(moves_max, moves_min)
            moves_max = list(set(moves_max) - set(worse_moves))
            random.shuffle(moves_max)
            random.shuffle(worse_moves)
            moves = moves_max + worse_moves
        else:
            better_moves = self.better_moves(moves_max, moves_min)
            # worse_moves = self.worse_moves(moves_max, moves_min)
            moves_max = list(set(moves_max) - set(better_moves))  # - set(worse_moves))
            random.shuffle(moves_max)
            random.shuffle(better_moves)
            # random.shuffle(worse_moves)
            moves = better_moves + moves_max  # + worse_moves

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

            """
            print("\n\n----------------------\n\n")
            print("Score for this move sequence is: ", score)
            for state in board.board_states:
                print(state)
            print("\n\n----------------------\n\n")
            board.board_states.pop()
            """

            # RESET
            board[m[0]] = _from_fig
            board[m[1]] = _to_fig
            board.player_turn = player
            board.fullmove_number = move_number

            #if score > maxscore:
            #    maxscore = score
            if score > alpha:
                maxscore = score
                alpha = score
                if alpha >= beta:
                    # print('alpha,beta,minscore: ', alpha, ': ', beta, ': ', maxscore)
                    break

        return maxscore


class MrNoviceField:

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

class MrNoviceEval:

    def __init__(self, color, delay=0, threshold=5):
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
                [-8, -9, -10, -10, -9, -8],
                [-6, -7, 5, 5, -7, -6],
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

        score = 0
        team = {'white': -1, 'black': -1, self.color: 1}
        # print("Check winning")
        t1 = time.time()

        t2 = time.time()
        # print("Checking winning in evaluation: ", t2-t1)

        # print("Is in Check")
        t1 = time.time()
        if board.is_in_check(self.color):
            score -= self.score['check']

        if board.is_in_check(board.get_enemy(self.color)):
            score += self.score['check']

        t2 = time.time()
        # print("Checking Is in Check in evaluation: ", t2-t1)

        # print("Calc score")
        t1 = time.time()
        # for coord in board.keys():
        for coord, figure in board.items():
            if figure is not None:
                fig_type = figure.abbriviation.lower()
                fig_color = figure.color
                # print(coord)
                # xy = board.number_notation(coord)
                xy = [int(coord[1]) - 1, board.axis_y.index(coord[0])]
                if fig_color == 'white':
                    xy[0] = 5 - xy[0]
                    # xy[1] = 5 - xy[1]
                fig_val = self.score[fig_type].figure
                if board.fullmove_number < 30:
                    field_val = self.score[fig_type].field_1[xy[0]][xy[1]]
                else:
                    field_val = self.score[fig_type].field_2[xy[0]][xy[1]]
                #syn_value = self.score[fig_type].synergy[fig_color]
                score += team[fig_color] * (fig_val + field_val)
                if fig_type == 'b' or fig_type == 'r':
                    self.score[fig_type].synergy[fig_color] = 1.25
        # print('conventionell ', score)
        # move: from to type color
        """
        board_copy = deepcopy(original_board)
        #print('chosen', chosen)
        #print('board', board_copy)
        for move in chosen:
                xy_from = [int(move[0][1]) - 1, board.axis_y.index(move[0][0])]
                xy_to = [int(move[1][1]) - 1, board.axis_y.index(move[1][0])]
                if move[3] == 'white':
                    xy_from[0] = 5 - xy_from[0]
                   # xy_from[1] = 5 - xy[1]
                    xy_to[0] = 5 - xy_to[0]
                   # xy_to[1] = 5 - xy[1]
                score -= team[move[3]] * self.score[move[2]].field[xy_from[0]][xy_from[1]]
                if board_copy[move[1]] is not None:
                    fig_type = board_copy[move[1]].abbriviation.lower()
                    score += team[move[3]] * (self.score[fig_type].figure + self.score[fig_type].field[xy_to[0]][xy_to[1]])
                score += team[move[3]] * self.score[move[2]].field[xy_to[0]][xy_to[1]]
                board_copy._do_move(move[0], move[1])
        """
        # print('smarter? ', score)
        t2 = time.time()
        # print("Checking Score Calc in evaluation: ", t2-t1)

        # print("Evaluation of board ended.")
        # print(score)
        return score

    def better_moves(self, moves_max, moves_min):
        return [move for move in moves_max if
                move[1] in [i[0] for i in moves_min] or move[0] in [i[1] for i in moves_min]]

    def worse_moves(self, moves_max, moves_min):
        return [move for move in moves_max if move[1] in [i[1] for i in moves_min]]

    def generate_next_move(self, gui):

        # print("Next move will now be generated:")
        t_total = time.time()
        board = deepcopy(gui.chessboard)

        search_depth = 4
        maxscore = -math.inf

        bestmoves = []

        # print("First, valid moves are generated.")
        moves_max = board.generate_valid_moves(board.player_turn)
        if len(moves_max) < 5:
            search_depth = 4
        elif len(moves_max) < 10:
            search_depth = 4
        elif len(moves_max) < 12:
            search_depth = 4
        elif len(moves_max) < 18:
            search_depth = 3.5
        else:
            search_depth = 3
        print('search_depth ', search_depth)
        print('moves_max ', len(moves_max))

        moves_min = board.generate_valid_moves(board.get_enemy(self.color))
        # print(board.fullmove_number)
        # if board.fullmove_number<10:
        better_moves = self.better_moves(moves_max, moves_min)
        # worse_moves = self.worse_moves(moves_max, moves_min)
        moves_max = list(set(moves_max) - set(better_moves))  # - set(worse_moves))
        random.shuffle(moves_max)
        random.shuffle(better_moves)
        # random.shuffle(worse_moves)
        moves = better_moves + moves_max  # + worse_moves

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

                # print("We test main move: ", m, " and the board looks like this:")
                # board_copy.pprint()
                # print("Main move test start.")

                # board.board_states.append(board.to_string())

                score = self.min_func(gui.chessboard, board, search_depth, maxscore, math.inf)
                """
                print("\n\n----------------------\n\n")
                print("Main move " + "(" +m[0] + ", " + m[1] + ")" + " with score " + str(score) + " test end.\n\n")
                for state in board.board_states:
                    print(state)
                print("\n\n----------------------\n\n")
                board.board_states.pop()
                """

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

        # color = self.color
        if original_board.get_time_left() < self.TIME_THRESHOLD:
            print('threshhold')
            return self.evaluateGame(board)

        if board.check_winning_condition(self.color): return math.inf
        if board.check_winning_condition(board.get_enemy(self.color)): return -math.inf
        # game_ends = player_wins or enemy_wins

        if depth <= 0:
            return self.evaluateGame(board)

        moves_max = board.generate_valid_moves(board.player_turn)
        if len(moves_max) < 6:
            depth += 0.5
            # print('+0.5 ', depth)
        elif len(moves_max) > 15:
            depth -= 0.5
            # print('-0.5 ', depth)
        moves_min = board.generate_valid_moves(board.get_enemy(self.color))
        # print(board.fullmove_number)
        # if board.fullmove_number<10:
        better_moves = self.better_moves(moves_max, moves_min)
        # worse_moves = self.worse_moves(moves_max, moves_min)
        moves_max = list(set(moves_max) - set(better_moves))  # - set(worse_moves))
        random.shuffle(moves_max)
        random.shuffle(better_moves)
        # random.shuffle(worse_moves)
        moves = better_moves + moves_max  # + worse_moves
        """ else:
        worse_moves = self.worse_moves(moves_max, moves_min)
        moves_max = list(set(moves_max) - set(worse_moves))
        random.shuffle(moves_max)
        moves = moves_max + worse_moves"""

        # random.shuffle(moves)

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

            """
            print("\n\n----------------------\n\n")
            print("Score for this move sequence is: ", score)
            for state in board.board_states:
                print(state)
            print("\n\n----------------------\n\n")
            board.board_states.pop()
            """

            # RESET
            board[m[0]] = _from_fig
            board[m[1]] = _to_fig
            board.player_turn = player
            board.fullmove_number = move_number

            # if score < minscore:
            #    minscore = score
            if score < beta:
                minscore = score
                beta = score
                if beta <= alpha:
                    # print('alpha,beta,minscore: ', alpha, ': ', beta, ': ', minscore)
                    break

        return minscore

    def max_func(self, original_board, board, depth, alpha, beta):

        if original_board.get_time_left() < self.TIME_THRESHOLD:
            print('threshhold')
            return self.evaluateGame(board)

        if board.check_winning_condition(self.color): return math.inf
        if board.check_winning_condition(board.get_enemy(self.color)): return -math.inf

        if depth <= 0:
            return self.evaluateGame(board)

        moves_max = board.generate_valid_moves(board.player_turn)
        if len(moves_max) < 6:
            depth += 0.5
            # print('+0.5 ', depth)
        elif len(moves_max) > 15:
            depth -= 0.5
            # print('-0.5 ', depth)
        moves_min = board.generate_valid_moves(board.get_enemy(self.color))
        # print(board.fullmove_number)
        # if board.fullmove_number<10:
        better_moves = self.better_moves(moves_max, moves_min)
        # worse_moves = self.worse_moves(moves_max, moves_min)
        moves_max = list(set(moves_max) - set(better_moves))  # - set(worse_moves))
        random.shuffle(moves_max)
        random.shuffle(better_moves)
        # random.shuffle(worse_moves)
        moves = better_moves + moves_max  # + worse_moves

        """ else:
         worse_moves = self.worse_moves(moves_max, moves_min)
         moves_max = list(set(moves_max) - set(worse_moves))
         random.shuffle(moves_max)
         moves = moves_max + worse_moves"""

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

            """
            print("\n\n----------------------\n\n")
            print("Score for this move sequence is: ", score)
            for state in board.board_states:
                print(state)
            print("\n\n----------------------\n\n")
            board.board_states.pop()
            """

            # RESET
            board[m[0]] = _from_fig
            board[m[1]] = _to_fig
            board.player_turn = player
            board.fullmove_number = move_number

            # if score > maxscore:
            #    maxscore = score
            if score > alpha:
                maxscore = score
                alpha = score
                if alpha >= beta:
                    # print('alpha,beta,minscore: ', alpha, ': ', beta, ': ', maxscore)
                    break

        return maxscore