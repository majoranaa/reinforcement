# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 16:41:32 2014

@author: Kai
"""
import numpy as np

# AI is always O (2)

class MinimaxPlayer:
    def __init__(self):
        self.board = None
    def request_move(self,game):
        self.board = np.copy(game.boxes)
        move = self.minimax()
        game.boxes[move[0]][move[1]] = 2-game.x_turn
        return move
    
    def gameEnded():
        
    def minimax():
        best_move = (-1,-1)
        if self.gameEnded():
            return best_move
        else:
            value = -2
            for i in range(3):
                for j in range(3):
                    if not self.board[i][j]:
                        self.board[i][j] = 2
                        temp = self.minMove():
    
    def minMove():
        if self.gameEnded():
            return self.state
    def maxMove():
        if self.gameEnded():
            return self.state
        else:
            best_move = (-1,-1)
            value = -2 # loss: -1 Draw: 0 Win: 1
            for i in range(3):
                for j in range(3):
                    if not self.board[i][j]:
                        min_move = MinMo
                    
    
class TDPlayer:
    def request_move(self,game):
        chosen = (-1,-1)
        chose = False
        for i in range(3):
            for j in range(3):
                if not game.boxes[i][j] and not chose:
                    game.boxes[i][j] = 2-game.x_turn
                    chosen = (i,j)
                    chose = True
        return chosen

class TicTacToeGame:
    def __init__(self, mode, td_file):
        self.x_turn = True
        self.won = False
        self.boxes = np.zeros((3,3),dtype=int)
        self.count = 0
        
        self.player = None # 2-player
        if mode == 1: # minimax
            self.player = MinimaxPlayer()
        elif mode == 2: # TD
            self.player = TDPlayer(td_file)
            
        self.mode = mode
        
    def draw(self):
        return self.count >= 9 and not self.won
                
    def checkWon(self, last_point):
        x = last_point[0]
        y = last_point[1]
        # column
        for i in range(3):
            if self.boxes[x][i] != 2-self.x_turn:
                break
            if i == 2:
                self.won = True
                
        # row
        for i in range(3):
            if self.boxes[i][y] != 2-self.x_turn:
                break
            if i == 2:
                self.won = True
        
        # diag
        for i in range(3):
            if self.boxes[i][i] != 2-self.x_turn:
                break
            if i == 2:
                self.won = True
                
        # anti-diag
        for i in range(3):
            if self.boxes[i][2-i] != 2-self.x_turn:
                break
            if i == 2:
                self.won = True
   
    def select(self, x, y):
        if self.boxes[x][y]: return
        
        if self.x_turn:
            self.boxes[x][y] = 2 # X (shorter ver is 2-self.x_turn)
        else:
            self.boxes[x][y] = 2 # O
        
        self.checkWon((x,y))
        self.count = self.count + 1
        if not self.won: self.x_turn = not self.x_turn
        
        if self.mode and not self.won: # request move if game isn't over
            self.checkWon(self.player.request_move(self)) # request_move modifies game's board
            self.count = self.count + 1
            if not self.won: self.x_turn = not self.x_turn