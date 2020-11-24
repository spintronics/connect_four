import pygame, sys
from pygame.locals import *
from game import *
from components import *
import logic
from logic import valid_move
import util

# from server import ResponseCodes, Routes
import uuid
import copy
import ai


def asset_path(file):
    return path.join(util.current_directory, file)


class Assets:
    # did realize i mispelled peice at some point, but we've come too far
    # board = asset_path('assets\\connect_four_blank.png')
    new_game_button = asset_path("assets\\new_game_button.png")
    computer_button = asset_path("assets\\computer_button.png")
    two_player_button = asset_path("assets\\2_player_button.png")
    player_1_win = asset_path("assets\\1_winner.png")
    player_2_win = asset_path("assets\\2_winner.png")
    tie_game = asset_path("assets\\tie_game.png")


initial_state = {
    "window": {"width": 900, "height": 1000},
    # 'background_color': (166,117,161),
    "background_color": (225, 216, 159),
    "game": {
        "board_color": [0, 3, 123],
        "player_1_color": [113, 20, 17],
        "player_2_color": [255, 242, 0],
        "empty_color": [0, 0, 0],
        "player_turn": 1,
        "piece_spacing_ratio": (1, 2),
        "board_padding": 27,
        "board": [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ],
        "winner": 0,
        "active_column": 0,
        "remote": False,
        "user_id": uuid.uuid1(),
        "2_player_game": True,
        "game_started": False,
        "controls_state": 0,
        "controls_focused": False,
    },
}


class ControlState:
    new_game, select_mode = range(2)


def prop(value=None):
    def access(new):
        nonlocal value
        if new:
            value = new
        return value

    return access


class ActionNames:
    change_active_column = "change:active_column"
    drop_piece = "action:drop_piece"
    update_board = "change:board"
    joined_game = "action:joined_game"
    left_game = "action:left_game"
    focus_controls = "change:controls_focused"
    new_game = "change:game_started"
    set_game_mode = "change:2_player_game"


class ConnectFourActions:
    """
    these functions define how the state changes
    """

    @classmethod
    def change_active_column(Self, state, column):
        # returning none skips the redraw (nothing is changing)
        if (
            util.get("game.active_column", state) == column
            and util.get("game.controls_focused", state) == False
        ):
            return None

        # fine because assigning a literal
        util.path_set("game.active_column", column, state)
        util.path_set("game.controls_focused", False, state)
        return state

    @classmethod
    def drop_piece(Self, state, column):
        if not util.get("game.game_started", state):
            return state

        board = util.get("game.board", state)
        player = util.get("game.player_turn", state)
        if not logic.valid_move(column, board):
            return None
        util.path_set("game.board", logic.drop_piece(player, column, board), state)
        util.path_set("game.player_turn", 1 if player == 2 else 2, state)

        new_board = util.get("game.board", state)
        winner = logic.check_win(new_board)
        valid_moves = logic.valid_moves(new_board)
        if winner or not len(valid_moves):
            util.path_set("game.winner", winner[0] if winner else 3, state)
            util.path_set("game.game_started", False, state)

        if (
            not util.get("game.2_player_game", state)
            and util.get("game.player_turn", state) == 2
        ):
            move = ai.generate_move(new_board, 2)
            if move == -1:
                return None
            Self.drop_piece(state, move)

        return state

    @classmethod
    def focus_controls(Self, state, _):
        # if util.get("game.controls_focused", state):
        #     return None
        util.path_set("game.controls_focused", True, state)
        return state

    @classmethod
    def new_game(Self, state, _):
        util.path_set("game.board", util.get("game.board", initial_state), state)
        util.path_set("game.player_turn", 1, state)
        util.path_set("game.controls_state", 1, state)
        util.path_set("game.game_started", False, state)
        util.path_set("game.winner", 0, state)

        return state

    @classmethod
    def set_game_mode(self, state, two_player):
        util.path_set("game.2_player_game", two_player, state)
        util.path_set("game.controls_state", 0, state)
        util.path_set("game.game_started", True, state)
        return state


