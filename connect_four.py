import pygame, sys
from pygame.locals import *
from os import path
from game import *
from components import *
import logic

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
        'width': 900,
        'height': 1000
    },
    'background_color': (255,255,255),
    'game': {
        'board_color': [0,3,128],
        'player_1_color': [113,20,17],
        'player_2_color': [255,242,0],
        'empty_color': [0,0,0],
        'player_turn': 1,
        'piece_spacing_ratio': (1,2),
        'board_padding': 27,
        'board': [
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
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


class ActionNames:
    change_active_column = 'change:active_column'
    drop_piece = 'action:drop_piece'

class ConnectFourActions:
    @classmethod
    def change_active_column(Self, state, column):
        #fine because assigning a literal
        state['game']['active_column'] = column.id
        return state

    @classmethod
    def drop_piece(Self, state, column):
        board = state['game']['board']
        player = state['game']['player_turn']
        if not logic.valid_move(board, column.id, player): return None
        state['game']['board'] = logic.drop_piece(player, column.id, board)
        state['game']['player_turn'] = 1 if player == 2 else 2

        return state


class ConnectFour(Game):
    def __init__(self, state, publisher):
        super().__init__(state, publisher)
        self.refs = {
            'piece_grid': prop()
        }

        self.piece_colors = [self.state.get('game.empty_color'), self.state.get(
            'game.player_1_color'), self.state.get('game.player_2_color')]


        state.register(
            ActionNames.change_active_column,
            ConnectFourActions.change_active_column
        )
        state.register(
            ActionNames.drop_piece,
            ConnectFourActions.drop_piece
        )


    def win_condition(self):
        return False

    def interactive_columns(self):
        board = self.state.get('game.board')
        dimensions = self.piece_dimensions()

        self.refs['columns'] = [prop() for row in board]

        return Row(
            gutter=dimensions['spacing'][0],
            children=[
                with_events(
                    Component(
                        # color=(0,0,index * 35)
                    ),
                    publisher = self.publisher,
                    id = index,
                    on_hover = lambda e, c: self.state.dispatch(ActionNames.change_active_column, c),
                    on_click = lambda e, c: self.state.dispatch(ActionNames.drop_piece, c)
                ) for index, row in enumerate(board[0])
            ]
        )

    def piece_dimensions(self):
        # memoize perhaps
        board = self.state.get('game.board')
        window = self.state.get('window')
        dimension = min(window.values())
        spacing = self.piece_spacing()
        padding = self.state.get('game.board_padding')

        vertical_piece_length = (dimension - padding * 2) / len(board[0]) - spacing[0] * (len(board[0]) - 1)
        horizontal_piece_length = (dimension - padding * 2) / len(board) - spacing[0] * (len(board) - 1)
        piece_diameter = min([vertical_piece_length, horizontal_piece_length])
        radius = piece_diameter / 2

        return {
            'radius': radius,
            'spacing': spacing,
            'width': dimension
        }


    def game_board(self):
        board = self.state.get('game.board')
        window = self.state.get('window')
        padding = self.state.get('game.board_padding')

        dimensions = self.piece_dimensions()

        rows = [
            list(map(
                lambda cell: Circle(radius=dimensions['radius'], color=self.piece_colors[cell]),
                row
            )) for row in board
        ]
        return [
            Rectangle(
                width=window['width'],
                height=window['width'],
                color=self.state.get('game.board_color')
            ),
            Component(
                name="piece_grid",
                padding=padding,
                ref = self.refs['piece_grid'],
                children=[
                    self.interactive_columns(),
                    Column(
                        gutter = dimensions['spacing'][1],
                        children=[Row(gutter=dimensions['spacing'][0], children=row) for row in rows]
                    )
                ]
            )

        ]

    def piece_spacing(self):
        x,y = self.state.get('game.piece_spacing_ratio')
        board = self.state.get('game.board')

        scaled_x = self.state.get('window.width') * .1 / len(board)

        return (scaled_x, y * scaled_x / x)


        
    def next_piece(self):
        active_column = self.state.get('game.active_column')
        board = self.state.get('game.board')
        dimensions = self.piece_dimensions()
        padding = self.state.get('game.board_padding')
        children = [False] * len(board[0])
        current_player = self.state.get('game.player_turn')

        children[active_column] = Circle(
            radius=dimensions['radius'],
            color=self.piece_colors[current_player],
            name="next_piece"
        )
        return Component(
            padding=padding,
            children=[
                Row(
                    name="next_piece_row",
                    padding=padding,
                    gutter=dimensions['spacing'][0],
                    children=children
                )
            ]
        )

    def draw(self):
        #remove events to prevent duplicates
        self.publisher.purge([
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONUP
        ])
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

    


publisher = Publisher()
state = State(initial_state, publisher)
game = ConnectFour(state, publisher)
game.draw()

while game.running:
    # game.update()
    game.consume_events()
    pygame.time.wait(20)
