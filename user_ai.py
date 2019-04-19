#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""


An AI player for Othello. 

@author: Catherine Du yd2386
"""

import random
import sys
import time
from math import inf
# You can use the functions in othello_shared to write your AI 
from othello_shared import find_lines, get_possible_moves, get_score, play_move
from heapq import heappush
from heapq import heappop


dp = {}
dp_alphabeta = {}

def compute_utility(board, color):
    """
    Return the utility of the given board state
    (represented as a tuple of tuples) from the perspective
    of the player "color" (1 for dark, 2 for light)
    """
    points = get_score(board)  #p1 is dark, p2 is light
    if color == 1:
        return points[0] - points[1]
    else:
        return points[1] - points[0]
    


############ MINIMAX ###############################

def minimax_min_node(board, color):
    if (board,color) in dp:
        return dp[(board,color)]

    if color == 1:
        opponent_color = 2
    else:
        opponent_color = 1

    
    if len(get_possible_moves(board, color)) == 0:
        return compute_utility(board, opponent_color)

    
    v = inf
    for successor in get_possible_moves(board, color): #iterates over a list of tuples of col and row
        new_board = play_move(board, color, successor[0], successor[1]) #returns a new board 
        v = min(v, minimax_max_node(new_board, opponent_color))
    dp.update({(board, color): v})
    return v


def minimax_max_node(board, color):
    if (board, color) in dp:
        return dp[(board, color)]

    if color == 1:
        opponent_color = 2
    else:
        opponent_color = 1
    if len(get_possible_moves(board, color)) == 0:
        return compute_utility(board,color)

    v = -inf
    for successor in get_possible_moves(board, color): #iterates over a list of tuples 
        new_board = play_move(board, color, successor[0], successor[1]) #returns a new board as tuple
        v = max(v, minimax_min_node(new_board, opponent_color))
        dp.update({(board, color): v})

    return v


    
def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  
    """

    dic = {}
    v = -inf

    if color == 1:
        opponent_color = 2
    else:
        opponent_color = 1 

    for successor in get_possible_moves(board, color): #iterates over a list of tuples 
        new_board = play_move(board, color, successor[0], successor[1]) #returns a new board as tuple
        v = max(v, minimax_min_node(new_board, opponent_color)) 
        if v not in dic:
            dic.update({v: successor})

    return dic[v]


############ ALPHA-BETA PRUNING #####################


def alphabeta_min_node(board, color, alpha, beta, level, limit): 
    if board in dp_alphabeta:
        return dp_alphabeta[board]
    
    if color == 1:
        opponent_color = 2
    else:
        opponent_color = 1

    if len(get_possible_moves(board, color)) == 0 or level == limit:
        return compute_utility(board, opponent_color)

    order = []

    #the PQ should return the lowest utility for this node
    for successor in get_possible_moves(board, color):
        temp_board = play_move(board, color, successor[0], successor[1]) #min node is AI-opponent
        heappush(order, (compute_utility(temp_board, color), temp_board))



    v = inf
    while order:
        min_util = heappop(order) #returns a tuple pair
        new_board = min_util[1] #get the board
        v = min(v, alphabeta_max_node(new_board, opponent_color, alpha, beta, level+1, limit))
        if v <= alpha:
            dp_alphabeta.update({board: v})
            return v  

        beta = min(beta, v)

    dp_alphabeta.update({board: v})
    return v



#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta, level, limit):
    if board in dp_alphabeta:
        return dp_alphabeta[board]
    if color == 1:
        opponent_color = 2
    else:
        opponent_color = 1

    if len(get_possible_moves(board, color)) == 0 or level == limit:
        return compute_utility(board, color)   

    order = []

    #the PQ should return the lowest utility for this node
    for successor in get_possible_moves(board, color):
        temp_board = play_move(board, color, successor[0], successor[1]) #max node is opponent - AI
        heappush(order, (compute_utility(temp_board, opponent_color), temp_board))


    v = -inf
    while order:
        min_util = heappop(order) #returns a tuple pair
        new_board = min_util[1] #get the board
        v = max(v, alphabeta_min_node(new_board, opponent_color, alpha, beta, level+1, limit))
        if v >= beta:
            dp_alphabeta.update({board: v})
            return v
        alpha = max(alpha, v)

    dp_alphabeta.update({board: v})
    return v


def select_move_alphabeta(board, color): 
    dic = {}
    if color == 1:
        opponent_color = 2
    else:
        opponent_color = 1
    v = -inf

    #v = alphabeta_max_node(board, color, -inf, inf)
    for successor in get_possible_moves(board, color):
        new_board = play_move(board, color, successor[0], successor[1])
        v = max(v, alphabeta_min_node(new_board, opponent_color, -inf, inf, 1, 5))
        if v not in dic:
            dic.update({v: successor})
            


    return dic[v]


####################################################
def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    print("Minimax AI") # First line is the name of this AI  
    color = int(input()) # Then we read the color: 1 for dark (goes first), 
                         # 2 for light. 

    while True: # This is the main loop 
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input() 
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over. 
            print 
        else: 
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The 
                                  # squares in each row are represented by 
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)
                    
            # Select the move and send it to the manager 
            #movei, movej = select_move_minimax(board, color)
            movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej)) 


if __name__ == "__main__":
    run_ai()
