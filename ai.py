import logic
import random
import copy
from concurrent.futures import ThreadPoolExecutor
import time

empty_board = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]


def threaded_example(board=empty_board):
    def count_columns(row):
        time.sleep(random.random())
        return len(row)

    with ThreadPoolExecutor(max_workers=4) as executor:
        lengths = list(
            executor.map(
                count_columns, [row + [0] * index for index, row in enumerate(board)]
            )
        )
        # => [7, 8, 9, 10, 11, 12]
        return lengths


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

    if random_wins:
        print(f"expected the ai to win every game but it lost {random_wins} times")


tests = [better_than_random]


if __name__ == "__main__":
    # threaded_example()
    for test in tests:
        test()
