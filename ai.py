import logic
import random
import copy

empty_board = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]


def generate_move(board):
    columns = len(board[0])
    move = False
    while True:
        move = random.randint(0, columns - 1)
        if logic.valid_move(2, move, board):
            break

    return move


def generate_random_move(board):
    columns = len(board[0])
    move = False
    while True:
        move = random.randint(0, columns - 1)
        if logic.valid_move(2, move, board):
            break

    return move


def better_than_random():
    ai_wins = 0
    random_wins = 0
    turn = 1
    while ai_wins + random_wins < 100:
        board = copy.deepcopy(empty_board)
        while True:
            winner = logic.check_win(board)
            if winner:
                if winner == 1:
                    ai_wins += 1
                else:
                    random_wins += 1
                break
            board = logic.drop_piece(
                turn,
                generate_move(board) if turn == 1 else generate_random_move(board),
                board,
            )
            turn = 2 if turn == 1 else 1


tests = [better_than_random]

if __name__ == "__main__":
    for test in tests:
        test()
