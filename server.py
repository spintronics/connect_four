from flask import Flask, request
from functools import wraps
import sys
import logic
import random
app = Flask(__name__)

initial_state = dict(
    id = 0,
    board = [[0,0,0,0,0,0,0] for _ in range(6)],
    turn = 1,
    winner = 0,
    player_1_id = 0,
    player_2_id = 0
)

class GameProps:
    player_1_id = 'player_1_id',
    player_2_id = 'player_2_id',


class Game:
    def __init__(self, state):
        self.state = state

class ResponseCodes:
    nice_try = 'Its not your turn'
    already_exists = 'Game already exists'
    success = 'Great Success'
    error = 'you broke it'
    malformed = 'check your body'
    no_such_game = 'you just made that up'
    game_full = 'make a new game'

class Params:
    user_id = "user_id"
    game_id = "game_id"
    column_id = "column_id"


def required_params(*keys):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                body = request.get_json()
                if not body:
                    return {
                        'code': ResponseCodes.malformed,
                        'data': f'expected a body'
                    }
                for key in keys:
                    if not (key in body):
                        return {
                            'code': ResponseCodes.malformed,
                            'data': f'expected {key}'
                        }
                return f(body, *args, **kwargs)
            except:
                e_type, e_obj, e_tb = sys.exc_info()
                print(e_obj, e_tb.tb_lineno)
                return {
                    'code': ResponseCodes.error,
                    'data': ''
                }
        return decorated_function

    return decorator
                        
    

    
games: [Game] = {}

@app.route('/new_game', methods=['POST'])
@required_params(Params.user_id)
def new_game(body):
    game_id = 0
    while game_id in games:
        game_id = random.randint(0, 900000)

    if game_id in games: return {
        'code': ResponseCodes.already_exists
    }
    state = {
        **initial_state,
        'player_1_id': body[Params.user_id]
    }
    games[game_id] = Game(**state)
    return {
        'code': ResponseCodes.success,
        'data': {
            'game_id': game_id
        }
    }

@app.route('/join_game')
@required_params(Params.game_id, Params.user_id)
def move(body):
    if not (body[Params.game_id] in games):
        return {
            'code': ResponseCodes.no_such_game
        }

    game = body[Params.game_id]
    
    if game.state[GameProps.player_2_id]:
        return {
            'code': ResponseCodes.game_full
        }

    game.state[GameProps.player_2_id] = body[Params.user_id]

    return ResponseCodes.success


    

    
