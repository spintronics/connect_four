import logic
import random

"""
Created on Fri Nov 20 02:24:44 2020

@author: Nicholas Mann
"""
empty_board = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]


def generate_move(board, player):

    """
    this function returns a position(move)
    """

    # valid_moves(board) -> [position]
    # drop_piece(board, position, player) -> board
    # check_win(board, player) -> True/False
    #

    positions = logic.valid_moves(board)
    opponent = 1 if player == 2 else 2

    if not len(positions):
        return -1

    good_moves = []

    for position in positions:
        new_board = logic.drop_piece(player, position, board)
        # if theres a move that would win, make it
        winner = logic.check_win(new_board)
        if winner and winner[0] == player:
            return position

        oponent_will_win = False
        next_positions = logic.valid_moves(new_board)

        # if the opponent would win on the following turn,
        # this position is not a good move
        for next_position in next_positions:
            next_board = logic.drop_piece(opponent, next_position, new_board)
            winner = logic.check_win(next_board)
            if winner and winner[0] == opponent:
                oponent_will_win = True
                break

        if not oponent_will_win:
            good_moves.append(position)

    if not len(good_moves):
        return random.choice(positions)

    return random.choice(good_moves)


def generate_random_move(board):
    positions = logic.valid_moves(board)
    if not len(positions):
        return -1

    return random.choice(positions)


def better_than_random():
    ai_wins = 0
    random_wins = 0
    turn = 1
    games = 100
    tie = 0
    while ai_wins + random_wins < games:

        board = logic.copy_board(empty_board)
        while True:
            winner = logic.check_win(board)
            if winner:
                if winner[0] == 1:
                    ai_wins += 1
                else:
                    random_wins += 1
                break

            next_move = (
                generate_move(board, 1) if turn == 1 else generate_random_move(board)
            )
            if next_move == -1:
                tie += 1
                break
            board = logic.drop_piece(
                turn,
                next_move,
                board,
            )
            turn = 2 if turn == 1 else 1

    print(ai_wins, random_wins, tie, ai_wins / games)


tests = [better_than_random]


# if __name__ == "__main__":
#     for test in tests:
#         test()
