"""
Tic Tac Toe Player
"""

import math
import random
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


def player(board, start):
    """
    Returns player who has the next turn on a board.
    """
    no_of_x, no_of_o = 0, 0
    for row in board:
        for position in row:
            if position == X: no_of_x += 1
            elif position == O: no_of_o += 1
    if start == X:
        if no_of_x > no_of_o:
            return O
        else: 
            return X
    elif start == O:
        if no_of_x < no_of_o:
            return X
        else: 
            return O

def board_converter(board: list) -> str:
    out = ""
    for row in board:
        for item in row:
            if item is not None:
                if item == X:
                    out += '❌ '
                else:
                    out += '⭕ '
            else:
                out += '⬜ '
        else:
            out += '\n'
    return out


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action = set()
    for i in board:
        for j in i:
            if j == EMPTY:
                val = board.index(i),i.index(j)
                action.add(val)
    return action


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = list(board)
    try:
        if new_board[action[0]][action[1]] is None:
            new_board[action[0]][action[1]] = player(board)
        else:
            raise ValueError("Already filled position.")
    except:
        raise ValueError("Position out of board.")
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #if board is None:

    for row in board:
        if row[0]==row[1]==row[2] and row[0] != EMPTY:
            return row[0]
    
    for i in range(3):
        if board[0][i]==board[1][i]==board[2][i] and board[0][i] != EMPTY:
            return board[0][i]
    
    if board[0][0]==board[1][1]==board[2][2]:
        if board[0][0] != EMPTY:
            return board[0][0]
    elif board[0][2]==board[1][1]==board[2][0]:
        if board[2][0] != EMPTY:
            return board[2][0]

    
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    else:
        empty_check = []
        for row in board:
            empty_check.append(any([i is None for i in row]))
        if not any(empty_check):
            return True
        else:
            return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X: return 1
    elif winner(board) == O: return -1
    else: return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    turn = player(board)

    return random.choice([action for action in actions(board)])
    