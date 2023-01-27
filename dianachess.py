from gui import BoardGuiTk
from engine import *
import tkinter as tk
from board import *
import sys, getopt


def display(chessboard,turn_time):
    root = tk.Tk()
    root.title("Simple Python Chess")

    gui = BoardGuiTk(root, chessboard)
    gui.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    gui.draw_pieces()
    label = tk.Label(text="")
    label.pack()
    gui.label = label
    update_clock(chessboard,label,turn_time,turn_time,"white",root)
    stopClock(root,chessboard,gui)
    startGame(root,chessboard,gui)
    root.mainloop()

# 1 = Human
# 2 = Mr. Random 
# 3 = Mr. Novice
# 4 = Mr. Expert
# 5 = Custom
# 6 = Mr. NovicePruning

if __name__ == "__main__":
    
    TURN_TIME = 30
    PLAYER_2 = 5
    PLAYER_1 = 3
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'w:b:t:')
    except getopt.GetoptError:
        print('dianachess.py -w <white player> -b <black player -t <turn time>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-w':
            if arg == 'Human':
                PLAYER_1 = 1
            elif arg == 'MrRandom':
                PLAYER_1 = 2
            elif arg == 'MrNovice':
                PLAYER_1 = 3
            elif arg == 'MrExpert':
                PLAYER_1 = 3
            elif arg == 'Student':
                PLAYER_1 = 5
            elif arg == 'MrNovicePruning':
                PLAYER_1 = 6
            elif arg == 'MrNovicePruningBetter1':
                PLAYER_1 = 7
            elif arg == 'MrNoviceField':
                PLAYER_1 = 8
            elif arg == 'MrNoviceEval':
                PLAYER_1 = 9
            else:
                PLAYER_1 = 1
                print('Selecting human as white player.')
                print('Please give one of the following arguments for white player:'
                      '\nHuman\nMrRandom\nMrNovice\nMrExpert\nStudent')
        elif opt == '-b':
            if arg == 'Human':
                PLAYER_2 = 1
            elif arg == 'MrRandom':
                PLAYER_2 = 2
            elif arg == 'MrNovice':
                PLAYER_2 = 3
            elif arg == 'MrExpert':
                PLAYER_2 = 3
            elif arg == 'Student':
                PLAYER_2 = 5
            elif arg == 'MrNovicePruning':
                PLAYER_1 = 6
            elif arg == 'MrNovicePruningBetter1':
                PLAYER_1 = 7
            elif arg == 'MrNoviceField':
                PLAYER_1 = 8
            elif arg == 'MrNoviceEval':
                PLAYER_1 = 9
            else:
                PLAYER_2 = 1
                print('Selecting human as black player.')
                print('Please give one of the following arguments for black player:'
                      '\nHuman\nMrRandom\nMrNovice\nMrExpert\nStudent')
        elif opt == '-t':
            TURN_TIME = int(arg)
    
    game = Board(PLAYER_1, PLAYER_2)
    display(game,TURN_TIME)
