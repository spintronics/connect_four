from functools import partial
import copy
from io import TextIOWrapper
from sys import getsizeof
import json


empty_board = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]


def transpose(board):
    columns = [[] for _ in range(len(board[0]))]
    for row in board:
        for index, item in enumerate(row):
            columns[index].append(item)

    return columns


def flip(board):
    return [row[::-1] for row in board]


def drop_piece_optimized(player, column, adjusted_board):
    new_board = copy.deepcopy(adjusted_board)
    for dex, cell in enumerate(new_board[column]):
        if cell == 0:
            new_board[column][dex] = player
            break
    return new_board


def valid_move(column, board):
    """
    returns a boolean that indicates whether the given column is full
    or the move is outside the game board

    """
    return 0 in board[column]


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


def diagonals_test():
    # board = [[] for _ in range(6)]
    # for x in range(42):
    #     board[x // 7].append(x)

    board = [
        [0, 1, 2, 3, 4, 5, 6],
        [7, 8, 9, 10, 11, 12, 13],
        [14, 15, 16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25, 26, 27],
        [28, 29, 30, 31, 32, 33, 34],
        [35, 36, 37, 38, 39, 40, 41],
    ]
    print(board)

    ltr = [
        [0],
        [7, 1],
        [14, 8, 2],
        [21, 15, 9, 3],
        [28, 22, 16, 10, 4],
        [35, 29, 23, 17, 11, 5],
        [36, 30, 24, 18, 12, 6],
        [37, 31, 25, 19, 13],
        [38, 32, 26, 20],
        [39, 33, 27],
        [40, 34],
        [41],
    ]

    rtl = [
        [6],
        [13, 5],
        [20, 12, 4],
        [27, 19, 11, 3],
        [34, 26, 18, 10, 2],
        [41, 33, 25, 17, 9, 1],
        [40, 32, 24, 16, 8, 0],
        [39, 31, 23, 15, 7],
        [38, 30, 22, 14],
        [37, 29, 21],
        [36, 28],
        [35],
    ]

    diag_1 = diagonals(board)
    diag_2 = diagonals(flip(board))

    return str(ltr) == str(diag_1) and str(rtl) == str(diag_2)


def connect_four(row):
    str_row = "".join(list(map(str, row)))
    if "1111" in str_row:
        return 1
    elif "2222" in str_row:
        return 2
    return 0


def check_win(board):
    rows = board + transpose(board) + diagonals(board) + diagonals(flip(board))
    for row in rows:
        winner = connect_four(row)
        if winner:
            return winner
    return 0


def permutations(board, player, file: TextIOWrapper):
    # list of valid next moves
    valid_next_moves = [
        column for column in range(len(board)) if valid_move(column, board)
    ]
    if len(valid_next_moves) == 0:
        return

    next_board_states = [
        drop_piece_optimized(player, column, board) for column in valid_next_moves
    ]
    for next_board in next_board_states:

        # if the move results in a win, write it to a file
        if check_win(next_board):
            file.write(json.dumps(next_board) + ",\n")
        else:
            # otherwise check deeper
            permutations(next_board, 1 if player == 2 else 2, file)


def drop_piece(player, column, board):
    columns = transpose(board)
    flipped = flip(columns)

    for dex, cell in enumerate(flipped[column]):
        if cell == 0:
            flipped[column][dex] = player
            break
    return transpose(flip(flipped))


def pipe(*fns):
    def inner(value):
        for f in fns:
            value = f(value)
        return value

    return inner


def test_drop_piece():
    start, end = [
        [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2],
            [0, 2, 1, 2, 1, 0, 1],
        ],
    ]
    result = pipe(
        partial(drop_piece, 1, 2),
        partial(drop_piece, 2, 1),
        partial(drop_piece, 2, 3),
        partial(drop_piece, 1, 4),
        partial(drop_piece, 1, 6),
        partial(drop_piece, 2, 6),
    )(start)
    if str(result) != str(end):
        print(f"expected {end} to equal {result}")
        return False
    return True


# with open('winning_permutations.pickle', 'a') as file:
#   permutations(transpose(empty_board), 1, file)

tests = [test_drop_piece, diagonals_test]

if __name__ == "__main__":
    fails = 0
    for test in tests:
        if not test():
            fails += 1
    if fails:
        print(f"{fails} out of {len(tests)} failed")
    else:
        print("all tests passed")
