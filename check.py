############################################

#ADDED CAHCHING

###########################################

def alphabeta_min_node(board, color, alpha, beta): 
    if board in dp_alphabeta:
        return dp_alphabeta[board]
    
    if color == 1:
        opponent_color = 2
    else:
        opponent_color = 1

    if len(get_possible_moves(board, color)) == 0:
        return compute_utility(board, opponent_color)

    v = inf
    for successor in get_possible_moves(board, color): #iterates over a list of tuples of col and row
        new_board = play_move(board, color, successor[0], successor[1]) #returns a new board 
        v = min(v, alphabeta_max_node(new_board, opponent_color, alpha, beta))
        if v <= alpha:
            dp_alphabeta.update({board: v})
            return v  


        beta = min(beta, v)

    dp_alphabeta.update({board: v})
    return v



#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta):
    if board in dp_alphabeta:
        return dp_alphabeta[board]
    if color == 1:
        opponent_color = 2
    else:
        opponent_color = 1

    if len(get_possible_moves(board, color)) == 0:
        return compute_utility(board, color)

    v = -inf
    for successor in get_possible_moves(board, color): #iterates over a list of tuples 
        new_board = play_move(board, color, successor[0], successor[1]) #returns a new board as tuple
        v = max(v, alphabeta_min_node(new_board, opponent_color, alpha, beta))
        if v >= beta:
            dp_alphabeta.update({board: v})
            return v
        alpha = max(alpha, v)

    dp_alphabeta.update({board: v})
    return v



######################### ADDED ORDER NODE HEURISTIC


######################################################
def alphabeta_min_node(board, color, alpha, beta): 
    if board in dp_alphabeta:
        return dp_alphabeta[board]
    
    if color == 1:
        opponent_color = 2
    else:
        opponent_color = 1

    if len(get_possible_moves(board, color)) == 0:
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
        v = min(v, alphabeta_max_node(new_board, opponent_color, alpha, beta))
        if v <= alpha:
            dp_alphabeta.update({board: v})
            return v  

        beta = min(beta, v)

    dp_alphabeta.update({board: v})
    return v



#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta):
    if board in dp_alphabeta:
        return dp_alphabeta[board]
    if color == 1:
        opponent_color = 2
    else:
        opponent_color = 1

    if len(get_possible_moves(board, color)) == 0:
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
        v = max(v, alphabeta_min_node(new_board, opponent_color, alpha, beta))
        if v >= beta:
            dp_alphabeta.update({board: v})
            return v
        alpha = max(alpha, v)

    dp_alphabeta.update({board: v})
    return v


# #alphabeta_min_node(board, color, alpha, beta, level, limit)
# def alphabeta_min_node(board, color, alpha, beta, level, limit): 
#     if (board, color) in dp_alphabeta:
#         return dp_alphabeta[(board, color)]
    
#     if color == 1:
#         opponent_color = 2
#     else:
#         opponent_color = 1

#     if len(get_possible_moves(board, color)) or level > limit:
#         return compute_utility(board, opponent_color)

#     order = []

#     #the PQ should return the lowest utility for this node
#     for successor in get_possible_moves(board, color):
#         temp_board = play_move(board, color, successor[0], successor[1]) #min node is AI-opponent
#         heappush(order, (compute_utility(temp_board, color), temp_board))



#     v = inf
#     while order:
#         min_util = heappop(order) #returns a tuple pair
#         new_board = min_util[1] #get the board
#         #current_color = min_util[1][1]
#         v = min(v, alphabeta_max_node(new_board, opponent_color, alpha, beta, level+1, limit))
#         if v <= alpha:
#             dp_alphabeta.update({(board, color): v})
#             return v  

#         beta = min(beta, v)

#     dp_alphabeta.update({(board, color): v})
#     return v



# #alphabeta_max_node(board, color, alpha, beta, level, limit)
# def alphabeta_max_node(board, color, alpha, beta, level, limit):
#     if (board, color) in dp_alphabeta:
#         return dp_alphabeta[(board, color)]

#     if color == 1:
#         opponent_color = 2
#     else:
#         opponent_color = 1

#     if len(get_possible_moves(board, color)) == 0 or level > limit:
#         return compute_utility(board, color)   

#     order = []

#     #the PQ should return the lowest utility for this node
#     for successor in get_possible_moves(board, color):
#         temp_board = play_move(board, color, successor[0], successor[1]) #max node is opponent - AI
#         heappush(order, (compute_utility(temp_board, opponent_color), temp_board))


#     v = -inf
#     while order:
#         min_util = heappop(order) #returns a tuple pair
#         new_board = min_util[1] #get the board
#         v = max(v, alphabeta_min_node(new_board, opponent_color, alpha, beta, level+1, limit))
#         if v >= beta:
#             dp_alphabeta.update({(board, color): v})
#             return v
#         alpha = max(alpha, v)

#     dp_alphabeta.update({(board, color): v})
#     return v
