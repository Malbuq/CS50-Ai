"""
Tic Tac Toe Player
"""

import math
import copy

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

    amount_X = 0
    amount_O = 0

    for row in board:
        for cell in row:
            if cell == X:
                amount_X += 1
            elif cell == O:
                amount_O += 1
    
    if amount_O < amount_X:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                detected_action = (i,j)
                possible_actions.add(detected_action)
    
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    if board[i][j] is not EMPTY:
        raise Exception("Invalid action")
    
    curr_player = player(board)
    board_after_action = copy.deepcopy(board)
    board_after_action[i][j] = curr_player

    return board_after_action


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #Check for rows
    for row in board:
        if all(cell == 'X' for cell in row):
            return 'X'
        elif all(cell == 'O' for cell in row):
            return 'O'
    
    #Check of columns
    for col_idx in range(len(board)):
        curr_X_points = curr_O_points = 0

        for row_idx in range(len(board)):
            if board[row_idx][col_idx] == X:
                curr_X_points += 1
            elif board[row_idx][col_idx] == O:
                curr_O_points += 1
        
        if curr_X_points == 3:
            return X
        elif curr_O_points == 3:
            return O
    
    #Check for diagnal
    right_diag_X = right_diag_O = left_diag_X = left_diag_O = 0

    for row_idx in range(len(board)):
        if board[row_idx][row_idx] == X:
            right_diag_X += 1

        elif board[row_idx][row_idx] == O:
            right_diag_O += 1

        if board[row_idx][len(board[row_idx]) - 1 - row_idx] == X:
            left_diag_X += 1

        elif board[row_idx][len(board[row_idx]) - 1 - row_idx] == O:
            left_diag_O += 1
    
    if right_diag_X == 3 or left_diag_X == 3:
        return X
    elif right_diag_O == 3 or left_diag_O == 3:
        return O

    return None
        
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    elif len(actions(board)) == 0:
        return True
    else:
        return False
    
def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """ 
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    curr_player = player(board)

    if curr_player == X:
        _, move = max_value(board)
        return move
    else:
        _, move = min_value(board)
        return move

def min_value(board):
    if terminal(board):
        return utility(board), None
    
    curr_min = float('inf')
    move = None

    for action in actions(board):
        point, curr_move = max_value(result(board, action))
        if point < curr_min:
            curr_min = point
            move = action

    return curr_min, move    
    
def max_value(board):
    if terminal(board):
        return utility(board), None
    
    curr_max = float('-inf')
    move = None

    for action in actions(board):
        point, curr_move = min_value(result(board, action))
        if point > curr_max:
            curr_max = point
            move = action

    return curr_max, move    
    