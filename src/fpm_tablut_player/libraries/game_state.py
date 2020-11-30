import numpy as np

from fpm_tablut_player.libraries.game_node import GameNode
from fpm_tablut_player.utils import GameUtils


###


class GameState:
    board: [[]]
    turn: str

    def __init__(self):
        self.turn = None
        self.board = []

    def createFromServerState(self, stateFromServer):
        self.turn = GameUtils.turnToString(stateFromServer["turn"])
        board = stateFromServer["board"]
        #
        # TODO: [@primiano] missing code.
        # ...
        #
        self.board = np.array(board)
        #
        return self

    def createfromGameNode(self, initialGameState, node: GameNode):
        #
        # TODO: [@primiano] missing code.
        # ...
        #
        return self

    def getPossibleMoves(self, turn: str) -> list:
        #
        # TODO: [@primiano] missing code.
        # ...
        #
        return [
            {'from': (0, 3), 'to': (1, 3)},
            {'from': (3, 0), 'to': (3, 1)},
            {'from': (3, 8), 'to': (3, 7)},
            {'from': (8, 3), 'to': (7, 3)}
        ]
