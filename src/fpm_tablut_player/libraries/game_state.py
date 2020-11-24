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
        board, turn = gameStateRaw
        self.board = np.array(board)
        self.turn = turn

    def createfromNode(self, initialGameState, node: GameNode):
        # ...
        # missing code
        # ...
        return self

    def getPossibleMoves(self, turn: str):
        # missing ...
        return [{'from': (0, 0), 'to': (0, 0)}]

    def generateSearchTree(self):
        K = CONFIGS.K
        # ...
        # missing code
        # ...
        return self.board