class ConnectFour(Game):
    def __init__(self, state, publisher):
        super().__init__(state, publisher)
        self.refs = {"piece_grid": prop()}

        self.piece_colors = [
            self.state.get("game.empty_color"),
            self.state.get("game.player_1_color"),
            self.state.get("game.player_2_color"),
        ]

        # self.async_pool = async_pool
        # self.remote_game = True

        state.register(
            ActionNames.change_active_column, ConnectFourActions.change_active_column
        )
        state.register(ActionNames.drop_piece, ConnectFourActions.drop_piece)
        state.register(ActionNames.focus_controls, ConnectFourActions.focus_controls)
        state.register(ActionNames.new_game, ConnectFourActions.new_game)
        state.register(ActionNames.set_game_mode, ConnectFourActions.set_game_mode)

        # if self.state.get('game.remote'):
        #     self.new_remote_game()

    # def new_remote_game(self):
    #     user_id = self.state.get('game.user_id')
    #     self.async_pool.request(Routes.new_game, {'user_id': user_id})

    def win_condition(self):
        return False

    def interactive_columns(self):
        board = self.state.get("game.board")
        dimensions = self.piece_dimensions()

        self.refs["columns"] = [prop() for row in board]

        return Row(
            gutter=dimensions["spacing"][0],
            children=[
                with_events(
                    Component(
                        # color=(0,0,index * 35)
                    ),
                    publisher=self.publisher,
                    on_hover=lambda e, c, column=index: self.state.dispatch(
                        ActionNames.change_active_column, column
                    ),
                    on_click=lambda e, c, column=index: self.state.dispatch(
                        ActionNames.drop_piece, column
                    ),
                )
                for index, row in enumerate(board[0])
            ],
        )

    def piece_dimensions(self):
        # memoize perhaps
        board = self.state.get("game.board")
        window = self.state.get("window")
        dimension = min(window.values())
        spacing = self.piece_spacing()
        padding = self.state.get("game.board_padding")

        vertical_piece_length = (dimension - padding * 2) / len(board[0]) - spacing[
            0
        ] * (len(board[0]) - 1)
        horizontal_piece_length = (dimension - padding * 2) / len(board) - spacing[
            0
        ] * (len(board) - 1)
        piece_diameter = min([vertical_piece_length, horizontal_piece_length])
        radius = piece_diameter / 2

        return {"radius": radius, "spacing": spacing, "width": dimension}

    def game_board(self):
        board = self.state.get("game.board")
        window = self.state.get("window")
        padding = self.state.get("game.board_padding")

        dimensions = self.piece_dimensions()

        rows = [
            list(
                map(
                    lambda cell: Circle(
                        radius=dimensions["radius"], color=self.piece_colors[cell]
                    ),
                    row,
                )
            )
            for row in board
        ]
        return [
            Rectangle(
                width=window["width"],
                height=window["width"],
                color=self.state.get("game.board_color"),
            ),
            Component(
                name="piece_grid",
                padding=padding,
                ref=self.refs["piece_grid"],
                children=[
                    self.interactive_columns(),
                    Column(
                        gutter=dimensions["spacing"][1],
                        children=[
                            Row(gutter=dimensions["spacing"][0], children=row)
                            for row in rows
                        ],
                    ),
                ],
            ),
        ]

    def piece_spacing(self):
        x, y = self.state.get("game.piece_spacing_ratio")
        board = self.state.get("game.board")

        scaled_x = self.state.get("window.width") * 0.1 / len(board)

        return (scaled_x, y * scaled_x / x)

    def next_piece(self):
        active_column = self.state.get("game.active_column")
        board = self.state.get("game.board")
        dimensions = self.piece_dimensions()
        padding = self.state.get("game.board_padding")
        children = [False] * len(board[0])
        current_player = self.state.get("game.player_turn")
        computer_game = self.state.get("game.2_player_game") == False

        if current_player == 2 and computer_game:
            return

        children[active_column] = Circle(
            radius=dimensions["radius"],
            color=self.piece_colors[current_player],
            name="next_piece",
        )

        # only show piece when appropriate (game is running, controls not hovered)
        if self.state.get("game.controls_focused"):
            return None
        if not self.state.get("game.game_started"):
            return None

        return Component(
            padding=padding,
            children=[
                Row(
                    name="next_piece_row",
                    padding=padding,
                    gutter=dimensions["spacing"][0],
                    children=children,
                )
            ],
        )

    def game_controls(self):
        # if not self.state.get("game.controls_focused"):
        #     return None
        controls_state = self.state.get("game.controls_state")

        buttons = [
            [
                with_events(
                    Image(Assets.new_game_button, centered=True),
                    publisher=self.publisher,
                    on_click=lambda x, c: self.state.dispatch(
                        ActionNames.new_game, None
                    ),
                )
            ],
            [
                with_events(
                    Image(Assets.two_player_button, centered=True),
                    publisher=self.publisher,
                    on_click=lambda x, c: self.state.dispatch(
                        ActionNames.set_game_mode, True
                    ),
                ),
                with_events(
                    Image(Assets.computer_button, centered=True),
                    publisher=self.publisher,
                    on_click=lambda x, c: self.state.dispatch(
                        ActionNames.set_game_mode, False
                    ),
                ),
            ],
        ][controls_state]
        return with_events(
            Row(children=[Component(children=[button]) for button in buttons]),
            publisher=self.publisher,
            on_hover=lambda e, c: self.state.dispatch(ActionNames.focus_controls, None),
        )

    def draw(self):
        # remove events to prevent duplicates
        self.publisher.purge([pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP])
        window = self.state.get("window")

        winner = self.state.get("game.winner")

        winner_message = [
            None,
            Image(Assets.player_1_win, centered=True),
            Image(Assets.player_2_win, centered=True),
            Image(Assets.tie_game, centered=True),
        ]

        component_tree = (
            ContextProvider(
                context={"screen": self.screen, "position": [0, 0]},
                width=window["width"],
                height=window["height"],
                children=[
                    Expanded(
                        direction="down",
                        children=[
                            Rectangle(
                                name="controls",
                                expanded=True,
                                color=self.state.get("background_color"),
                                children=[
                                    self.game_controls(),
                                    winner_message[winner],
                                    self.next_piece(),
                                ],
                            ),
                            Component(
                                width=window["width"],
                                height=874,
                                children=self.game_board(),
                            ),
                        ],
                    )
                ],
            )
            .resize_children()
            .draw()
        )

        pygame.display.flip()

        # only update when a property changes
        self.updated = True


