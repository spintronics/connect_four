# {
#     board: [[]],
#     turn: 1,
#     game_over: False
# }

def transpose(board):
    columns = [[] for _ in range(len(board[0]))]
    for row in board:
        for index, item in enumerate(row):
            columns[index].append(item)

    return columns

def flip(board):
    return [row[::-1] for row in board]


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


def check_win(board, move):
    """
    checks whether the last piece caused a move
    compile the list of horizonal/vertical/diagonal moves
    returns the winning player number or 0 if no winner
    """
    pass


def do_move(board, column, player):
    """
    update the board with the new piece dropped into the appropriate column
    """
    return board


def valid_move(board, move, player):
    """
    returns a boolean that indicates whether the given column is full
    or the move is outside the game board
    """
    return True


# def main():
#     while True:
#         move = input()
#         state = do_move(state)
#         check_win(move)
