import pygame, sys
from pygame.locals import *
from os import path
from game import *
from components import *

current_directory = path.abspath(path.dirname(__file__))

def asset_path(file): return path.join(current_directory, file)

class Assets:
    #did realize i mispelled peice at some point, but we've come too far
    # board = asset_path('assets\\connect_four_blank.png')
    board = asset_path('assets\\connect_four_blank_filled.png')
    red_peice = asset_path('assets\\red_peice.png')
    yellow_peice = asset_path('assets\\yellow_peice.png')
    black_peice = asset_path('assets\\black_peice.png')



initial_state = {
    'window': {
        'width': 1166,
        'height': 1000
    },
    'background_color': (255,255,255),
    'game': {
        'player_turn': 1,
        'board': [
            [0,0,0,0,0,0,0],
            [2,0,2,0,2,0,2],
            [1,0,1,0,1,2,1],
            [2,1,2,1,2,1,2],
            [1,2,1,2,1,2,1],
            [2,1,2,1,2,1,2],
        ],
        'winner': 0
    }
}

class Prop:
    def __init__(self, name = '', value = None):
        self._name = name
        self._value = value
    def get(self):
        return self._value
    def set(self, value):
        self._value = value


class ConnectFour(Game):
    def __init__(self, state):
        super().__init__(state)
        self.piece_grid = Prop()


    def win_condition(self):
        return False

        
    def draw(self):
        board = self.state.get('game.board')

        peice = [Assets.black_peice, Assets.red_peice, Assets.yellow_peice]

        rows = [
            list(map(
                lambda cell: Image(peice[cell]) if peice[cell] else None,
                row
            )) for row in board
        ]

        

        # the resize/draw stuff should be delegated to the base game class

        component_tree = ContextProvider(
            context = {'screen': self.screen, 'position': [0,0]},
            width=1166,
            height=874,

            children = [
                Image(Assets.board, name="board"),
                Component(
                    name="piece_grid",
                    padding=27,
                    ref = self.piece_grid,
                    children=[
                        Column(
                            gutter=16,
                            children = list(map(lambda row: Row(gutter=35, children=row), rows))
                        )
                    ]
                )
            ]
        ).resize_children().draw()

        
        pygame.display.flip()



state = State(initial_state)
game = ConnectFour(state)
game.draw()


input()