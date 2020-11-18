from flask import Flask, request
from functools import wraps
import sys
import logic
import random
import socketserver

app = Flask(__name__)

initial_state = dict(
    id=0,
    board=[[0, 0, 0, 0, 0, 0, 0] for _ in range(6)],
    turn=1,
    winner=0,
    player_1_id=0,
    player_2_id=0,
)


class GameProps:
    player_1_id = "player_1_id"
    player_2_id = "player_2_id"
    board = "board"
    turn = "turn"


class Game:
    def __init__(self, state):
        self.state = state


class ResponseCodes:
    nice_try = "Its not your turn"
    already_exists = "Game already exists"
    success = "Great Success"
    error = "you broke it"
    malformed = "check your body"
    no_such_game = "you just made that up"
    game_full = "make a new game"
    invalid_move = "maybe your hand slipped"
    no_change = "looks the same to me"
    change = "is good for the soul"
    unexpected = "that wasnt supposed to happen"


class Params:
    user_id = "user_id"
    game_id = "game_id"
    column_id = "column_id"
    board = "board"


class Routes:
    new_game = "/new_game"
    join_game = "/join_game"
    move = "/move"
    leave = "/leave"
    check = "/check"


def required_params(*keys):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # try:
            body = request.json
            if not body:
                return {"code": ResponseCodes.malformed, "data": f"expected a body"}
            for key in keys:
                if not (key in body):
                    return {"code": ResponseCodes.malformed, "data": f"expected {key}"}
            return f(body, *args, **kwargs)

        # except Exception as e:
        #     exc_type, exc_obj, exc_tb = sys.exc_info()
        #     return {
        #         'code': ResponseCodes.error,
        #         'data': str(exc_tb.tb_lineno) + ': ' + str(e)
        #     }
        return decorated_function

    return decorator


games: [Game] = {}


@app.route("/new_game", methods=["POST"])
@required_params(Params.user_id)
def new_game(body):
    game_id = 0
    while game_id in games:
        game_id = random.randint(0, 900000)

    state = {**initial_state, "player_1_id": body[Params.user_id]}
    games[game_id] = Game(state)
    return {"code": ResponseCodes.success, "data": {"game_id": game_id}}


@app.route("/join_game", methods=["POST"])
@required_params(Params.game_id, Params.user_id)
def join(body):
    if not (body[Params.game_id] in games):
        return {"code": ResponseCodes.no_such_game}

    game = games[body[Params.game_id]]

    if game.state[GameProps.player_2_id]:
        return {"code": ResponseCodes.game_full}

    game.state[GameProps.player_2_id] = body[Params.user_id]

    return {"code": ResponseCodes.success, "data": {"game_id": body[Params.game_id]}}


@app.route("/move", methods=["POST"])
@required_params(Params.game_id, Params.user_id, Params.column_id)
def move(body):
    if not (body[Params.game_id] in games):
        return {"code": ResponseCodes.no_such_game}

    game = games[body[Params.game_id]]
    player = 1 if game.state[GameProps.player_1_id] == body[Params.user_id] else 2
    column = body[Params.column_id]
    board = game.state[GameProps.board]
    turn = game.state[GameProps.turn]

    if turn != player:
        return {"code": ResponseCodes.nice_try}

    if not logic.valid_move(player, column, board):
        return {"code": ResponseCodes.invalid_move}

    game.state[GameProps.board] = logic.drop_piece(player, column, board)

    game.state[GameProps.turn] = 1 if turn == 2 else 2

    return {"code": ResponseCodes.success}


# end game
@app.route("/leave", methods=["POST"])
@required_params(Params.game_id, Params.user_id)
def leave(body):
    if not (body[Params.game_id] in games):
        return {"code": ResponseCodes.no_such_game}
    del games[body[Params.game_id]]
    return {"code": ResponseCodes.success}


# check board (see if server has a more recent board after opponent moves)
@app.route("/check", methods=["POST"])
@required_params(Params.game_id, Params.board)
def check(body):
    if not (body[Params.game_id] in games):
        return {"code": ResponseCodes.no_such_game}
    game = games[body[Params.game_id]]
    board = game.state[GameProps.board]
    if str(body[Params.board]) == str(board):
        return {"code": ResponseCodes.no_change}

    return {"code": ResponseCodes.change, "data": board}
