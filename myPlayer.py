# -*- coding: utf-8 -*-
''' 
This file contains the content of the AI player using MinMax with AlphaBeta Prunning
'''

from abc import get_cache_token
import time
import math

from numpy import lib
import Goban 
import numpy as np
from random import choice
from playerInterface import *

class myPlayer(PlayerInterface):
    ''' 
        The main player class for our team, uses MinMax with AlphaBeta prunning
    '''
    
    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None
        self._visited = np.zeros((9,9))
        self._counted = np.zeros((9,9))
        self._turn = 0
        self._last_opponent_move = -1
        self._my_last_move = -1
        self._time = 0

    def getPlayerName(self):
        return "Minjara"

    def getPlayerMove(self):
        tmp_time = time.time()
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS"
        
        moves = self._board.weak_legal_moves()
        move = None
        value = 0
        if self._time < 7*60:
            print(self._time)
            if self._turn == 0:
                d = list(self._opennings.keys())
                move = d[0]
            elif self._turn <= 5:
                openning_area = self.get_openning_move_array(moves)
                (move, value) = self.applyAlphaBeta(1,openning_area)
            if move == None:
                (move, value) = self.applyAlphaBeta(1,moves)
        else:
            moves = self._board.legal_moves()
            move = choice(moves)
        print("i am playing now !!")
        self._board.push(move)
        self._time += time.time() - tmp_time
        print(self._time)
        self._my_last_move = move
        self._turn += 1

        # New here: allows to consider internal representations of moves
        print("I am playing ", self._board.move_to_str(move))
        print("My heuristic value", value)
        print("My current board :")
        self._board.prettyPrint()
        # move is an internal representation. To communicate with the interface I need to change if to a string
        return Goban.Board.flat_to_name(move) 

    def playOpponentMove(self, move):
        print("Opponent played ", move) # New here
        # the board needs an internal represetation to push the move.  Not a string
        self._last_opponent_move = self._board.name_to_flat(move)
        self._board.push(Goban.Board.name_to_flat(move)) 

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

        # Initiating some variables that will help on oppenings
        import gzip, os.path
        import json

        # File that contains 9x9 pro matchs to guess opennings
        json_file = "games.json"

        if not os.path.isfile(json_file):
            return
      
        with open('games.json', 'r') as f:
            data = json.load(f)
        
        moves = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'J1',
                 'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'J2',
                 'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'J3',
                 'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'J4', 
                 'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'J5',
                 'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6', 'J6',
                 'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'J7',
                 'A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'J8',
                 'A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9', 'J9',
                 'PASS']

        if color == self._board._BLACK:
            d = { i : 0 for i in moves }
            for i in data:
                if i['winner'] == 'B':
                    for j in range(0,10,2):
                        d[i['moves'][j]] += 1
        else:
            d = { i : 0 for i in moves }
            for i in data:
                if i['winner'] == 'W':
                    for j in range(1,11,2):
                        d[i['moves'][j]] += 1

        # Sorting the dictionnary to get the top oppenning move easily
        self._opennings = {self._board.name_to_flat(k): v for k, v in sorted(d.items(), key=lambda item: -item[1])}
    
    def get_openning_move_array(self, moves):
        max = 0
        d = list(self._opennings.keys())
        final_moves = []
        for i in range(0,10):
            if d[i] in moves:
                final_moves.append(d[i])
        return final_moves


    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")

    def around_moves(self, moves):
        '''
            Function that calculates the area around my player's last move and opponent's
            last move with depth = 2
        '''
        neighbors = self._board._get_neighbors(self._my_last_move) + self._board._get_neighbors(self._last_opponent_move)
        area = [] + neighbors
        final_area = []
        for nb in neighbors:
            area += self._board._get_neighbors(nb)
        area = list(dict.fromkeys(area))
        print(area)
        for nb in moves:
            if self._board[nb] == self._board._EMPTY and nb in neighbors:
                final_area.append(nb)
        return final_area

    def liberties_in_manhattan_distance(self,move,depth,color,init):
        '''
            Manhattan distance is a measure of the distance between two vertices used 
            in computer go. It is determined as the number of horizontal and vertical 
            steps one has to take to go from one stone to another.
                Used for the evaluation function
        '''
        (cl, lg) = self._board.unflatten(move)

        if depth == 0:
            if self._board[move] == self._board._EMPTY and self._counted[cl][lg] == 0 :
                self._visited[cl][lg] = 1
                self._counted[cl][lg] = 1
                return 1
            return 0

        (cl, lg) = self._board.unflatten(move)
        self._visited[cl][lg] = 1
        liberties = 0
    
        neighbors, unvisited = [], []
        if(init):
            area = self.get_color_area(move, color)
            for n in area:
                local_neighbors = self._board._get_neighbors(n)
                neighbors = neighbors + local_neighbors
            for nb in neighbors:
                (cl, lg) = self._board.unflatten(nb)
                if self._visited[cl][lg] == 0 and not(nb in unvisited):
                    self._visited[cl][lg] = 1
                    unvisited = unvisited + [nb]

        else:
            neighbors = self._board._get_neighbors(move)
            for nb in neighbors:
                (cl, lg) = self._board.unflatten(nb)
                if self._visited[cl][lg] == 0 and not(nb in unvisited):
                    self._visited[cl][lg] = 1
                    unvisited = unvisited + [nb]

        for nb in unvisited:
            if self._board[nb] == color:
                liberties += self.liberties_in_manhattan_distance(nb,depth,color,True)
            elif self._board[nb] == self._board._EMPTY:
                liberties += self.liberties_in_manhattan_distance(nb,depth-1,color,False)
        return liberties

    def get_color_area(self, move, color):
        '''
            Function that calculates the whole area connected to move with same color
        '''
        if self._board[move] != color:
            (cl, lg) = self._board.unflatten(move)
            self._visited[cl][lg] = 0
            return []
        else:
            area = [move]
            for nb in self._board._get_neighbors(move):
                (cl, lg) = self._board.unflatten(nb)
                if self._visited[cl][lg] == 0:
                    self._visited[cl][lg] = 1
                    area = area + self.get_color_area(nb, color)
            return area

    def get_quads_number(self,color):
        '''
            Function that counts the number of occurrences of the three quad types
            Q1, Q3, and Qd in the board.
            Q1 = one colored stone in a square
            Q2 = two stones with same color in diagonal in square
            Q3 = three stones with same color in a square
        '''
        quads1,quads2,quads3 = 0,0,0
        # The borders are counted as empty, that's why we go from -1 to 9
        for i in range(-1,10):
            for j in range(-1,10):
                coord = (i,j)
                type = self.get_quad_type(coord,color)
                quads1 += (type == 1)
                quads2 += (type == 2)
                quads3 += (type == 3)
        return (quads1,quads2,quads3)

    def get_quad_type(self,coord,color):
        '''
            Function used in get_quads_number, determines quad's type
        '''
        (i,j) = coord
        colored = 0
        if i >= 0 and i <= 8 and j >= 0 and j <= 8:
            colored += (self._board[self._board.flatten((i,j))] == color)
        if i <= 7 and j >= 0 and j <= 8:
            colored += (self._board[self._board.flatten((i+1,j))] == color)
        if i >= 0 and i <= 8 and j <= 7:
            colored += (self._board[self._board.flatten((i,j+1))] == color)
        if i <= 7 and j <= 7:
            colored += (self._board[self._board.flatten((i+1,j+1))] == color)

        if colored == 1:
            return 1
        if colored == 3:
            return 3
        if colored == 2 and i >= 0 and j >= 0 and i <= 7 and j <= 7:
            if self._board[self._board.flatten((i,j))] == color and self._board[self._board.flatten((i+1,j+1))] == color:
                return 2
            elif self._board[self._board.flatten((i+1,j))] == color and self._board[self._board.flatten((i,j+1))] == color:
                return 2
        return 0

    def euler_number(self,color):
        '''
            Function that calculates the euler number
        '''
        (Q1,Q2,Q3) = self.get_quads_number(color)
        return (Q1 - Q3 + 3*Q2)/4

    def to_zero_visited(self):
        '''
            Remains the two matrix used for heuristic to zero
        '''
        self._visited = np.zeros((9,9))
        self._counted = np.zeros((9,9))

    def ponnuki_evaluate(self,a,b,g,d,eps,color):
        '''
            Evaluation function : the parameters advised for small border 5x5 ..etc, are:
            a = 1, b = 1, g = 1/2, d = 3, eps = -4, for our case we used the file test.py
            to visualize the evaluation of some board to find good params.
        '''
        f1,f2,f3,f4 = 0,0,0,0
        self.to_zero_visited()
        for fcoord in range(self._board._BOARDSIZE**2):
            (cl, lg) = self._board.unflatten(fcoord)
            if self._board[fcoord] == self._board._BLACK and self._visited[cl][lg] == 0:
                f1 += self.liberties_in_manhattan_distance(fcoord,1,self._board._BLACK,True)
                f2 += self.liberties_in_manhattan_distance(fcoord,2,self._board._BLACK,True)
                f3 += self.liberties_in_manhattan_distance(fcoord,3,self._board._BLACK,True)
            if self._board[fcoord] == self._board._WHITE and self._visited[cl][lg] == 0:
                f1 -= self.liberties_in_manhattan_distance(fcoord,1,self._board._WHITE,True)
                f2 -= self.liberties_in_manhattan_distance(fcoord,2,self._board._WHITE,True)
                f3 -= self.liberties_in_manhattan_distance(fcoord,3,self._board._WHITE,True)

        f4 += self.euler_number(self._board._BLACK)
        f4 -= self.euler_number(self._board._WHITE)
        captured = self._board.diff_stones_captured()
        if color == self._board._WHITE:
            f1, f2, f3, f4, captured = -f1, -f2, -f3, -f4, -captured
        return min(max(a*f1 + b*f2 + g*f3,-d),d) + eps*f4

    def heuristic(self):
        ''' 
            Heuristic evaluation used for our MinMax with AlphaBeta prunning algo. 
        '''
        a, b, g, d, eps = 1, 1, 0.5, 3, 4
        # a, b, g, d, eps = 1, 1, 0.5, 3, 4 # best args founded
        # a, b, g, d, eps = 1, 1, 1, 8, 4
        return self.ponnuki_evaluate(a,b,g,d,eps,self._mycolor)

    def alphabeta(self, depth, alpha, beta, maximizingPlayer):
        '''
            Function that implements the MinMax algorithm with AlphaBeta prunning
        '''
        if depth == 0:
            return self.heuristic()
        
        # To verify
        if self._board.is_game_over():
            res = self._board.result()
            if res == "1-0":
                return 1000
            elif res == "0-1":
                return -1000
            else:
                return 0
        
        if maximizingPlayer:
            value = -math.inf
            for m in self._board.weak_legal_moves():
                if self._board.push(m):
                    value = max(value, self.alphabeta(depth-1,alpha,beta,False))
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
                self._board.pop()
            return value

        else:
            value = math.inf
            for m in self._board.weak_legal_moves():
                if self._board.push(m):
                    value = min(value, self .alphabeta(depth-1,alpha,beta,True))
                    alpha = min(beta, value)
                    if beta <= alpha:
                        break
                self._board.pop()
            return value

    def applyAlphaBeta(self,depth,moves):
        '''
            Function that applies the MinMax with AlphaBeta algo.
        '''
        if self._board.is_game_over() or depth == 0 or len(moves) == 0:
            return None

        v = -math.inf
        c = None
        for m in moves:
            if self._board.push(m):
                ret = self.alphabeta(depth,-math.inf,math.inf,True)
                if ret > v:
                    print(ret)
                    c = m
                    v = ret
            self._board.pop()

        return (c, v)