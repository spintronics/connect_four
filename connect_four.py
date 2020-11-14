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
        'height': 980
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
        'winner': 0,
        'active_column': 0
    }
}

def prop(value = None):
    def access(new):
        if new: value = new
        return value
    return access


class ConnectFour(Game):
    def __init__(self, state):
        super().__init__(state)
        self.refs = {
            'piece_grid': prop()
        }

        self.publisher = Publisher()

        self.events = Events(self.publisher)

        self.piece_paths = [Assets.black_peice, Assets.red_peice, Assets.yellow_peice]

    def win_condition(self):
        return False

    def interactive_columns(self):
        board = self.state.get('game.board')

        self.refs['columns'] = [prop() for row in board]

        return Row(
            gutter=35,
            children=[
                with_events(
                    Component(
                        ref=self.refs['columns'][index]
                    ),
                    event_stream = self.events,
                    name = f'column {index}',
                    on_hover = lambda e, c: print(f'{c.name} hover!')
                ) for index, row in enumerate(board)
            ]
        )


    def game_board(self):
        board = self.state.get('game.board')
        rows = [
            list(map(
                lambda cell: Image(self.piece_paths[cell]) if self.piece_paths[cell] else None,
                row
            )) for row in board
        ]
        return [
            Image(Assets.board, name="board"),
            Component(
                name="piece_grid",
                padding=27,
                ref = self.refs['piece_grid'],
                children=[
                    self.interactive_columns(),
                    Column(
                        gutter = 16,
                        children = list(map(lambda row: Row(gutter=35, children=row), rows))
                    )
                ]
            )

        ]
        
    def next_piece(self):
        active_column = self.state.get('game.active_column')
        board = self.state.get('game.board')
        children = [False] * len(board)
        children[active_column] = Image(
            self.piece_paths[1],
            name="next_piece",
            height=123
        )
        return Component(
            padding=27,
            children=[
                Row(
                    name="next_piece_row",
                    padding=27,
                    gutter=35,
                    children=children
                )
            ]
        )

    def draw(self):
        #remove events to prevent duplicates
        self.publisher.purge()
        window = self.state.get('window')

        component_tree = ContextProvider(
            context = {'screen': self.screen, 'position': [0,0]},
            width=window['width'],
            height=window['height'],

            children = [
                Expanded(
                    direction='down',
                    children=[
                        Rectangle(
                            name="controls",
                            expanded = True,
                            color=(255,255,255),
                            children=[
                                self.next_piece()
                            ]
                        ),
                        Component(
                            width=window['width'],
                            height=874,
                            children=self.game_board()
                        ),
                    ]
                )
                
            ]
        ).resize_children().draw()

        
        pygame.display.flip()


        #only update when a property changes
        self.updated = True

    



state = State(initial_state)
game = ConnectFour(state)
game.draw()

while game.running:
    game.update()
    game.events.process()
    pygame.time.wait(200)
