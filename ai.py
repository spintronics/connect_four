import logic
import random
from util import cache_function


empty_board = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]


def ai(ai_player=1, max_depth=2):
    opponent = 1 if ai_player == 2 else 2

    def non_recursive(board, depth=0, recurse=False, strength=0):
        return not recurse

    @cache_function(lambda moves: moves[:], predicate=non_recursive)
    def _generate_moves(board, depth=0, recurse=False, strength=0):

        if depth > max_depth and recurse:
            return strength

        valid_next_moves = logic.valid_moves(board)

        if len(valid_next_moves) == 0:
            if recurse:
                return strength
            return []

        # collect each board state after valid ai moves
        next_board_states = [
            (position, logic.drop_piece(opponent, position, board))
            for position in valid_next_moves
        ]

        reasonable_moves = []

        for position, board in next_board_states:
            # check for next turn win
            if logic.check_win(board) == ai_player:
                if recurse:
                    strength += 1
                    continue

                return [position]

            # otherwise check all valid opponent moves
            valid_opponent_moves = logic.valid_moves(board)
            # gather boards
            opponent_boards = [
                logic.drop_piece(opponent, opponent_move, board)
                for opponent_move in valid_opponent_moves
            ]

            # if any are wins for opponent, skip this position
            if any(
                [
                    True
                    for board in opponent_boards
                    if logic.check_win(board) == opponent
                ]
            ):
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
        print(reasonable_moves)
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


def generate_random_move(board):
    positions = logic.valid_moves(board)
    if not len(positions):
        return -1

    return random.choice(positions)


generate_move = ai()


def better_than_random():
    ai_wins = 0
    random_wins = 0
    turn = 1
    games = 5
    tie = 0
    while ai_wins + random_wins < games:

        board = logic.copy_board(empty_board)
        while True:
            winner = logic.check_win(board)
            if winner:
                if winner == 1:
                    ai_wins += 1
                else:
                    random_wins += 1
                break

            next_move = (
                generate_move(board) if turn == 1 else generate_random_move(board)
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
