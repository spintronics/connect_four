from functools import partial


def transpose(board):
    columns = [[] for _ in range(len(board[0]))]
    for row in board:
        for index, item in enumerate(row):
            columns[index].append(item)

    return columns


def flip(board):
    return [row[::-1] for row in board]


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


def horizontals(board, move):
    """
    return the 4 cells (3 to the left 3 to the right)
    return two lists
    move = [4, 6]
    [0,0,1,1,1,0,2,0]
    [
      [0,0,1,1]
      [1,1,0,2]
    ]
    """
    pass


# horizontals_test = [
#     [
#         [
#             [0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0],
#         ],
#         [0, 7],
#         [
#             [1, 2, 3],
#             [0, 1, 0]
#         ],
#     ]
# ]
# for test in horizontals_test:
#     result = horizontals(test[0], test[1])
#     if result != test[2]:
#         print(f'expected {result} to equal {test[2]}')


def verticals(board, move):
    """
    return the 4 cells (3 above 3 below)
    return two lists
    """
    pass


def diagonals(board, move):
    pass


def connect_four(possibility):
    """
    length is four and all the same pieces?

    """

    pass


def check_win(board):
    """
    checks whether the last piece caused a move
    compile the list of horizonal/vertical/diagonal moves
    returns the winning player number or 0 if no winner
    """
    return False


def valid_move(player, column, board):
    """
    returns a boolean that indicates whether the given column is full
    or the move is outside the game board

    """
    return True


tests = [test_drop_piece]

if __name__ == "__main__":
    fails = 0
    for test in tests:
        if not test():
            fails += 1
    if fails:
        print(f"{fails} out of {len(tests)} failed")
    else:
        print("all tests passed")
