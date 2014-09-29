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
parser.add_argument('--config', nargs='?', default=None, help='Changeable paramters')

args = parser.parse_args()
#assign args
use_minimax = args.minimax
use_td = args.td
td_file = args.dest
config = args.config

tictac_controller = controller.TicTacToeController(config)

if __name__ == '__main__':
    tictac_controller.run()