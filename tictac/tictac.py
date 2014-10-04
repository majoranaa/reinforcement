# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 14:19:14 2014

@author: kaiyang
"""

import argparse
from tictactoe import controller

parser = argparse.ArgumentParser(description="Tic-tac-toe with minimax or TD AI capabilities. Default is 2-player mode")
parser.add_argument('--minimax', action='store_true', help='use minimax AI')
parser.add_argument('--td', action='store_true', help='use TD learning AI')
parser.add_argument('--dest', nargs='?', default='q_data.csv', help='File that stores Q data for TD learning')

args = parser.parse_args()
#assign args
mode = 0 # 2-player
if args.minimax:
    mode = 1
elif args.td:
    mode = 2
td_file = args.dest

tictac_controller = controller.TicTacToeController(mode, td_file)

if __name__ == '__main__':
    tictac_controller.run()