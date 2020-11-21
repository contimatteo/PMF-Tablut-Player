import fpm_tablut_player.configs as CONFIGS


###


class GameState:
    board: any
    turn: str

    def __init__(self, initialGameState: dict):
        self.__load(initialGameState)

    def __load(self, gameStateRaw):
        board, turn = gameStateRaw
        self.board = board
        self.turn = turn

    def generateSearchTree(self):
        K = CONFIGS.K
        # ...
        # missing code
        # ...
        return self.board
