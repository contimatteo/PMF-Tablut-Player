import numpy as np

import fpm_tablut_player.configs as CONFIGS
from fpm_tablut_player.libraries.game_node import GameNode


###


class GameState:
    board: [[]]
    turn: str

    def __init__(self):
        self.turn = None
        self.board = []

    def createFromServerState(self, gameStateRaw):
        self.turn = str(gameStateRaw["turn"]).lower()
        board = gameStateRaw["board"]
        # TODO: missing code.
        # ...
        self.board = np.array(board)

    def createfromNode(self, initialGameState, node: GameNode):
        # TODO: missing code.
        # ...
        return self

    def getPossibleMoves(self, turn: str):
        # TODO: missing code.
        # ...
        return [{'from': (0, 0), 'to': (0, 0)}]

