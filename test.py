from util import AsyncRequestPool, get
from server import Routes
import time
                




requestPool = AsyncRequestPool()

def with_game(response):
    game_id = get('data.game_id', response)
    requestPool.request(Routes.join_game, {'user_id': 5, 'game_id': game_id}, print)
    requestPool.request(Routes.move, {'user_id': 2, 'game_id': game_id, 'column_id': 0}, print)
    requestPool.request(Routes.move, {'user_id': 5, 'game_id': game_id, 'column_id': 0}, print)
    requestPool.request(Routes.move, {'user_id': 2, 'game_id': game_id, 'column_id': 0}, print)
    requestPool.request(
        Routes.check, {'game_id': game_id, 'board': [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            ],
        }, print
    )
    requestPool.request(
        Routes.check, {'game_id': game_id, 'board':
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [2, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0],
            ],
        }, print
    )

requestPool.request(
    Routes.new_game, {'user_id': 2}, with_game
)

while True:
    requestPool.drain()
    time.sleep(1)



