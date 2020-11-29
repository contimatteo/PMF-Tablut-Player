import fpm_tablut_player.configs as CONFIGS

from fpm_tablut_player.libraries.game_state import GameState

###

ROW_NAMES: list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
COL_NAMES: list = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
ROWS_SIZE: int = len(ROW_NAMES)
COLS_SIZE: int = len(COL_NAMES)

###


class GameMove:
    fromCell: str
    toCell: str
    turn: str

    def __init__(self):
        self.fromCell = None
        self.toCell = None
        self.turn = str(CONFIGS.APP_ROLE).lower()

    def __convertCellToServerFormat(self, x: int, y: int) -> str:
        if x < 0 or x > (ROWS_SIZE - 1):
            raise Exception("Wrong X cell (index) selected.")

        if y < 0 or y > (COLS_SIZE - 1):
            raise Exception("Wrong Y cell (index) selected.")

        return "{}{}".format(str(ROW_NAMES[x]), str(COL_NAMES[y]))

    def __getMoveForReachingState(self, start: GameState, end: GameState) -> (tuple, tuple):
        #
        # TODO: [@contimatteo] missing code.
        # ...
        # gameMove = start.getMoveForReaching(stateToReach: GameState) (board = .state)
        #
        fromCell = (3, 1)  # "d1"
        toCell = (3, 2)  # "d2"
        #
        return (fromCell, toCell)

    ###

    def fromStartToEnd(self, start: GameState, end: GameState):
        (fromCell, toCell) = self.__getMoveForReachingState(start, end)

        # (int,int) --> str
        self.fromCell = self.__convertCellToServerFormat(fromCell[0], fromCell[1])
        self.toCell = self.__convertCellToServerFormat(toCell[0], toCell[1])

        return self

    def export(self):
        return {
            "turn": self.turn,
            "from": self.fromCell,
            "to": self.toCell
        }