class ExternalActions:
    """
    define how server data changes the game state in these actions
    """

    @classmethod
    def update_board(Self, state, board):
        # server is always right, copy the data because it is a non-primitive
        if not board:
            return None
        copy = [row.copy() for row in board]
        state["game"]["board"] = copy
        return state

    @classmethod
    def joined_game(Self, state, game_id):
        if not game_id:
            return None
        state["game"]["id"] = game_id
        return state

    @classmethod
    def left_game(Self, state, _):
        state["game"]["id"] = -1
        return state


publisher = Publisher()

# register external external actions and create the state
# actions = [
#     Action(ActionNames.update_board, ExternalActions.update_board),
#     Action(ActionNames.joined_game, ExternalActions.joined_game),
#     Action(ActionNames.left_game, ExternalActions.left_game),
# ]
# async_pool = util.AsyncRequestPool()

state = State(copy.deepcopy(initial_state), publisher)
game = ConnectFour(state, publisher)
state.replay_actions()

# async_pool.request(Routes.new_game, {'user_id': ConnectFourActions.user_id})

# ConnectFourActions.async_pool = async_pool

game.draw()

# dispatch external actions when responses are received
# def handle_responses(responses):
#     # handle errors
#     for response in responses:
#         if response['url'] == Routes.new_game:
#             state.dispatch(ActionNames.joined_game, util.get('data.game_id', response))
#         if response['url'] == Routes.join_game:
#             state.dispatch(ActionNames.joined_game, util.get('data.game_id', response))
#         if response['url'] == Routes.check:
#             state.dispatch(ActionNames.update_board, util.get('data', response))


try:
    while game.running:
        # handle_responses(async_pool.drain())
        game.consume_events()
        pygame.time.wait(20)
except:
    print("something broke")
