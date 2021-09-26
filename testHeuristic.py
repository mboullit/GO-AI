import Goban 
import importlib
import time
import math
from io import StringIO
import sys
''' 
    This file is used only to debug Players heuristics, and to find correct evaluation for the board
'''
def fileorpackage(name):
    if name.endswith(".py"):
        return name[:-3]
    return name

if len(sys.argv) > 1:
    classNames = [fileorpackage(sys.argv[1])]
else:
    classNames = ['Minjara']

b = Goban.Board()

player1class = importlib.import_module(classNames[0])
player1 = player1class.myPlayer()
player1.newGame(Goban.Board._BLACK)

nextplayer = 0
nextplayercolor = Goban.Board._BLACK
otherplayer = (nextplayer + 1) % 2
othercolor = Goban.Board.flip(nextplayercolor)

b = player1._board

b.push(Goban.Board.name_to_flat('E8'))
b.push(Goban.Board.name_to_flat('E7'))
b.push(Goban.Board.name_to_flat('D8'))
b.push(Goban.Board.name_to_flat('D7'))
b.push(Goban.Board.name_to_flat('F8'))
b.push(Goban.Board.name_to_flat('F7'))
b.push(Goban.Board.name_to_flat('G7'))
b.push(Goban.Board.name_to_flat('F6'))
b.push(Goban.Board.name_to_flat('G6'))
b.push(Goban.Board.name_to_flat('E5'))
b.push(Goban.Board.name_to_flat('C7'))
b.push(Goban.Board.name_to_flat('D6'))
b.push(Goban.Board.name_to_flat('C6'))
b.push(Goban.Board.name_to_flat('D5'))
b.push(Goban.Board.name_to_flat('C5'))
b.push(Goban.Board.name_to_flat('E3'))
b.push(Goban.Board.name_to_flat('G3'))
b.push(Goban.Board.name_to_flat('J9'))
b.push(Goban.Board.name_to_flat('G4'))
b.push(Goban.Board.name_to_flat('D3'))
b.push(Goban.Board.name_to_flat('F5'))
b.push(Goban.Board.name_to_flat('F3'))
b.push(Goban.Board.name_to_flat('G5'))
b.push(Goban.Board.name_to_flat('F4'))
b.push(Goban.Board.name_to_flat('C4'))
b.push(Goban.Board.name_to_flat('J1'))
b.push(Goban.Board.name_to_flat('C3'))
b.push(Goban.Board.name_to_flat('A1'))

# b.push(Goban.Board.name_to_flat('E5'))
# b.push(Goban.Board.name_to_flat('H1'))
# print(player1.liberties_in_manhattan_distance(b.name_to_flat('D7'),3,b._WHITE,True))

for m in b.weak_legal_moves():
    if b.push(m):
        # probably moves must be pushed on player
        ret = player1.alphabeta(2,-math.inf,math.inf,True)
        print(b.flat_to_name(m),ret)
    b.pop()
b.push(Goban.Board.name_to_flat('A9'))
player1._board.prettyPrint()
b.prettyPrint()
print(player1._board.diff_stones_captured())
print(player1._board.diff_stones_board())
