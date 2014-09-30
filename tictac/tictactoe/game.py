# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 16:41:32 2014

@author: Kai
"""
import numpy as np

class TicTacToeGame:
    def __init__(self):
        self.x_turn = True
        self.won = False
        self.boxes = np.zeros((3,3),dtype=int)
        self.count = 0
        
    def draw(self):
        return self.count == 9 and not self.won
        
    def select(self, x, y):
        if self.boxes[x][y]: return
        
        if self.x_turn:
            self.boxes[x][y] = 1
        else:
            self.boxes[x][y] = 2
            
        # check if won
            
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
        self.x_turn = not self.x_turn
        self.count = self.count + 1