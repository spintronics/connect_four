import random
import copy

"""
Created on Fri Nov 20 02:24:44 2020

@author: Nicholas Mann
"""


def transpose(board):
    columns = [[] for _ in range(len(board[0]))]
    for row in board:
        for index, item in enumerate(row):
            columns[index].append(item)

    return columns


def copy_board(board):
    result = []
    for row in board:
        result.append(row[:])

    return result


def flip(board):
    return [row[::-1] for row in board]


def diagonals(board):
    diags = [[] for _ in range(12)]
    diagonal_indexes = [[x for x in range(len(board[0]))]]
    for i in range(len(board)):
        diagonal_indexes.append([x + 1 for x in diagonal_indexes[-1]])
    for y in range(len(board[0])):
        for x in range(len(board)):
            dex = diagonal_indexes[x][y]
            # if not (dex in diags): diags[dex] = []
            diags[dex].append(board[x][y])

    return diags


def connect_n(rows, player, n):
    str_row = "".join([str(row) for row in rows])
    if str(player) * n in str_row:
        return True
    return False


def check_win(board, player, n=3):

    for row in board + transpose(board) + diagonals(board) + diagonals(flip(board)):
        if connect_n(row, player, n):
            return True
    return False


def valid_moves(board):
    moves = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[x][y] == 0:
                moves.append([x, y])
    return moves


def random_move(board):
    valid = valid_moves(board)
    if not len(valid):
        return -1
    return random.choice(valid) if len(valid) else []


def place_piece(board, position, player):
    board = copy_board(board)
    board[position[0]][position[1]] = player
    return board


def generate_move(board):

    """
    this function returns a position(move)
    """

    # valid_moves(board) -> [position]
    # place_piece(board, position, player) -> board
    # check_win(board, player) -> True/False
    #

    positions = valid_moves(board)

    # this checks to see which moves are still available on the board
    # this checks to see if the positioned pick is a win for player 1

    if not len(positions):
        return -1

    good_moves = []

    # if theres a move that would win, make it
    for position in positions:
        new_board = place_piece(board, position, player)
        # this will go through each move in the available moves
        if check_win(new_board, player):
            # if there is a move that will win this will find it
            return position

        oponent_will_win = False

        for next_position in positions:
            if next_position != position:
                next_board = place_piece(new_board, next_position, 2)
                if check_win(next_board, 2):
                    oponent_will_win = True
                    break

        if not oponent_will_win:
            good_moves.append(position)

    if not len(good_moves):
        return random.choice(positions)

    return random.choice(good_moves)


blank_board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

player = 1

wins = [0, 0, 0]

while sum(wins) < 100:
    ai_player = 1
    board = copy.deepcopy(blank_board)
    while True:
        move = generate_move(board) if player == 1 else random_move(board)
        if move == -1:
            wins[2] += 1
            break
        board = place_piece(board, move, player)
        if check_win(board, player):
            if player == ai_player:
                wins[0] += 1
            else:
                wins[1] += 1
            break
        player = 1 if player == 2 else 2

print(wins)