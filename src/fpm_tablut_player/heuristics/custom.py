import random

import fpm_tablut_player.configs as CONFIGS
from fpm_tablut_player.libraries import GameNode, GameState
from fpm_tablut_player.utils import DebugUtils, GameUtils


###

ESCAPE_CELLS: list = GameUtils.getEscapeCells()

###


class CustomHeuristic():

    @staticmethod
    def __iskingAlive(currentState: GameState) -> bool:
        return currentState.state.King is not None

    @staticmethod
    def __isKingOnEscapeArea(currentState: GameState) -> bool:
        found = False
        for escape in ESCAPE_CELLS:
            if escape == currentState.King:
                found = True
                break
        return found

    @staticmethod
    def __kingIsNearTheEscape(currentState: GameState):
        pass

    @staticmethod
    def __getPlayablePawns(currentState: GameState) -> int:
        if currentState.turn == "black":
            return currentState.state.BlackNumber
        return currentState.state.WhiteNumber

    @staticmethod
    def __blackPawnNearTheKing(currentState: GameState):
        #
        # TODO: missing ...
        #
        pass

    @staticmethod
    def __getNumberOfKills(currentState: GameState) -> int:
        #
        # TODO: missing ...
        #
        pass

    @staticmethod
    def __computeForBlack(currentState: GameState):
        #
        # TODO: missing ...
        #
        pass

    @staticmethod
    def __computeForWhite(currentState: GameState):
        #
        # TODO: missing ...
        #
        pass

    ###

    @staticmethod
    def assignValue(initialState: GameState, node: GameNode):
        value: int = 0
        currentState = None
        my_player_role = GameUtils.turnToString(CONFIGS.APP_ROLE)

        try:
            currentState = GameState().createFromMoves(initialState, node.moves)
        except Exception as error:
            if error.__class__.__name__ == "WhiteWinsException":
                if my_player_role == "white":
                    value = 1000000
                else:
                    value = -1000000
            elif error.__class__.__name__ == "BlackWinsException":
                if my_player_role == "white":
                    value = -1000000
                else:
                    value = 1000000
            else:
                value = 0

        # ########################################
        # TODO: [@contimatteo] remove this logic #
        value = random.randint(1, 101)
        # ########################################

        node.heuristic = value
