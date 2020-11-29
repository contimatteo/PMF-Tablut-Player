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
