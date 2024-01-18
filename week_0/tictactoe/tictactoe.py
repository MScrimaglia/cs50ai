"""
Tic Tac Toe Player
"""

import math
import copy
from datetime import datetime

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0

    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1

    if x_count > o_count:
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    res = set()

    for row_index in range(0, 3):
        for cell_index in range(0, 3):
            if board[row_index][cell_index] == EMPTY:
                res.add((row_index, cell_index))

    return res


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    row = action[0]
    cell = action[1]
    result = copy.deepcopy(board)

    if board[row][cell] != EMPTY or row not in range(0, 3) or cell not in range(0, 3):
        raise RuntimeError

    result[row][cell] = player(board)

    return result


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    def row_winner(board):
        for row in board:
            if row[0] == row[1] == row[2] != None:
                return row[0]
        return None
    
    def column_winner(board):
        for column_index in range(0, 3):
            if board[0][column_index] == board[1][column_index] == board[2][column_index] != None:
                return board[0][column_index]
        return None
    
    def diagonal_winner(board):
        if (board[0][0] == board[1][1] == board[2][2] != None or
                board[0][2] == board[1][1] == board[2][0] != None):
            return board[1][1]
        return None
    
    if row_winner(board):
        return row_winner(board)
    if column_winner(board):
        return column_winner(board)
    return diagonal_winner(board)


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    def all_cells_filled(board):
        for row in board:
            for cell in row:
                if cell == EMPTY:
                    return False
        return True

    if winner(board) or all_cells_filled(board):
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    if board == initial_state():
        return (0, 0)
    
    def max_value(state, alpha, beta):
        if terminal(state):
            return utility(state)
        v = -math.inf
        for action in actions(state):
            v = max(v, min_value(result(state, action), alpha, beta))
            alpha = max(alpha, v)
            if beta <= alpha:
                return v
        return v
    
    def min_value(state, alpha, beta):
        if terminal(state):
            return utility(state)
        v = math.inf
        for action in actions(state):
            v = min(v, max_value(result(state, action), alpha, beta))
            beta = min(beta, v)
            if beta <= alpha:
                return v
        return v
    
    optimal_action = None
    current_player = player(board)

    if current_player == X:
        maximize = True
        res_utility = -math.inf
    elif current_player == O:
        maximize = False
        res_utility = math.inf

    alpha = -math.inf
    beta = math.inf

    for action in actions(board):
        if maximize:
            action_max_value = min_value(result(board, action), alpha, beta)
            if action_max_value > res_utility:
                res_utility = action_max_value
                optimal_action = action
        else:
            action_min_value = max_value(result(board, action), alpha, beta)
            if action_min_value < res_utility:
                res_utility = action_min_value
                optimal_action = action

    return optimal_action