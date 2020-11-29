###


class GameUtils:

    @staticmethod
    def turnToString(rawTurn: str) -> str:
        return str(rawTurn).lower()

    @staticmethod
    def togglTurn(rawTurn: str) -> str:
        turn = GameUtils.turnToString(rawTurn)
        #
        if turn == 'white':
            return 'black'
        #
        return 'white'

    @staticmethod
    def getThroneCell() -> tuple:
        return (4, 4)

    @staticmethod
    def getCampCells() -> [tuple]:
        return [
            (0, 3), (0, 4), (0, 5), (1, 4),
            (3, 0), (3, 8), (4, 0), (4, 1),
            (4, 7), (4, 8), (5, 0), (5, 8),
            (7, 4), (8, 3), (8, 4), (8, 5)
        ]

    @staticmethod
    def getEscapeCells() -> [tuple]:
        return [
            (0, 1), (0, 2), (0, 6), (0, 7),
            (1, 0), (1, 8), (2, 0), (2, 8),
            (6, 0), (6, 8), (7, 0), (7, 8),
            (8, 1), (8, 2), (8, 6), (8, 7)
        ]
