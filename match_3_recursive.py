from functools import wraps
import random
import copy
from sys import getsizeof


def true_predicate(*args, **kwargs):
    return True


def cache_function(copy=lambda x: x, predicate=true_predicate, maxsize=2000000):
    """
    must be pure function with serializable arguments.
    predicate should be used to skip caching, it is passed the same args as the fn
    maxsize in bytes
    copy the result from the cache if it is an object that you dont want to mutate
    default maxsize is 2mb, i dont see a way to forget older entries without sacrificing speed
    """
    cache = {}
    maxed = False

    def cacher(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not predicate(*args, **kwargs):
                return fn(*args, **kwargs)

            signature = str([args, kwargs])
            nonlocal maxed

            if signature in cache:
                return cache[signature]

            result = fn(*args, **kwargs)

            if not maxed:
                cache[signature] = result
                maxed = getsizeof(cache) >= maxsize

            return copy(result)

        return wrapper

    return cacher


def copy_board(board):
    result = []
    for row in board:
        result.append(row[:])

    return result


def transpose(board):
    columns = [[] for _ in range(len(board[0]))]
    for row in board:
        for index, item in enumerate(row):
            columns[index].append(item)

    return columns


def flip(board):
    return [row[::-1] for row in board]


def unnest(list):
    result = []
    for x in list:
        for y in x:
            result.append(y)

    return result


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


@cache_function()
def check_win(board, player, n=3):

    for row in board + transpose(board) + diagonals(board) + diagonals(flip(board)):
        if connect_n(row, player, n):
            return True
    return False


@cache_function(lambda moves: moves[:])
def valid_moves(board):
    moves = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[x][y] == 0:
                moves.append([x, y])
    return moves


def place_piece(board, position, player):
    board = copy_board(board)
    board[position[0]][position[1]] = player
    return board


def random_move(board):
    valid = valid_moves(board)
    if not len(valid):
        return -1
    return random.choice(valid) if len(valid) else []


def ai(ai_player=1, max_depth=10):
    opponent = 1 if ai_player == 2 else 2

    def non_recursive(board, depth=0, recurse=False, strength=0):
        return not recurse

    @cache_function(lambda moves: copy_board(moves), predicate=non_recursive)
    def _generate_moves(board, depth=0, recurse=False, strength=0):

        if depth > max_depth and recurse:
            return strength

        valid_next_moves = valid_moves(board)

        if len(valid_next_moves) == 0:
            if recurse:
                return strength
            return []

        # collect each board state after valid ai moves
        next_board_states = [
            (position, place_piece(board, position, player))
            for position in valid_next_moves
        ]

        reasonable_moves = []

        for position, board in next_board_states:
            # check for next turn win
            if check_win(board, ai_player):
                if recurse:
                    strength += 1
                    continue

                return [position]

            # otherwise check all valid opponent moves
            valid_opponent_moves = valid_moves(board)
            # gather boards
            opponent_boards = [
                place_piece(board, opponent_move, opponent)
                for opponent_move in valid_opponent_moves
            ]

            # if any are wins for opponent, skip this position
            if any([True for board in opponent_boards if check_win(board, opponent)]):
                if recurse:
                    strength -= 1
                continue

            next_moves_strengths = [
                _generate_moves(board, depth + 1, True, strength)
                for board in opponent_boards
            ]

            if recurse:
                return sum(next_moves_strengths)

            reasonable_moves.append((position, sum(next_moves_strengths)))

        if recurse:
            return strength

        # return list of reasonable moves, sorted by strength
        return [
            move[0]
            for move in sorted(reasonable_moves, key=lambda pair: pair[1], reverse=True)
        ]

    def generate_move(board):
        moves = _generate_moves(board)

        if not len(moves):
            return -1

        return moves[0]

    return generate_move


blank_board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

player = 1

generate_move = ai()

wins = [0, 0, 0]

game_count = 1000

while sum(wins) < game_count:
    ai_player = 1
    board = copy_board(blank_board)
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

print(wins, wins[0] / game_count)
