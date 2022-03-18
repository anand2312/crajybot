"""
Tic Tac Toe Player
"""

import random

X = (
    "<:x1:757950268875735041>",
    "<:x2:757950318045560902>",
    "<:x3:757950402661449819>",
    "<:x4:757950360336728086>",
)
O = (
    "<:o1:757945971123683418>",
    "<:o2:757945990090326068>",
    "<:o3:757946006322282507>",
    "<:o4:757946024064057395>",
)
EMPTY = (
    "<:empty:755333349043863623>",
    "<:empty:755333349043863623>",
    "<:empty:755333349043863623>",
    "<:empty:755333349043863623>",
)
board = {
    "↖": EMPTY,
    "⬆": EMPTY,
    "↗": EMPTY,
    "⬅": EMPTY,
    "⏺": EMPTY,
    "➡": EMPTY,
    "↙": EMPTY,
    "⬇": EMPTY,
    "↘": EMPTY,
}


def initial_state():
    """
    Returns starting state of the board.
    """
    return [board[i] for i in board]


def update_board(main_embed, reaction, player):
    board[reaction] = player
    main_embed.description = update_board_embed()
    return main_embed


def update_board_embed():
    board_result = ""
    for i in range(3):
        line1 = ""
        line2 = ""
        for j in ["↖", "⬆", "↗", "⬅", "⏺", "➡", "↙", "⬇", "↘"][i * 3 : (i + 1) * 3]:
            line1 += "".join(board[j][0:2])
            line2 += "".join(board[j][2:4])
        board_result += line1 + "\n" + line2 + "\n"
    return board_result


def reset_board():
    global board
    board = {
        "↖": EMPTY,
        "⬆": EMPTY,
        "↗": EMPTY,
        "⬅": EMPTY,
        "⏺": EMPTY,
        "➡": EMPTY,
        "↙": EMPTY,
        "⬇": EMPTY,
        "↘": EMPTY,
    }


def actions(board):  # NOT USED YET
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    action = list()
    for row, i in enumerate(board):
        for position, j in enumerate(i):
            if j is None:
                val = row, position
                action.append(val)
    return action


def valid_action(move: tuple, board: list) -> bool:  # NOT USED YET
    return move in actions(board)


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # if board is None:
    current_board = initial_state()
    for i in range(3):
        if (
            current_board[i * 3]
            == current_board[i * 3 + 1]
            == current_board[i * 3 + 2]
            != EMPTY
        ):
            return True
    for i in range(3):
        if current_board[i] == current_board[i + 3] == current_board[i + 6] != EMPTY:
            return True
    if current_board[0] == current_board[4] == current_board[8] != EMPTY:
        return True
    if current_board[2] == current_board[4] == current_board[6] != EMPTY:
        return True
    return False


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is True:
        return True
    else:
        for i in board:
            if i == EMPTY:
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


def minimax(board):  # MIGHT DEVELOP LATER
    """
    Returns the optimal action for the current player on the board.
    """
    ...
