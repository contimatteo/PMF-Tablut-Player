import fpm_tablut_player.configs as CONFIGS

from fpm_tablut_player.libraries.game_state import GameState
from fpm_tablut_player.libraries.game_node import GameNode

###

ROW_NAMES: list = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
COL_NAMES: list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
ROWS_SIZE: int = len(ROW_NAMES)
COLS_SIZE: int = len(COL_NAMES)


###


class GameMove:
    fromCell: str
    toCell: str
    turn: str

    ###

    def __init__(self):
        self.fromCell = None
        self.toCell = None
        self.turn = str(CONFIGS.APP_ROLE).lower()

    def __convertCellToServerFormat(self, x: int, y: int) -> str:
        if x < 0 or x > (ROWS_SIZE - 1):
            raise Exception("Wrong X cell (index) selected.")

        if y < 0 or y > (COLS_SIZE - 1):
            raise Exception("Wrong Y cell (index) selected.")

        return "{}{}".format(str(COL_NAMES[y]), str(ROW_NAMES[x]))

    def __getMoveFromGameNode(self, gameNode: GameNode) -> ((int, int), (int, int)):
        move = gameNode.moves[0]
        return (move["from"], move["to"])

    ###

    def fromGameNode(self, gameNode: GameNode):
        (fromCell, toCell) = self.__getMoveFromGameNode(gameNode)

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
